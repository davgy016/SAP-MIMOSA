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
    LLMType: str
    mappings: List[MappingEntry]
    prompt: Optional[str] = None
    accuracyRate: Optional[float]=None
    qualityRate: Optional[float]=None
    matchingRate: Optional[float]=None

    class Config:
        allow_population_by_field_name = True

class MappingQuery(RootModel[List[Mapping]]):
    pass
