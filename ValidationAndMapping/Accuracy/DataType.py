# DataType compares the data type between mapped fields to see if they are likely to be able to contain similar data.
# DataType.py
import re
from ..Models import MappingEntry

# Original alias definitions (mixed case) – keep these human-readable
rawAliases = {
    "INT":       "INTEGER",
    "SMALLINT":  "INTEGER",
    "DEC":       "DECIMAL",
    "NUM":       "NUMERIC",
    "cct:NumericType":"NUMERIC",
    "CHAR":      "STRING",
    "VARCHAR":   "STRING",
    "TextType":  "STRING",
    "cct:TextType":  "STRING",
    "TEXT":      "STRING",
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

# Build an uppercase-key alias map once
ALIASES = { key.upper(): val for key, val in rawAliases.items() }

def normalize(dt: str) -> str:
    """Turn any dt string into a canonical category like INTEGER, STRING, DATE, etc."""
    # 1) strip whitespace, uppercase
    s = dt.strip().upper()
    # 2) remove any "namespace:" prefix
    if ":" in s:
        s = s.split(":", 1)[1]
    # 3) drop any "(...)" parameters
    base = re.split(r"\s*\(", s)[0]
    # 4) lookup in our uppercase alias map
    return ALIASES.get(base, base)

class DataType:
    @staticmethod
    def score(mapping: MappingEntry) -> float:
        """
        Returns 1.0 if the normalized SAP type exactly matches
        the normalized MIMOSA type, else 0.0.
        """
        sapDt    = normalize(mapping.sap.dataType)
        mimosaDt = normalize(mapping.mimosa.dataType)
        return 1.0 if sapDt == mimosaDt else 0.0
    
