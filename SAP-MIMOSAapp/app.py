from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
import os
import uvicorn
from typing import List, Optional

# Initialize OpenAI client
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# JSON file path
JSON_FILE = "Data/JsonTemplate.json"

# Models
from pydantic import BaseModel, Field
class SearchQuery(BaseModel):
    Query: str = Field(..., alias="query")
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
    mapID: str
    LLMType: str
    mappings: List[MappingPair]
    #color: Optional[str] = None

# JSON file operations
def load_data():
    if not os.path.exists(JSON_FILE):
        os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            default_data = []
            json.dump(default_data, file, ensure_ascii=False, indent=4)
        return default_data
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# OpenAI endpoint
@app.post("/ask_openai")
async def ask_openai(request: SearchQuery):
    try:
        print(f"Received query: {request.Query}")  # already camelCase usage
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an Generative AI assistant for generating mapping between SAP and MIMOSA data models."},
                {"role": "user", "content": request.Query +" response provide in json format"}  # already camelCase usage
            ]
        )
        
        result = response.choices[0].message.content
        print(f"Sending response: {result}")
        return {"response": result}

    except Exception as e:
        print(f"Error in ask_openai: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Work order endpoints
@app.get("/workorders")
async def get_workorders():
    return load_data()

@app.put("/workorders")
async def update_workorders(documents: List[MappingDocument]):
    save_data([doc.dict(exclude_none=True) for doc in documents])
    return documents

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

