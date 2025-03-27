# python3 -m uvicorn app:fastapi_app --host 0.0.0.0 --port 8000

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI


# Initialize OpenAI client
client = OpenAI()

app = FastAPI()

# Request Model
class SearchQuery(BaseModel):
    query: str

@app.post("/ask_openai")
async def ask_openai(request: SearchQuery):
    try:
        # Correct method for chat-based models
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant for SAP-MIMOSA work order mapping."},
                {"role": "user", "content": request.query}
            ]
        )
        return {"response": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
