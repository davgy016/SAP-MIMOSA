# This DataType engine compares the data type of mapped fields to compare similarity.
import re
from ..Models import Mapping

ALIASES = {
    "INT":       "INTEGER",
    "SMALLINT":  "INTEGER",
    "DEC":       "DECIMAL",
    "NUM":       "NUMERIC",
    "CHAR":      "CHAR",
    "VARCHAR":   "VARCHAR",
    "TEXT":      "VARCHAR",
    "DATE":      "DATE",
    "DATETIME":  "DATETIME",
    "TIMESTAMP": "DATETIME",
}

def normalize(dt: str) -> str:
    dt = dt.strip().upper()
    base = re.split(r"\s*\(", dt)[0]
    return ALIASES.get(base, base)

class DataType:
    @staticmethod
    def score(mapping: Mapping) -> float:
        """
        mappings: list of MappingEntry objects or dicts with 'sap'/'mimosa' fields.
        Returns the fraction of fields whose normalized types match exactly.
        """
        entry = mapping.mappings[0]
        sap_dt = normalize(entry.sap.dataType)
        mimosa_dt = normalize(entry.mimosa.dataType)

        return float(sap_dt == mimosa_dt)
