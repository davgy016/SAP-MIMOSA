import os
from openai import OpenAI as OpenAIClient
from ValidationAndMapping.Models import  MappingEntry
import json
from typing import List


class OpenAIModel:
    @staticmethod
    def getGenerateMappingMessage():
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
    def getImproveMappingsMessage():
        
        return (
            "You are an AI assistant for improving existing mappings between SAP and MIMOSA data models. "
            "Review these mappings. Improve their accuracy, completeness, and clarity. "
            "If any mapping is incorrect, incomplete, or ambiguous, fix it. "
            "Return the improved mappings in the same JSON format. "
            "Do NOT remove any fields. Only update or clarify as needed. "
            "The platform for SAP should always be 'SAP' and for MIMOSA should always be 'MIMOSA'. "
            "Below are the current mapping pairs in JSON format:\n"            
        )

    def __init__(self, query: str, llmModel: str, mappings: List[MappingEntry] = None, systemPrompt: str = None):
        self.query = query
        self.llmModel = llmModel
        self.mappings = mappings
        self.systemPrompt = systemPrompt
        # if set up env for api key(check readme.md) keep following, otherwise directly set api key with your key self.apiKey = "YOUR_API_KEY"
        self.apiKey = os.getenv("OPENAI_API_KEY")

    def chat(self):
        if not self.apiKey:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        client = OpenAIClient(api_key=self.apiKey)

        # Decide which system message to use
        if self.systemPrompt and self.systemPrompt.strip():
            systemPrompt = self.systemPrompt
        else:
            if self.mappings and len(self.mappings) > 0:
                systemPrompt = self.getImproveMappingsMessage()
            else:
                systemPrompt = self.getGenerateMappingMessage()

        # If mappings exist, append them to the system_message
        if self.mappings:
            mappingsDict = [m.model_dump() for m in self.mappings]
            mappingsJson = json.dumps(mappingsDict, ensure_ascii=False, indent=2)
            systemPrompt += f"\n{mappingsJson}"

        system_message = {"role": "system", "content": systemPrompt}
        user_message = {"role": "user", "content": self.query}
        messages = [system_message, user_message]

        '''        
        print("Messages sent to OpenAI:")
        for m in messages:
            print(m) 
        '''

        response = client.chat.completions.create(
            model=self.llmModel,
            messages=messages
        )
        return response