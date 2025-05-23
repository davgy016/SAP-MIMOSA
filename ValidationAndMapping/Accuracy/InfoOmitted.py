#InfoOmitted checks if there is are any incomplete tables

from ..Models import MappingEntry
from pathlib import Path
import json

class InfoOmitted:
    """
    Checks that all entities have fields mapped to every map if not it calculates how much is missing.
    Scores as: (# entries) / (entries in entity).
    """

    def __init__(self):
        # locate the JSON next to the Data folder under ValidationAndMapping
        base = Path(__file__).parent.parent   # .../ValidationAndMapping
        schema = base / "Data" / "sapSchema.json"
        if not schema.exists():
            raise FileNotFoundError(f"Cannot find SAP schema at {schema}")

        raw = json.loads(schema.read_text(encoding="utf-8"))
        # build schema: { TABLE → { FIELD → meta } }
        self.schema = {}
        for table in raw:
            tbl = table["TableName"].upper()
            self.schema[tbl] = {
                fld["Field"].upper(): {
                    "DataType":    fld["SAP Type"],
                    "FieldLength": int(fld["Length"]),
                    "Description": fld["Description"],
                }
                for fld in table.get("Fields", [])
            }

        # flatten index of every field across all tables
        self.any_field_index = {
            field: meta
            for tbl_meta in self.schema.values()
            for field, meta in tbl_meta.items()
        }

    def score_overall(self, mapping: list) -> float:
        #total number of fields mapped 
        #TODO remove duplicates
        countFields = len(mapping)

        #a list of all the different entities
        entities = []
        for map in mapping:
            if map.sap.entityName not in entities:
                entities.append(map.sap.entityName)
        
        #a count of the number of fields across all entities
        totalFields = 0

        for entity in entities:
            entity = entity.upper()
            if entity in self.schema:
                tableFields = self.schema[entity]
                totalFields += len(tableFields)
        print(f"Fields counted in overall score {countFields} for entities {entities} with total fields {totalFields}")

        if totalFields == 0:
            return 0

        return countFields/totalFields
    
    def score_single(self, map: MappingEntry, mappings: list) -> float:
        countFields = 0 
        entity = map.sap.entityName.upper()

        for mapping in mappings:
            if mapping.sap.entityName.upper() == entity:
                countFields += 1
        
        totalFields = 0
        if entity in self.schema:
            tableFields = self.schema[entity]
            totalFields = len(tableFields)

        if totalFields == 0:
            return 0
        
        print(f"Fields counted in single score {countFields} for entity {entity} with total fields {totalFields}")

        return countFields/totalFields
