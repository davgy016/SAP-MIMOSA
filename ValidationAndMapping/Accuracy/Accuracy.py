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
        self.type_scorer        = DataType()
        self.sap_checker        = SAPChecker()
        self.mimosa_checker     = MimosaChecker()
    
    def calculateAccuracy(self, mapping: MappingEntry) -> dict:
        """
        Returns a dict in [0..1] by averaging:
         • description similarity
         • field-length similarity
         • data-type equality
         • SAP-schema validation score
        """        
        output = {}
        desc_score  = self.description_scorer.score(mapping)
        type_score  = self.type_scorer.score(mapping)

        # SAP schema checks: get a FieldCheck per entry
        sap_field_checks = self.sap_checker.checkField(mapping.sap)

        # flatten to a single 0..1: 1 point per CORRECT, 0 otherwise
        total_checks = 5
        correct = sum(
            1
            for fc in sap_field_checks
            for state in fc
            if state == FieldState.CORRECT
        )
        sap_score = correct / total_checks if total_checks else 0.0

        # MIMOSA schema checks: get a FieldCheck per entry
        mimoosa_field_checks = self.mimosa_checker.checkField(mapping.mimosa)

        # flatten to a single 0..1: 1 point per CORRECT, 0 otherwise
        correct = sum(
            1
            for fc in mimoosa_field_checks
            for state in fc
            if state == FieldState.CORRECT
        )
        mimosa_score = correct / total_checks if total_checks else 0.0

        # average all components
        total = (desc_score + type_score + sap_score + mimosa_score) / 4.0

        output["Accuracy"] = total
        output["DescriptionSimilarity"] = desc_score
        output["FieldLength"] = len_score
        output["DataType"] = type_score
        output["SAPSimilarity"] = sap_score
        output["MimosaSimilarity"] = mimosa_score

        return output
