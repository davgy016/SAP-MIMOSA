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
        self.descriptionScorer = DescriptionSimilarity()
        self.typeScorer        = DataType()
        self.sapChecker        = SAPChecker()
        self.mimosaChecker     = MimosaChecker()
    
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
        sapFc    = self.sapChecker.checkField(entry.sap)     # returns a FieldCheck
        sapScore = sapFc.toScore()                           
        scores["SAPSimilarity"] = sapScore

        # 2) MIMOSA schema check - flatten to single 0..1
        mimoFc    = self.mimosaChecker.checkField(entry.mimosa)
        mimoScore = mimoFc.toScore()
        scores["MIMOSASimilarity"] = mimoScore

        # 3) Build existence mask
        exist = Existence.fieldsPresent(entry)
        # exist is e.g. {"description": True, "dataType": False, ...}

        # 4) Conditional scorers
        scores["DescriptionSimilarity"] = (
            self.descriptionScorer.score(entry) if exist["description"] else 0.0
        )
        scores["DataType"] = (
            self.typeScorer.score(entry) if exist["dataType"] else 0.0
        )


        # 5) Dynamic Overall = average of whatever keys we have
        values = list(scores.values())
        scores["Accuracy"] = sum(values) / len(values) if values else 0.0

        for k,v in scores.items():
            scores[k] = max(0.0, min(v, 1.0))

        return scores
