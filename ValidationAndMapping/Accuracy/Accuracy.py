# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria

from .DataType import DataType
from .DescriptionSimilarity import DescriptionSimilarity
from .FieldLength import FieldLength
from .MimosaChecker import MimosaChecker
from ..Existence          import Existence
from .SAPChecker import SAPChecker
from .MimosaChecker import MimosaChecker

from ..Models import MappingEntry, FieldState


class Accuracy:
    def __init__(self):
        # instantiate once, reuse across calls
        self.description_scorer = DescriptionSimilarity()
        self.type_scorer        = DataType()
        self.sap_checker        = SAPChecker()
        self.mimosa_checker     = MimosaChecker()
    
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
        exist = Existence.fields_present(entry)
        # exist is e.g. {"description": True, "dataType": False, ...}

        # 4) Conditional scorers
        if exist["description"]:
            scores["DescriptionSimilarity"] = self.description_scorer.score(entry)
        else:
            scores["DescriptionSimilarity"] = None

        scores["DataType"] = (
            self.type_scorer.score(entry) if exist["dataType"] else 0.0
        )
        if exist["dataType"]:
            scores["DataType"] = self.description_scorer.score(entry)
        else:
            scores["DataType"] = None        

        # 5) Dynamic Overall 
        real_values = [v for v in scores.values() if isinstance(v, float)]
        if real_values:
            dynamic_avg = sum(real_values) / len(real_values)
        else:
            dynamic_avg = None

        scores["Accuracy"] = dynamic_avg

        for k,v in scores.items():
            if isinstance(v, float):
                scores[k] = max(0.0, min(v, 1.0))

        return scores
