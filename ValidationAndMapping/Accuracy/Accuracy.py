# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria
# from .AssociationMatching import AssociationMatching
from .DataType import DataType
from .DescriptionSimilarity import DescriptionSimilarity
from .FieldLength import FieldLength
from .MimosaChecker import MimosaChecker
from .SapValidator import SapValidator

from ..Models import Mapping


class Accuracy:
    def calculateAccuracy(self, mapping:  Mapping) -> float:
        """ 
            Calcualte accruacy takes a single mapping and outputs an accuracy score
        
            Args:
                mapping (Mapping): A Mapping object to score.
            
            Returns:
                float: The computed score as a float.
        """
        # Run the mapping through description similarity
        # 1) Type match (exact or 0)
        dt_score    = DataType.score(mapping)
        # 2) Textual similarity of descriptions (0–1)
        desc_score  = DescriptionSimilarity().score(mapping)
        # 3) Relative field‐length closeness (0–1)
        fl_score    = FieldLength.score(mapping)
        # 4) Entity‐level association (0–1)
        assoc_score = AssociationMatching.score(mapping)

        sapdoc_score = SapValidator.score(mapping)   

        # Simple unweighted average:
        return (dt_score + desc_score + fl_score + assoc_score + sapdoc_score) / 5.0
