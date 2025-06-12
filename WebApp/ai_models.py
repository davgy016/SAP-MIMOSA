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
    def get_improve_mappings_message():
        
        return (
            "You are an AI assistant for improving existing mappings between SAP and MIMOSA data models. "
            "Review these mappings. Improve their accuracy, completeness, and clarity. "
            "If any mapping is incorrect, incomplete, or ambiguous, fix it. "
            "Return the improved mappings in the same JSON format. "
            "Do NOT remove any fields. Only update or clarify as needed. "
            "The platform for SAP should always be 'SAP' and for MIMOSA should always be 'MIMOSA'. "
            "Below are the current mapping pairs in JSON format:\n"            
        )

    def __init__(self, query: str, llm_model: str, mappings: List[MappingEntry] = None, system_prompt: str = None):
        self.query = query
        self.llm_model = llm_model
        self.mappings = mappings
        self.system_prompt = system_prompt
        self.api_key = ""

    def chat(self):
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        client = OpenAIClient(api_key=self.api_key)

        # Decide which system message to use
        if self.system_prompt and self.system_prompt.strip():
            system_prompt = self.system_prompt
        else:
            if self.mappings and len(self.mappings) > 0:
                system_prompt = self.get_improve_mappings_message()
            else:
                system_prompt = self.get_generate_mapping_message()

        # If mappings exist, append them to the system_message
        if self.mappings:
            mappings_dict = [m.model_dump() for m in self.mappings]
            mappings_json = json.dumps(mappings_dict, ensure_ascii=False, indent=2)
            system_prompt += f"\n{mappings_json}"

        system_message = {"role": "system", "content": system_prompt}
        user_message = {"role": "user", "content": self.query}
        messages = [system_message, user_message]

        '''        
        print("Messages sent to OpenAI:")
        for m in messages:
            print(m) 
        '''

        response = client.chat.completions.create(
            model=self.llm_model,
            messages=messages
        )
        return response