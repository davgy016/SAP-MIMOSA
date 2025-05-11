import json, os
from pydantic import BaseModel
from typing import Dict

# Pydantic model to represent ONE SAP‐side field definition
class SapFieldDef(BaseModel):
    Label:       str  # the field name, e.g. "QMNUM"
    DataType:    str  # e.g. "CHAR(12)"
    Description: str
    FieldLength: int

# Load the JSON file once and build a dict keyed by the SAP field label
def load_sap_fields(path: str) -> Dict[str, SapFieldDef]:
    raw = json.load(open(path, encoding="utf-8"))
    lookup: Dict[str, SapFieldDef] = {}
    for rec in raw:
        # each rec has a "SapField": [ {...} ]
        for sf in rec.get("SapField", []):
            label = sf["Label"].upper()
            lookup[label] = SapFieldDef(
                Label=       sf["Label"],
                DataType=    sf["DataType"],
                Description=sf["Description"],
                FieldLength=int(sf["FieldLength"]) if sf["FieldLength"] else 0
            )
    return lookup

HERE = os.path.dirname(__file__)
SAP_FIELD_INDEX = load_sap_fields(os.path.join(HERE, "Data\sapSchema.json"))
