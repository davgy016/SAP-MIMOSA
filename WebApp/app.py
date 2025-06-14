from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI
import json
import os
import re
import uvicorn
from .ai_models import OpenAIModel
from typing import List, Optional
from uuid import uuid4
from ValidationAndMapping.ScoreManager import ScoreManager
from ValidationAndMapping.Models import MappingQuery, SearchQuery, MappingEntry, Mapping as MappingDocument
from datetime import datetime
from fastapi import Query
from fastapi.responses import JSONResponse


# Initialize OpenAI client
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# JSON storage file path
storagePath = "Data/SAPMIMOSA.json"
# JSON Raw-Data file path
rawDataStoragePath = "Data/rawDataOfAIResponses.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:7090"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

import datetime

def convert_datetimes(obj):
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(i) for i in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat(timespec="seconds")
    else:
        return obj

def save_data(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        data = convert_datetimes(data)
        json.dump(data, file, ensure_ascii=False, indent=4)

def store_raw_data_of_AI_responses(mapping_doc):	       
    entry = mapping_doc.model_dump(mode="json")
    
    try:
        data = load_data(rawDataStoragePath)           
        data.append(entry)            
        save_data(data, rawDataStoragePath)            
    except Exception as file_exc:
        print(f"Failed to write raw OpenAI response: {file_exc}")
        import traceback
        traceback.print_exc()


# Extract JSON from LLM response
def extract_json_from_response(response_text):
    # Extract Json
    match = re.search(r"```json\s*([\s\S]*?)\s*```", response_text)
    if match:
        return match.group(1)
    # Find the first Json-looking structure
    match = re.search(r"(\[.*\]|\{.*\})", response_text, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("No JSON found in AI response")


# Endpoint to get system initial message of ai_model
@app.get("/system-message")
def get_system_message(improve_mappings: bool):
    # For improving mappings
    if improve_mappings == True:
        system_message = OpenAIModel.get_improve_mappings_message()
    else:
        # For initial mapping
        system_message = OpenAIModel.get_generate_mapping_message()
    return JSONResponse(content={"system_message": system_message})

# OpenAI endpoint
@app.post("/ask_AI")
async def ask_AI(request: SearchQuery):
    try:
        llm_model = request.llm_model
        system_prompt = request.system_prompt                
        ai_model = OpenAIModel(request.Query, llm_model, request.mappings, system_prompt)
        response = ai_model.chat()
        
        result = response.choices[0].message.content
        print(f"Sending response: {result}")

        # Extract JSON from LLM response
        json_str = extract_json_from_response(result)
        mapping_doc_dict = json.loads(json_str)
        #print("AI returned:", mapping_doc_dict)  
        
        if isinstance(mapping_doc_dict, dict) and "mappings" in mapping_doc_dict:
            mappings = mapping_doc_dict["mappings"]
        elif isinstance(mapping_doc_dict, list):
            mappings = mapping_doc_dict
        else:
            raise ValueError(f"AI response is not a dict with a 'mappings' key or a list. Got: {mapping_doc_dict}")

        # Convert list of dicts to list of MappingEntry objects
        mapping_entries = [MappingEntry(**item) for item in mappings]
        mapping_doc = MappingDocument(
            LLMType=llm_model,
            mappings=mapping_entries,
            prompt=request.Query,
            createdAt=datetime.datetime.now().isoformat(timespec="seconds")
        )
       
        # Call check_accuracy and set the accuracyResult and accuracy of Single MappingPair  properties
        accuracy_result = await check_accuracy(mapping_entries)
        mapping_doc.accuracyResult = accuracy_result["overall"]
        mapping_doc.accuracySingleMappingPair = accuracy_result["singlePairAccuracydetails"]       

        # Store mapping_doc in Data/rawDataOfAIResponses.json for ranking LLMs performance 
        store_raw_data_of_AI_responses(mapping_doc)

        # Return the Mapping object directly
        return mapping_doc

    except Exception as e:
        print(f"Error in ask_openai: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Get mappings
@app.get("/mappings")
async def get_mappings():
    return load_data(storagePath)

@app.get("/mappings/{map_id}")
async def get_mappings(map_id: str):
    data = load_data(storagePath)
    for doc in data:
        if str(doc.get("mapID")) == str(map_id):
            return doc
    raise HTTPException(status_code=404, detail="Mapping not found")

@app.post("/mappings")
async def create_mappings(document: MappingDocument):
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

# Update mapping 
@app.put("/mappings/{map_id}")
async def update_mappings(map_id: str, document: MappingDocument):
    data = load_data(storagePath)
    updated = False
    for idx, doc in enumerate(data):
        if str(doc.get("mapID")) == str(map_id):
            data[idx] = document.dict(exclude_none=True)
            updated = True
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"Mapping with mapID {map_id} not found.")
    save_data(data, storagePath)
    return document

@app.delete("/mappings/{map_id}")
async def delete_mappings(map_id: str):
    data = load_data(storagePath)
    original_len = len(data)
    data = [doc for doc in data if str(doc.get("mapID")) != str(map_id)]
    if len(data) == original_len:
        raise HTTPException(status_code=404, detail=f"Mapping with mapID {map_id} not found.")
    save_data(data, storagePath)
    return {"detail": f"Mapping with mapID {map_id} deleted successfully."}

# Retrieve historical data from Data/rawDataOfAIResponses.json
@app.get("/fetchHistoricalData")
async def get_filter_historicalData(createdDate: Optional[datetime.datetime] = Query(None)):
    data = load_data(rawDataStoragePath)

    if createdDate:
        createdDateStr = createdDate.isoformat(timespec="seconds")
        result = [
            map for map in data
            if map.get("createdAt") == createdDateStr
        ]
        return result

    return data


# Pydantic's BaseModel does not preserve the exact decimal places of floats. Roudning in ScoreManager did not work,
# when  do round(x, 2), it stores the binary float.
# but when serializing to JSON, it dumps the full binary float representation. 
# Also myltiply by 100 to get the percentage
def to_decimals(d):
    return {k: (round(v* 100, 2) if isinstance(v, float) and v is not None else v) for k, v in d.items()}

@app.post("/check_accuracy")
async def check_accuracy(entries: List[MappingEntry]):
    results = ScoreManager.scoreOutputWithDetails(entries)    
    return {
        "overall": to_decimals(results["overall"].model_dump()),
        "singlePairAccuracydetails": [to_decimals(r.model_dump()) for r in results["singlePairAccuracydetails"]]        
    }

def start():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# Run the FastAPI app
#if __name__ == "__main__":
   # uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

