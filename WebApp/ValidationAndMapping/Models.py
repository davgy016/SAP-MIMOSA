from pydantic import BaseModel, RootModel, Field
from typing import List, Optional

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
    mapID: Optional[str] = None
    LLMType: str = Field(..., alias="llmType")
    mappings: List[MappingEntry]
    prompt: Optional[str] = None
    accuracyRate: Optional[float]=Field(None, alias="accuracyRate")
    qualityRate: Optional[float]=Field(None, alias="qualityRate")
    matchingRate: Optional[float]=Field(None, alias="matchingRate")

    class Config:
        allow_population_by_field_name = True

class MappingQuery(RootModel[List[Mapping]]):
    pass
