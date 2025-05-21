# This DataType engine compares the data type between mapped fields to see if they are likely to be able to contain similar data.
import re
from ..Models import MappingEntry

ALIASES = {
    "INT":       "INTEGER",
    "SMALLINT":  "INTEGER",
    "DEC":       "DECIMAL",
    "NUM":       "NUMERIC",
    "NumericType":"NUMERIC",
    "cct:NumericType":"NUMERIC",
    "CHAR":      "STRING",
    "VARCHAR":   "STRING",
    "TextType":  "STRING",
    "cct:TextType":  "STRING",
    "TEXT":      "STRING",
    "STRING":    "STRING",
    "DATE":      "DATE",
    "DATETIME":  "DATETIME",
    "TIMESTAMP": "DATETIME",
    "BinaryObjectType":"BOOL",
    "cct:BinaryObjectType":"BOOL",
    "boolean":"BOOL",
    "xs:boolean":"BOOL",
    "IDType":"ID",
    "cct:IDType":"ID",
    "UTCDateTime":"DATETIME",
    "cct:DateTimeType":"DATETIME",
    "DateTimeType":"DATETIME",
    "int":"INTEGER",
    "xs:int":"INTEGER",
    "string":"STRING",
    "xs:string":"STRING",
    "anyURI":"STRING",
    "xs:anyURI":"STRING",
    "nonNegativeInteger":"INTEGER",
    "xs:nonNegativeInteger":"INTEGER",
    "language":"STRING",
    "xs:language":"STRING"
    
}

def normalize(dt: str) -> str:
    dt = dt.strip().upper()
    base = re.split(r"\s*\(", dt)[0]
    return ALIASES.get(base, base)

class DataType:
    @staticmethod
    def score(mapping: MappingEntry) -> float:
        """
        mappings: list of MappingEntry objects or dicts with 'sap'/'mimosa' fields.
        Returns the fraction of fields whose normalized types match exactly.
        """
        entry = mapping       
        sap_dt = normalize(entry.sap.dataType)
        mimosa_dt = normalize(entry.mimosa.dataType)        
        
        return float(sap_dt == mimosa_dt)            
