# The InfoOmitted engine checks if there is any important content missing from the output.

from ..Models import Mapping, MappingEntry

class InfoOmitted:
    """
    Checks that each MappingEntry has non-empty
    `fieldName`, `dataType`, `description` and `fieldLength`.
    Scores as: (# entries with all info) / (total entries).
    """
    @staticmethod
    def score(mapping: Mapping) -> float:
        total = len(mapping.mappings)
        if total == 0:
            return 0.0
        good = 0
        for entry in mapping.mappings:
            sap = entry.sap
            # ensure none of these are empty or whitespace
            if all([
                sap.fieldName and sap.fieldName.strip(),
                sap.dataType    and sap.dataType.strip(),
                sap.description and sap.description.strip(),
                sap.fieldLength and sap.fieldLength.strip()
            ]):
                good += 1
        return good / total