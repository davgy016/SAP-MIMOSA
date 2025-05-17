# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
from .Score import Score

#Score Managers
# from ValidationAndMapping.Quality import Quality
from .Accuracy import Accuracy
from .Models import Mapping
from typing import List

class ScoreManager:

    @staticmethod
    def scoreOutput(mappings: list) -> dict:
        """
        This method processes a list of MappingEntry objects and returns aggregated accuracy metrics.
        Args:
            mappings (List[MappingEntry]): A list of MappingEntry objects to score.
        Returns:
            dict: The computed accuracy metrics as a dictionary.
        """
        print("Received mappings for scoring:", mappings)
        accuracy_scorer = Accuracy()

        output = {
            "Accuracy": 0,
            "DataType": 0,
            "DescriptionSimilarity": 0,
            "FieldLength": 0,
            "SAPSimilarity": 0,
            "InfoOmitted": 0,
            "MimosaSimilarity": 0
        }
        n = len(mappings)
        if n == 0:
            return output
        for map in mappings:
            acc = accuracy_scorer.calculateAccuracy(map)
            output["Accuracy"] += acc["Accuracy"] / n
            output["DescriptionSimilarity"] += acc["DescriptionSimilarity"] / n
            output["FieldLength"] += acc["FieldLength"] / n
            output["DataType"] += acc["DataType"] / n
            output["SAPSimilarity"] += acc["SAPSimilarity"] / n
            output["InfoOmitted"] += acc["InfoOmitted"] / n
            output["MimosaSimilarity"] += acc["MimosaSimilarity"] / n
        return output

