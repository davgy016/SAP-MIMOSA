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
def loadData(file_path):
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

def convertDatetimes(obj):
    if isinstance(obj, dict):
        return {k: convertDatetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertDatetimes(i) for i in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat(timespec="seconds")
    else:
        return obj

def saveData(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        data = convertDatetimes(data)
        json.dump(data, file, ensure_ascii=False, indent=4)

def storeRawDataOfAiResponses(mapping_doc):	       
    entry = mapping_doc.model_dump(mode="json")
    
    try:
        data = loadData(rawDataStoragePath)           
        data.append(entry)            
        saveData(data, rawDataStoragePath)            
    except Exception as file_exc:
        print(f"Failed to write raw OpenAI response: {file_exc}")
        import traceback
        traceback.print_exc()


# Extract JSON from LLM response
def extractJsonFromResponse(response_text):
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
@app.get("/system_message")
def getSystemMessage(improveMappings: bool):
    # For improving mappings
    if improveMappings == True:
        systemMessage = OpenAIModel.getImproveMappingsMessage()
    else:
        # For initial mapping
        systemMessage = OpenAIModel.getGenerateMappingMessage()
    return JSONResponse(content={"system_message": systemMessage})

# OpenAI endpoint
@app.post("/ask_AI")
async def askAI(request: SearchQuery):
    try:
        llmModel = request.llmModel
        systemPrompt = request.systemPrompt                
        aiModel = OpenAIModel(request.Query, llmModel, request.mappings, systemPrompt)
        response = aiModel.chat()
        
        result = response.choices[0].message.content
        print(f"Sending response: {result}")

        # Extract JSON from LLM response
        json_str = extractJsonFromResponse(result)
        mappingDocDict = json.loads(json_str)
        #print("AI returned:", mappingDocDict)  
        
        if isinstance(mappingDocDict, dict) and "mappings" in mappingDocDict:
            mappings = mappingDocDict["mappings"]
        elif isinstance(mappingDocDict, list):
            mappings = mappingDocDict
        else:
            raise ValueError(f"AI response is not a dict with a 'mappings' key or a list. Got: {mappingDocDict}")

        # Convert list of dicts to list of MappingEntry objects
        mappingEntries = [MappingEntry(**item) for item in mappings]
        mappingDoc = MappingDocument(
            LLMType=llmModel,
            mappings=mappingEntries,
            prompt=request.Query,
            createdAt=datetime.datetime.now().isoformat(timespec="seconds")
        )
       
        # Call check_accuracy and set the accuracyResult and accuracy of Single MappingPair  properties
        accuracyResult = await checkAccuracy(mappingEntries)
        mappingDoc.accuracyResult = accuracyResult["overall"]
        mappingDoc.accuracySingleMappingPair = accuracyResult["singlePairAccuracydetails"]       

        # Store mapping_doc in Data/rawDataOfAIResponses.json for ranking LLMs performance 
        storeRawDataOfAiResponses(mappingDoc)

        # Return the Mapping object directly
        return mappingDoc

    except Exception as e:
        print(f"Error in ask_openai: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Get mappings
@app.get("/mappings")
async def getMappings():
    return loadData(storagePath)

@app.get("/mappings/{map_id}")
async def getMappings(map_id: str):
    data = loadData(storagePath)
    for doc in data:
        if str(doc.get("mapID")) == str(map_id):
            return doc
    raise HTTPException(status_code=404, detail="Mapping not found")

@app.post("/mappings")
async def createMappings(document: MappingDocument):
    data = loadData(storagePath)    
    if not document.mapID:
        existing_ids = [
            int(doc["mapID"]) for doc in data
            if "mapID" in doc and str(doc["mapID"]).isdigit()
        ]
        next_id = max(existing_ids, default=0) + 1
        document.mapID = f"{next_id:03d}"
    data.append(document.dict(exclude_none=True))
    saveData(data, storagePath)
    return document

# Update mapping 
@app.put("/mappings/{map_id}")
async def updateMappings(map_id: str, document: MappingDocument):
    data = loadData(storagePath)
    updated = False
    for idx, doc in enumerate(data):
        if str(doc.get("mapID")) == str(map_id):
            data[idx] = document.dict(exclude_none=True)
            updated = True
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"Mapping with mapID {map_id} not found.")
    saveData(data, storagePath)
    return document

@app.delete("/mappings/{map_id}")
async def deleteMappings(map_id: str):
    data = loadData(storagePath)
    originalLen = len(data)
    data = [doc for doc in data if str(doc.get("mapID")) != str(map_id)]
    if len(data) == originalLen:
        raise HTTPException(status_code=404, detail=f"Mapping with mapID {map_id} not found.")
    saveData(data, storagePath)
    return {"detail": f"Mapping with mapID {map_id} deleted successfully."}

# Retrieve historical data from Data/rawDataOfAIResponses.json
@app.get("/fetchHistoricalData")
async def getFilterHistoricalData(createdDate: Optional[datetime.datetime] = Query(None)):
    data = loadData(rawDataStoragePath)

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
async def checkAccuracy(entries: List[MappingEntry]):
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

