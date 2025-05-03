import os
from openai import OpenAI as OpenAIClient


class OpenAIModel:
    def __init__(self, query: str, llm_model: str):
        self.query = query
        self.llm_model = llm_model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def chat(self):
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        client = OpenAIClient(api_key=self.api_key)
        
        system_message = {
            "role": "system",
            "content": (
                "You are an AI assistant for generating mapping between SAP and MIMOSA data models. "
                "Generate a structured JSON response that follows this exact format: "
                "{"
                  "\"mappings\": ["
                    "{"
                      "\"sap\": {"
                        "\"platform\": \"SAP\","
                        "\"entityName\": \"string\","
                        "\"fieldName\": \"string\","
                        "\"description\": \"string\","
                        "\"dataType\": \"string\","
                        "\"notes\": \"string\","
                        "\"fieldLength\": \"string\""
                      "},"
                      "\"mimosa\": {"
                        "\"platform\": \"MIMOSA\","
                        "\"entityName\": \"string\","
                        "\"fieldName\": \"string\","
                        "\"description\": \"string\","
                        "\"dataType\": \"string\","
                        "\"notes\": \"string\","
                        "\"fieldLength\": \"string\""
                      "}"
                    "}"
                  "]"
                "}"
                "Ensure all fields are filled with appropriate values. The platform for SAP should always be 'SAP' and for MIMOSA should always be 'MIMOSA'. "
                "Generate all mapping pairs that are accurate and relevant to the query."
            )
        }
        user_message = {"role": "user", "content": self.query}
        response = client.chat.completions.create(
            model=self.llm_model,
            messages=[system_message, user_message]
        )
        return response