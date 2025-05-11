# FieldLength checks the length of each field mapped to see if the data contained to likely to be comparable. 
# The closer they are in length the more likely it is they contain the same data. 

from ..Models import Mapping

class FieldLength:
    def score(self, mapping: Mapping) -> float:
        # get the values for sap and mimos
        entry = mapping.mappings[0]
        sap_fieldLength_str = entry.sap.fieldLength
        mimosa_fieldLength_str = entry.mimosa.fieldLength
       
        # convert to integers
        try:
            sap_fieldLength_int = int(sap_fieldLength_str)
            mimosa_fieldLength_int = int(mimosa_fieldLength_str)
            score = 1 - (abs(sap_fieldLength_int - mimosa_fieldLength_int) / max(sap_fieldLength_int, mimosa_fieldLength_int))
            return score
        except (ValueError, TypeError):
            print(f"Non-integer fieldLength encountered: SAP='{sap_fieldLength_str}', MIMOSA='{mimosa_fieldLength_str}'")
            return 0.0