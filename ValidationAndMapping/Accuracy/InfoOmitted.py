# The InfoOmitted engine checks if there is any important content missing from the output.

from ..Models import MappingEntry

class InfoOmitted:
    """
    Checks that each MappingEntry has non-empty
    `fieldName`, `dataType`, `description` and `fieldLength`.
    Scores as: (# entries with all info) / (total entries).
    """
    @staticmethod
    def score(mapping: MappingEntry) -> float:
        total = 10
        good = 0
        sap = mapping.sap
        # ensure none of these are empty or whitespace
        if all([
            sap.entityName and sap.entityName.strip(),
            sap.fieldName and sap.fieldName.strip(),
            sap.dataType    and sap.dataType.strip(),
            sap.description and sap.description.strip(),
            sap.fieldLength and sap.fieldLength.strip()
        ]):
            good += 1
        mimosa = mapping.mimosa
        # ensure none of these are empty or whitespace
        if all([
            mimosa.entityName and sap.entityName.strip(),
            mimosa.fieldName and sap.fieldName.strip(),
            mimosa.dataType    and sap.dataType.strip(),
            mimosa.description and sap.description.strip(),
            mimosa.fieldLength and sap.fieldLength.strip()
        ]):
            good += 1
        return good / total