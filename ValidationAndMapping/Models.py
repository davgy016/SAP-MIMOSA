from pydantic import BaseModel, RootModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum

class FieldState(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    NARF = "not a real field"
    UNCHECKED = "has not been checked yet"

class SearchQuery(BaseModel):
    Query: str = Field(..., alias="query")
    llm_model: Optional[str] = Field(None, alias="llm_model")
    mappings:  Optional[List["MappingEntry"]]
    model_config = ConfigDict(validate_by_name=True)


class FieldMapping(BaseModel):
    platform: str
    entityName: str
    fieldName: str
    description: str
    dataType: str
    notes: str
    fieldLength: str

class FieldCheck(BaseModel):
    entityName: FieldState = FieldState.UNCHECKED
    fieldName: FieldState = FieldState.UNCHECKED
    description: FieldState = FieldState.UNCHECKED
    dataType: FieldState = FieldState.UNCHECKED
    fieldLength: FieldState = FieldState.UNCHECKED

class MappingEntry(BaseModel):
    sap: FieldMapping
    mimosa: FieldMapping
    class Config:
        extra = "ignore"

class Mapping(BaseModel):
    mapID: Optional[str] = None
    LLMType: str
    prompt: Optional[str] = None
    accuracyRate: Optional[float]=None
    descriptionSimilarity: Optional[float]=None
    mimosaSimilarity: Optional[float]=None
    sapSimilarity: Optional[float]=None
    dataType: Optional[float]=None
    infoOmitted: Optional[float]=None
    fieldLength: Optional[float]=None
    mappings: List[MappingEntry]

    model_config = ConfigDict(validate_by_name=True)

class MappingQuery(RootModel[List[Mapping]]):
    pass
