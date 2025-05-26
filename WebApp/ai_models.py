import os
from openai import OpenAI as OpenAIClient
from ValidationAndMapping.Models import  MappingEntry
import json
from typing import List


class OpenAIModel:
    @staticmethod
    def get_generate_mapping_message():
        return (
            """You are an AI assistant for generating mapping between SAP and MIMOSA data models. "
            "Generate a structured JSON response that follows this exact format: "
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
            "Ensure all fields are filled with appropriate values. The platform for SAP should always be 'SAP' and for MIMOSA should always be 'MIMOSA'. "
            "Generate all mapping pairs that are accurate and relevant to the query."""
        )

    @staticmethod
    def get_improve_mappings_message(mappings):
        mappings_dict = [m.model_dump() for m in mappings]
        mappings_json = json.dumps(mappings_dict, ensure_ascii=False, indent=2)
        return (
            "You are an AI assistant for improving existing mappings between SAP and MIMOSA data models. "
            "Below are the current mapping pairs in JSON format:\n"
            f"{mappings_json}\n"
            "Review these mappings. Improve their accuracy, completeness, and clarity. "
            "If any mapping is incorrect, incomplete, or ambiguous, fix it. "
            "Return the improved mappings in the same JSON format. "
            "Do NOT remove any fields. Only update or clarify as needed. "
            "The platform for SAP should always be 'SAP' and for MIMOSA should always be 'MIMOSA'."
        )

    def __init__(self, query: str, llm_model: str, mappings: List[MappingEntry] = None, system_message: dict = None):
        self.query = query
        self.llm_model = llm_model
        self.mappings = mappings
        self.system_message = system_message
        self.api_key = os.getenv("OPENAI_API_KEY")

    def chat(self):
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        client = OpenAIClient(api_key=self.api_key)

        # Use the provided system_message if available
        if self.system_message:
            system_message = self.system_message
        else:
            if self.mappings and len(self.mappings) > 0:
                system_message_content = self.get_improve_mappings_message(self.mappings)
            else:
                system_message_content = self.get_generate_mapping_message()
            system_message = {
                "role": "system",
                "content": system_message_content
            }
        user_message = {"role": "user", "content": self.query}
        response = client.chat.completions.create(
            model=self.llm_model,
            messages=[system_message, user_message]
        )
        return response