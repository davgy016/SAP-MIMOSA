# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria

from .DataType import DataType
from .DescriptionSimilarity import DescriptionSimilarity
from .FieldLength import FieldLength
from .MimosaChecker import MimosaChecker
from .InfoOmitted import InfoOmitted
from .SAPChecker import SAPChecker
from .MimosaChecker import MimosaChecker

from ..Models import MappingEntry, FieldState


class Accuracy:
    def __init__(self):
        # instantiate once, reuse across calls
        self.description_scorer = DescriptionSimilarity()
        self.length_scorer      = FieldLength()
        self.type_scorer        = DataType()
        self.sap_checker        = SAPChecker()
        self.mimosa_checker     = MimosaChecker()
        self.exist_check  = InfoOmitted()
    
    def calculateAccuracy(self, entry: MappingEntry) -> dict:
        """
        Returns a dict in [0..1] by averaging:
         • description similarity
         • field-length similarity
         • data-type equality
         • SAP-schema validation score
        """        
        scores = {}

        # 1) SAP schema check - flatten to single 0..1
        sap_fc    = self.sap_checker.checkField(entry.sap)     # returns a FieldCheck
        sap_score = sap_fc.to_score()                           
        scores["SAPSimilarity"] = sap_score

        # 2) MIMOSA schema check - flatten to single 0..1
        mimo_fc    = self.mimosa_checker.checkField(entry.mimosa)
        mimo_score = mimo_fc.to_score()
        scores["MIMOSASimilarity"] = mimo_score

        # 3) Build existence mask
        exist = self.exist_check.existence(entry)
        # exist is e.g. {"description": True, "dataType": False, ...}

        # 4) Conditional scorers
        if exist["description"]:
            scores["DescriptionSimilarity"] = self.description_scorer.score(entry)

        if exist["dataType"]:
            scores["DataType"]    = self.type_scorer.score(entry)

        if exist["fieldLength"]:
            scores["FieldLength"] = self.length_scorer.score(entry)

        # 5) Dynamic Overall = average of whatever keys we have
        values = list(scores.values())
        overall = sum(values) / len(values) if values else 0.0
        scores["Accuracy"] = overall

        return scores
