from ValidationAndMapping.Models import Mapping
from ValidationAndMapping.SAPSchema import SAP_FIELD_INDEX
from DataType import normalize

class SapValidator:
    @staticmethod
    def score(mapping: Mapping) -> float:
        """
        Returns the fraction of SAP‐side fields that
        1) actually exist in the SAP_FIELD_INDEX
        2) match exactly on dataType AND fieldLength
        """
        entries = mapping.mappings
        if not entries:
            return 0.0

        valid = 0
        for entry in entries:
            label = entry.sap.fieldName.upper()
            defn  = SAP_FIELD_INDEX.get(label)
            if not defn:
                # AI invented a field that doesn't exist in SAPdata.json
                continue

            # Compare normalized types and numeric lengths
            same_type   = normalize(entry.sap.dataType) == normalize(defn.DataType)
            same_length = int(entry.sap.fieldLength) == defn.FieldLength

            if same_type and same_length:
                valid += 1

        return valid / len(entries)
