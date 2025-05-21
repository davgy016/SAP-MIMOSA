#SAP similarity compares the SAP side of the mapping to to the schema to see if it is a valid field.

from pathlib import Path
import json
from ..Models import FieldMapping, FieldState, FieldCheck


class SAPChecker:
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

    def checkField(self, field: FieldMapping) -> FieldCheck:
        # start all as NARF
        fc = FieldCheck(
            entityName=FieldState.NARF,
            fieldName=FieldState.NARF,
            dataType=FieldState.NARF,
            fieldLength=FieldState.NARF,
            description=FieldState.NARF,
        )

        tbl = field.entityName.upper()
        if tbl in self.schema:
            fc.entityName = FieldState.CORRECT
            table_fields = self.schema[tbl]
        else:
            # entity not found, but still check fieldName globally
            fc.entityName = FieldState.INCORRECT
            table_fields = {}

        fld = field.fieldName.upper()

        # 1) fieldName check: look in table first, then global index
        if fld in table_fields:
            fc.fieldName = FieldState.CORRECT
            meta = table_fields[fld]
        elif fld in self.any_field_index:
            fc.fieldName = FieldState.CORRECT
            meta = self.any_field_index[fld]
        else:
            return fc  # no such field anywhere

        # 2) dataType
        fc.dataType = FieldState.CORRECT if meta["DataType"].upper() == field.dataType.split("(")[0].upper() \
                      else FieldState.INCORRECT

        # 3) fieldLength
        try:
            fc.fieldLength = FieldState.CORRECT if meta["FieldLength"] == int(field.fieldLength) \
                              else FieldState.INCORRECT
        except ValueError:
            fc.fieldLength = FieldState.INCORRECT

        # 4) description
        fc.description = FieldState.CORRECT if meta["Description"].strip().lower() \
                                         == field.description.strip().lower() \
                         else FieldState.INCORRECT

        return fc