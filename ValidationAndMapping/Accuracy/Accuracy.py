# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria
from .AssociationMatching import AssociationMatching
from .DataType import DataType
from .DescriptionSimilarity import DescriptionSimilarity
from .FieldLength import FieldLength

class Accuracy:
    def calculateAccuracy(mappings: list):
        return float