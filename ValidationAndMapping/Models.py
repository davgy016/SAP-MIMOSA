from pydantic import BaseModel, RootModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum
from datetime import datetime

class FieldState(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    NARF = "not a real field"
    UNCHECKED = "has not been checked yet"

class SearchQuery(BaseModel):
    Query: str = Field(..., alias="query")
    systemPrompt: Optional[str] = Field(None, alias="system_prompt")
    llmModel: Optional[str] = Field(None, alias="llm_model")
    mappings:  Optional[List["MappingEntry"]]
    model_config = ConfigDict(validate_by_name=True)


class FieldMapping(BaseModel):
    platform: str
    entityName: str
    fieldName: str
    description: str
    dataType: str
    notes: Optional[str] = ""
    fieldLength: Optional[str] = ""
    
    def __eq__(self, other):
        if not isinstance(other, FieldMapping):
            return False
        return (
            self.platform == other.platform and
            self.entityName == other.entityName and
            self.fieldName == other.fieldName and
            self.description == other.description and
            self.dataType == other.dataType and
            self.fieldLength == other.fieldLength
        )
    
    def __hash__(self):
        return hash((
            self.platform,
            self.entityName,
            self.fieldName,
            self.description,
            self.dataType,
            self.fieldLength
        ))

class FieldCheck(BaseModel):
    entityName: FieldState = FieldState.UNCHECKED
    fieldName: FieldState = FieldState.UNCHECKED
    description: FieldState = FieldState.UNCHECKED
    dataType: FieldState = FieldState.UNCHECKED
    fieldLength: FieldState = FieldState.UNCHECKED

    def toScore(self) -> float:
        """
        Return ( #correct ) / ( #dimensions actually checked ).
        Unchecked dimensions (UNCHECKED) are excluded from both numerator and denominator.
        """
        states = list(self.model_dump().values())
        # keep only those we did check
        checked = [s for s in states if s is not FieldState.UNCHECKED]
        if not checked:
            return 0.0
        correct = sum(1 for s in checked if s is FieldState.CORRECT)
        return correct / len(checked)

class MappingEntry(BaseModel):
    sap: FieldMapping
    mimosa: FieldMapping
    class Config:
        extra = "ignore"

    def __eq__(self, other):
        if not isinstance(other, MappingEntry):
            return False
        return self.sap == other.sap and self.mimosa == other.mimosa
    
    def __hash__(self):
        return hash((self.sap, self.mimosa))

class AccuracyResult(BaseModel):
    accuracyRate: Optional[float] = None
    descriptionSimilarity: Optional[float] = None
    mimosaSimilarity: Optional[float] = None
    sapSimilarity: Optional[float] = None
    dataType: Optional[float] = None
    infoOmitted: Optional[float] = None
    fieldLength: Optional[float] = None
    missingFields: Optional[dict] = None

class promptEntry(BaseModel):
    text: Optional[str] = ""
    createdAt: Optional[datetime] = None

class Mapping(BaseModel):    
    createdAt: Optional[datetime] = None
    mapID: Optional[str] = None
    LLMType: str = ""
    prompts: List[str] = []
    promptHistory: List[promptEntry] = []
    mappings: List[MappingEntry] = []
    prompt: Optional[str] = ""
    accuracyResult: Optional[AccuracyResult] = None
    accuracySingleMappingPair: Optional[List[AccuracyResult]] = None

    model_config = ConfigDict(validate_by_name=True)

class MappingQuery(RootModel[List[Mapping]]):
    pass
