# This engine class uses SAP PM and MIMOSA CCOM schema to check how similar the associatons between the two fileds mapped are. 
from ..Models import Mapping

class AssociationMatching:
    @staticmethod
    def score(mapping: Mapping) -> float:
        """
        Checks whether the SAP entityName “aligns” with the MIMOSA entityName
        for each field‐pair. Returns the fraction of entries that match.
        """
        entries = mapping.mappings
        if not entries:
            return 0.0

        matches = 0
        for entry in entries:
            sap_ent    = entry.sap.entityName.strip().lower()
            mimosa_ent = entry.mimosa.entityName.strip().lower()
            # if MIMOSA uses dotted paths, just take the root
            if "." in mimosa_ent:
                mimosa_ent = mimosa_ent.split(".")[0]

            if sap_ent == mimosa_ent:
                matches += 1

        return matches / len(entries)