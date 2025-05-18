# The InfoOmitted engine checks if there is any important content missing from the output.

from ..Models import MappingEntry

class InfoOmitted:
    @staticmethod
    def existence(mapping: MappingEntry) -> dict[str,bool]:
        """Return which of the 5 metadata fields that actually exist on *both* SAP and MIMOSA."""
        sap = mapping.sap
        mim = mapping.mimosa

        has = lambda attr: bool(
            getattr(sap,   attr, None) and getattr(sap,   attr).strip() and
            getattr(mim,   attr, None) and getattr(mim,   attr).strip()
        )
        return {
            "entityName": has("entityName"),
            "fieldName":  has("fieldName"),
            "description":has("description"),
            "dataType":   has("dataType"),
            "fieldLength":has("fieldLength"),
        }