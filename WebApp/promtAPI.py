# python3 -m uvicorn app:fastapi_app --host 0.0.0.0 --port 8000

import sys
import os
from typing import List, Optional

# Add sibling of parent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sibling_dir = os.path.join(parent_dir, 'ValidationAndMapping')
sys.path.append(sibling_dir)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, RootModel
from openai import OpenAI
import ScoreManager


# Initialize OpenAI client
# client = OpenAI()

app = FastAPI()

# Request Model
class SearchQuery(BaseModel):
    query: str

# @app.post("/ask_openai")
# async def ask_openai(request: SearchQuery):
#     try:
#         # Correct method for chat-based models
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are an AI assistant for SAP-MIMOSA work order mapping."},
#                 {"role": "user", "content": request.query}
#             ]
#         )
#         return {"response": response.choices[0].message.content}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

class FieldMapping(BaseModel):
    platform: str
    entityName: str
    fieldName: str
    description: str
    dataType: str
    notes: str
    fieldLength: str

class MappingEntry(BaseModel):
    sap: FieldMapping
    mimosa: FieldMapping

class Mapping(BaseModel):
    mapID: str
    LLMType: str
    mappings: List[MappingEntry]

class MappingQuery(RootModel[List[Mapping]]):
    pass

@app.post("/check_accuracy")
async def check_accuracy(output: MappingQuery):
    data = output.root 
    score = ScoreManager.ScoringManager.scoreOutput(data)
    print(score)
    return score

