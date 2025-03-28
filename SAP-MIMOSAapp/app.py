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
JSON_FILE = "Data/SAPdata.json"

# Models
class SearchQuery(BaseModel):
    query: str


# JSON file operations
def load_data():
    if not os.path.exists(JSON_FILE):
        os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        return []
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
        print(f"Received query: {request.query}")
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an Generative AI assistant for generating mapping between SAP and MIMOSA data models."},
                {"role": "user", "content": request.query}
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

@app.get("/workorders/{id}")
async def get_workorder(id: int):
    workorders = load_data()
    workorder = next((w for w in workorders if w.get("Id") == id), None)
    if not workorder:
        raise HTTPException(status_code=404, detail="Work order not found")
    return workorder

@app.post("/workorders")
async def add_workorder(workorder: dict):
    workorders = load_data()
    
    # Ensure all keys use correct casing
    new_workorder = {key.capitalize(): value for key, value in workorder.items()}
    
    # Assign the correct ID
    max_id = max((w["Id"] for w in workorders if "Id" in w), default=0)
    new_workorder["Id"] = max_id + 1
    
    # Remove any old lowercase "id" if present
    new_workorder.pop("id", None)
    
    workorders.append(new_workorder)
    save_data(workorders)
    return new_workorder

@app.put("/workorders/{id}")
async def update_workorder(id: int, workorder: dict):
    workorders = load_data()
    
    # Ensure keys are capitalized
    updated_data = {key.capitalize(): value for key, value in workorder.items()}
    
    for w in workorders:
        if w.get("Id") == id:
            w.update(updated_data)
            w["Id"] = id  # Prevent ID modification
            w.pop("id", None)  # Remove any old lowercase ID
            save_data(workorders)
            return w
            
    raise HTTPException(status_code=404, detail="Work order not found")

@app.delete("/workorders/{id}")
async def delete_workorder(id: int):
    workorders = load_data()
    updated_workorders = [w for w in workorders if w.get("Id") != id]
    
    if len(updated_workorders) == len(workorders):
        raise HTTPException(status_code=404, detail="Work order not found")
        
    save_data(updated_workorders)
    return {"detail": "Work order deleted"}

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")