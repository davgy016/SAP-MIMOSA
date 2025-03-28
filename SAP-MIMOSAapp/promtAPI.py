
# This code is not necessary anymore, it is merged with app.py


# python3 -m uvicorn app:fastapi_app --host 0.0.0.0 --port 8000

# from fastapi import fastapi, httpexception
# from pydantic import basemodel
# from openai import openai


# # initialize openai client
# client = openai()

# app = fastapi()

# # request model
# class searchquery(basemodel):
#     query: str

# @app.post("/ask_openai")
# async def ask_openai(request: searchquery):
#     try:
#         # correct method for chat-based models
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "you are an ai assistant for sap-mimosa work order mapping."},
#                 {"role": "user", "content": request.query}
#             ]
#         )
#         return {"response": response.choices[0].message.content}
    
#     except exception as e:
#         raise httpexception(status_code=500, detail=str(e))
