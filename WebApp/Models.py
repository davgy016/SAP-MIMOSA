from pydantic import BaseModel, RootModel
from typing import List

class SearchQuery(BaseModel):
    query: str


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
