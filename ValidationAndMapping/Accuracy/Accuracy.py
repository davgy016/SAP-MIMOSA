# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria

from .DataType import DataType
from .DescriptionSimilarity import DescriptionSimilarity
from .FieldLength import FieldLength
from .MimosaChecker import MimosaChecker
from .SAPChecker                import SAPChecker

from ..Models import Mapping, FieldState


class Accuracy:
    def __init__(self):
        # instantiate once, reuse across calls
        self.description_scorer = DescriptionSimilarity()
        self.length_scorer      = FieldLength()
        self.type_scorer        = DataType()
        self.sap_checker        = SAPChecker()

    def calculateAccuracy(self, mapping: Mapping) -> float:
        """
        Returns a float in [0..1] by averaging:
         • description similarity
         • field-length similarity
         • data-type equality
         • SAP-schema validation score
        """

        desc_score  = self.description_scorer.score(mapping)
        len_score   = self.length_scorer.score(mapping)
        type_score  = self.type_scorer.score(mapping)

        # SAP schema checks: get a FieldCheck per entry
        field_checks = [ self.sap_checker.checkField(entry.sap)
                         for entry in mapping.mappings ]

        # flatten to a single 0..1: 1 point per CORRECT, 0 otherwise
        total_checks = len(field_checks) * 5
        correct = sum(
            1
            for fc in field_checks
            for state in fc.model_dump().values()
            if state == FieldState.CORRECT
        )
        sap_score = correct / total_checks if total_checks else 0.0

        # average all components
        return (desc_score + len_score + type_score + sap_score) / 4.0
