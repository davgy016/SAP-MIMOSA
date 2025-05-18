from pathlib import Path
import json
import re
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

        # build alias map from CheckTable → actual table metadata
        self.alias_map = {}
        for table in raw:
            real_tbl = table["TableName"].upper()
            meta_block = self.schema.get(real_tbl, {})
            for fld in table.get("Fields", []):
                chk = fld.get("CheckTable", "").upper()
                # ignore wildcards or empty
                if chk and chk != "*" and chk != real_tbl:
                    # only keep the first mapping (most JSONs tend to repeat)
                    self.alias_map.setdefault(chk, meta_block)

    def _normalize_table(self, name: str) -> str:
        """
        Strip off anything after the first word, e.g.
        "AUFK (OrderMaster)" → "AUFK"
        """
        name = name.upper().strip()
        m = re.match(r"^(\w+)", name)
        return m.group(1) if m else name

    def checkField(self, field: FieldMapping) -> FieldCheck:
        # start all as NARF
        fc = FieldCheck(
            entityName=FieldState.NARF,
            fieldName=FieldState.NARF,
            dataType=FieldState.NARF,
            fieldLength=FieldState.NARF,
            description=FieldState.NARF,
        )

        # normalize the incoming entityName
        tbl_raw = field.entityName
        tbl = self._normalize_table(tbl_raw)

        # pick the right metadata block
        if tbl in self.schema:
            fc.entityName = FieldState.CORRECT
            table_fields = self.schema[tbl]
        elif tbl in self.alias_map:
            # use CheckTable if original table was just an alias
            fc.entityName = FieldState.CORRECT
            table_fields = self.alias_map[tbl]
        else:
            # table not found
            fc.entityName = FieldState.INCORRECT
            table_fields = {}

        # normalize the incoming fieldName
        fld = field.fieldName.upper().strip()

        # 1) fieldName check: look in table first, then global index
        if fld in table_fields:
            fc.fieldName = FieldState.CORRECT
            meta = table_fields[fld]
        elif fld in self.any_field_index:
            fc.fieldName = FieldState.CORRECT
            meta = self.any_field_index[fld]
        else:
            # no such field anywhere
            return fc

        # 2) dataType
        got_type = field.dataType.split("(")[0].upper().strip()
        fc.dataType = (
            FieldState.CORRECT
            if meta["DataType"].upper() == got_type
            else FieldState.INCORRECT
        )

        # 3) fieldLength
        try:
            fc.fieldLength = (
                FieldState.CORRECT
                if meta["FieldLength"] == int(field.fieldLength)
                else FieldState.INCORRECT
            )
        except Exception:
            fc.fieldLength = FieldState.INCORRECT

        # 4) description
        fc.description = (
            FieldState.CORRECT
            if meta["Description"].strip().lower()
               == field.description.strip().lower()
            else FieldState.INCORRECT
        )

        return fc