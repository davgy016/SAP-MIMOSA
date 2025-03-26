from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import threading
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import JSONResponse

# Initialize OpenAI client
client = OpenAI()

# Flask app for work orders
flask_app = Flask(__name__)
CORS(flask_app)  # Enable CORS
# FastAPI app for OpenAI
fastapi_app = FastAPI()
# Add Flask app as middleware to FastAPI
fastapi_app.mount("/flask", WSGIMiddleware(flask_app))


JSON_FILE = "Data/SAPdata.json"


class SearchQuery(BaseModel):
    query: str


@fastapi_app.post("/ask_openai")
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




# Flask routes for work orders
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


@flask_app.route("/workorders", methods=["GET"])
def get_workorders():
    return jsonify(load_data())


@flask_app.route("/workorders/<int:Id>", methods=["GET"])
def get_workorder(Id):
    workorders = load_data()
    workorder = next((w for w in workorders if w.get("Id") == Id), None)
    return jsonify(workorder) if workorder else ("Not Found", 404)


@flask_app.route("/workorders", methods=["POST"])
def add_workorder():
    workorders = load_data()
    new_workorder = request.json

    # Ensure all keys use correct casing
    new_workorder = {key.capitalize(): value for key, value in new_workorder.items()}

    # Assign the correct ID
    max_id = max((w["Id"] for w in workorders if "Id" in w), default=0)
    new_workorder["Id"] = max_id + 1

    # Remove any old lowercase "id" if present
    new_workorder.pop("id", None)

    workorders.append(new_workorder)
    save_data(workorders)
    return jsonify(new_workorder), 201


@flask_app.route("/workorders/<int:Id>", methods=["PUT"])
def update_workorder(Id):
    workorders = load_data()
    updated_data = request.json

    # Ensure keys are capitalized
    updated_data = {key.capitalize(): value for key, value in updated_data.items()}

    for w in workorders:
        if w.get("Id") == Id:
            w.update(updated_data)
            w["Id"] = Id  # Prevent ID modification
            w.pop("id", None)  # Remove any old lowercase ID
            save_data(workorders)
            return jsonify(w)
    return "Not Found", 404


@flask_app.route("/workorders/<int:Id>", methods=["DELETE"])
def delete_workorder(Id):
    workorders = load_data()
    updated_workorders = [w for w in workorders if w.get("Id") != Id]

    if len(updated_workorders) == len(workorders):
        return "Not Found", 404

    save_data(updated_workorders)
    return "Deleted", 204


# Add Flask app as middleware to FastAPI
fastapi_app.mount("/flask", WSGIMiddleware(flask_app))


# Run the FastAPI app and Flask app together
if __name__ == "__main__":
    # Run both FastAPI and Flask on separate threads
    threading.Thread(target=lambda: fastapi_app.run(port=8000)).start()
    flask_app.run(port=5000)
