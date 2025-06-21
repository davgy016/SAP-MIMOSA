from .Models import MappingEntry

class Existence:
    @staticmethod
    def fieldsPresent(entry: MappingEntry) -> dict[str, bool]:
        """
        Returns a dict telling us which metadata fields were
        actually provided by the AI in *both* sap & mimosa.
        """
        sap   = entry.sap
        mimo  = entry.mimosa

        return {
            "description": bool(sap.description.strip()) and bool(mimo.description.strip()),
            "dataType":    bool(sap.dataType.strip())    and bool(mimo.dataType.strip()),
        }