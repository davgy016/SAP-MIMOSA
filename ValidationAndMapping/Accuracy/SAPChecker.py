#SAP similarity compares the SAP side of the mapping to to the schema to see if it is a valid field.

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
        self.anyFieldIndex = {
            field: meta
            for tblMeta in self.schema.values()
            for field, meta in tblMeta.items()
        }

        # build alias map from CheckTable → actual table metadata
        self.aliasMap = {}
        for table in raw:
            realTbl = table["TableName"].upper()
            metaBlock = self.schema.get(realTbl, {})
            for fld in table.get("Fields", []):
                chk = fld.get("CheckTable", "").upper()
                # ignore wildcards or empty
                if chk and chk != "*" and chk != realTbl:
                    # only keep the first mapping (most JSONs tend to repeat)
                    self.aliasMap.setdefault(chk, metaBlock)

    def normalizeTable(self, name: str) -> str:
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
        tblRaw = field.entityName
        tbl = self.normalizeTable(tblRaw)

        # pick the right metadata block
        if tbl in self.schema:
            fc.entityName = FieldState.CORRECT
            tableFields = self.schema[tbl]
        elif tbl in self.aliasMap:
            # use CheckTable if original table was just an alias
            fc.entityName = FieldState.CORRECT
            tableFields = self.aliasMap[tbl]
        else:
            # table not found
            fc.entityName = FieldState.INCORRECT
            tableFields = {}

        # normalize the incoming fieldName
        fld = field.fieldName.upper().strip()

        # 1) fieldName check: look in table first, then global index
        if fld in tableFields:
            fc.fieldName = FieldState.CORRECT
            meta = tableFields[fld]
        elif fld in self.anyFieldIndex:
            fc.fieldName = FieldState.CORRECT
            meta = self.anyFieldIndex[fld]
        else:
            # no such field anywhere
            return fc

        # 2) dataType
        gotType = field.dataType.split("(")[0].upper().strip()
        fc.dataType = (
            FieldState.CORRECT
            if meta["DataType"].upper() == gotType
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