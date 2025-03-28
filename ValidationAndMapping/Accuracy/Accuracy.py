# This engine class calculates the accuracy of the mappings generated using a series of criteria to generate a score.

#import criteria
import AssociationMatching
import DataType
import DescriptionSimilarity
import FieldLength

class Accuracy:
    def calculateAccuracy(mappings: list):
        return float