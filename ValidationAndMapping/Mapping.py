# DEPRECEATED NOW USING WebApp.Models

class Mapping:
    def __init__(self, sap_fieldName, sap_fieldLength, sap_dataType, sap_description, 
                 mimosa_fieldName, mimosa_fieldLength, mimosa_dataType, mimosa_description):
        self.sap_fieldName = sap_fieldName
        self.sap_fieldLength = sap_fieldLength
        self.sap_dataType = sap_dataType
        self.sap_description = sap_description
        self.mimosa_fieldName = mimosa_fieldName
        self.mimosa_fieldLength = mimosa_fieldLength
        self.mimosa_dataType = mimosa_dataType
        self.mimosa_description = mimosa_description

    def __repr__(self):
        return (f"Mapping(sap_fieldName={self.sap_fieldName}, sap_fieldLength={self.sap_fieldLength}, "
                f"sap_dataType={self.sap_dataType}, sap_description={self.sap_description}, "
                f"mimosa_fieldName={self.mimosa_fieldName}, mimosa_fieldLength={self.mimosa_fieldLength}, "
                f"mimosa_dataType={self.mimosa_dataType}, mimosa_description={self.mimosa_description})")

    def to_dict(self):
        """Convert the mapping to a dictionary."""
        return {
            "sap_fieldName": self.sap_fieldName,
            "sap_fieldLength": self.sap_fieldLength,
            "sap_dataType": self.sap_dataType,
            "sap_description": self.sap_description,
            "mimosa_fieldName": self.mimosa_fieldName,
            "mimosa_fieldLength": self.mimosa_fieldLength,
            "mimosa_dataType": self.mimosa_dataType,
            "mimosa_description": self.mimosa_description
        }
