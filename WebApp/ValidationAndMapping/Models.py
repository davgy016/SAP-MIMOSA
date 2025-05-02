from pydantic import BaseModel, RootModel, Field, ConfigDict
from typing import List, Optional

class SearchQuery(BaseModel):
    Query: str = Field(..., alias="query")
    llm_model: Optional[str] = Field(None, alias="llm_model")
    model_config = ConfigDict(validate_by_name=True)


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

    model_config = ConfigDict(validate_by_name=True)

class MappingQuery(RootModel[List[Mapping]]):
    pass
