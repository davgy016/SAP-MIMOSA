# FieldLength checks the length of each field mapped to see if the data contained to likely to be comparable. 
# The closer they are in length the more likely it is they contain the same data. 

from ..Models import MappingEntry

class FieldLength:
    def score(self, mapping: MappingEntry) -> float:
        # get the values for sap and mimos
        entry = mapping
        sapFieldLengthStr = entry.sap.fieldLength
        mimosaFieldLengthStr = entry.mimosa.fieldLength
       
        # convert to integers
        try:
            sapFieldLengthInt = int(sapFieldLengthStr)
            mimosaFieldLengthInt = int(mimosaFieldLengthStr)
            score = 1 - (abs(sapFieldLengthInt - mimosaFieldLengthInt) / max(sapFieldLengthInt, mimosaFieldLengthInt))
            return score
        except (ValueError, TypeError):
            print(f"Non-integer fieldLength encountered: SAP='{sapFieldLengthStr}', MIMOSA='{mimosaFieldLengthStr}'")
            return 0.0