# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria
from .AssociationMatching import AssociationMatching
from .DataType import DataType
from .DescriptionSimilarity import DescriptionSimilarity
from .FieldLength import FieldLength

from WebApp.Models import Mapping


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
        ds = DescriptionSimilarity()
        ds_score = ds.score(mapping)

        return ds_score