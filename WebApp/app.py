from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI
import json
import os
import uvicorn
from typing import List, Optional
from uuid import uuid4
from ValidationAndMapping.ScoreManager import ScoreManager
from ValidationAndMapping.Models import MappingQuery, SearchQuery, MappingEntry, Mapping as MappingDocument
from datetime import datetime

# Initialize OpenAI client
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# JSON storage file path
storagePath = "Data/SAPMIMOSA.json"
# JSON Raw-Data file path
rawDataStoragePath = "Data/rawDataOfAIResponses.json"

"""
# Models
class SearchQuery(BaseModel):
    Query: str = Field(..., alias="query")
    llm_model: Optional[str] = Field(None, alias="llm_model")
    class Config:
        allow_population_by_field_name = True


class MappingField(BaseModel):
    platform: str
    entityName: str
    fieldName: str
    description: str
    dataType: str
    notes: str
    fieldLength: str

class MappingPair(BaseModel):
    sap: MappingField
    mimosa: MappingField

class MappingDocument(BaseModel):
    mapID: Optional[str] = None
    LLMType: str
    mappings: List[MappingPair]
    prompt: Optional[str] = None
    #color: Optional[str] = None
"""
# JSON file operations
def load_data(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            default_data = []
            json.dump(default_data, file, ensure_ascii=False, indent=4)
        return default_data
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_data(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# OpenAI endpoint
@app.post("/ask_openai")
async def ask_openai(request: SearchQuery):
    try:
        llm_model = request.llm_model 
        print(f"Received query: {request.Query}, LLM Model: {llm_model}")
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": """You are an AI assistant for generating mapping between SAP and MIMOSA data models.
                Generate a structured JSON response that follows this exact format:
                {
                  "mappings": [
                    {
                      "sap": {
                        "platform": "SAP",
                        "entityName": "string",
                        "fieldName": "string",
                        "description": "string",
                        "dataType": "string",
                        "notes": "string",
                        "fieldLength": "string"
                      },
                      "mimosa": {
                        "platform": "MIMOSA",
                        "entityName": "string",
                        "fieldName": "string",
                        "description": "string",
                        "dataType": "string",
                        "notes": "string",
                        "fieldLength": "string"
                      }
                    }
                  ]
                }
                
                Ensure all fields are filled with appropriate values. The platform for SAP should always be "SAP" and for MIMOSA should always be "MIMOSA".
                Generate all mapping pairs that are accurate and relevant to the query."""},    
                {"role": "user", "content": request.Query }
            ]
        )
        
        result = response.choices[0].message.content
        print(f"Sending response: {result}")

        mapping_doc_dict = json.loads(result)
        # This is a list of dicts
        mappings = mapping_doc_dict["mappings"]  

        # Convert list of dicts to list of MappingEntry objects
        mapping_entries = [MappingEntry(**item) for item in mappings]

        # Create a Mapping object with required fields
        mapping_doc = MappingDocument(
            LLMType=llm_model,
            mappings=mapping_entries,
            prompt=request.Query
        )

        # Call check_accuracy and set the scores on the Mapping object
        mapping_query = MappingQuery(root=[mapping_doc])
        accuracyResult = await check_accuracy(mapping_query)
        mapping_doc.accuracyRate = accuracyResult["accuracy_score"]
        mapping_doc.qualityRate = accuracyResult["quality_score"]
        mapping_doc.matchingRate = accuracyResult["matching_score"] 
        
        # Return the Mapping object directly!
        return mapping_doc

    except Exception as e:
        print(f"Error in ask_openai: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Work order endpoints
@app.get("/workorders")
async def get_workorders():
    return load_data(storagePath)

@app.post("/workorders")
async def create_workorder(document: MappingDocument):
    data = load_data(storagePath)    
    if not document.mapID:
        existing_ids = [
            int(doc["mapID"]) for doc in data
            if "mapID" in doc and str(doc["mapID"]).isdigit()
        ]
        next_id = max(existing_ids, default=0) + 1
        document.mapID = f"{next_id:03d}"
    data.append(document.dict(exclude_none=True))
    save_data(data, storagePath)
    return document

@app.put("/workorders")
async def update_workorders(documents: List[MappingDocument]):
    save_data([doc.dict(exclude_none=True) for doc in documents], storagePath)
    return documents

@app.delete("/workorders/{map_id}")
async def delete_workorder(map_id: str):
    data = load_data(storagePath)
    original_len = len(data)
    data = [doc for doc in data if str(doc.get("mapID")) != str(map_id)]
    if len(data) == original_len:
        raise HTTPException(status_code=404, detail=f"Mapping with mapID {map_id} not found.")
    save_data(data, storagePath)
    return {"detail": f"Mapping with mapID {map_id} deleted successfully."}



@app.post("/check_accuracy")
async def check_accuracy(output: MappingQuery):
    data = output.root 
    accuracy_score = float(ScoreManager.scoreOutput(data))*100
    quality_score = float(0.75451) *100
    matching_score = float(0.80561)*100
    
    return {
        "accuracy_score": round(accuracy_score,2),
        "quality_score": round(quality_score, 2),
        "matching_score": round(matching_score,2)
        
    }



# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

