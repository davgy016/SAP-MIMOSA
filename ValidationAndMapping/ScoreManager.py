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
    def scoreOutput(mapping: Mapping) -> float:
        """
        This method processes the list of Mapping objects and returns a score.
        
        Args:
            mappings (List[Mapping]): A list of Mapping objects to score.
        
        Returns:
            str: The computed score as a string.
        """
        print("Received mappings for scoring:", mapping.mappings)
        
        # Create accuracy and quality objects to score each mapping
        accuracy_scorer = Accuracy()

        # Numbers to store the aggregate of each type of score
        accuracy_score = 0

        output = {}
        output["Accuracy"] = 0  
        output["DataType"] = 0
        output["DescriptionSimilarity"] = 0
        output["FieldLength"] = 0
        output["SAPSimilarity"] = 0
        output["DataType"] = 0
        output["InfoOmitted"] = 0
        output["MimosaSimilarity"] = 0

        # Iterate over all of the mappings
        for map in mapping.mappings:
            output["Accuracy"] += accuracy_scorer.calculateAccuracy(map)["Accuracy"]/len(mapping.mappings)
            output["DescriptionSimilarity"] += accuracy_scorer.calculateAccuracy(map)["DescriptionSimilarity"]/len(mapping.mappings)
            output["FieldLength"] += accuracy_scorer.calculateAccuracy(map)["FieldLength"]/len(mapping.mappings)
            output["DataType"] += accuracy_scorer.calculateAccuracy(map)["DataType"]/len(mapping.mappings)
            output["SAPSimilarity"] += accuracy_scorer.calculateAccuracy(map)["SAPSimilarity"]/len(mapping.mappings)
            output["InfoOmitted"] += accuracy_scorer.calculateAccuracy(map)["InfoOmitted"]/len(mapping.mappings)
            output["MimosaSimilarity"] += accuracy_scorer.calculateAccuracy(map)["MimosaSimilarity"]/len(mapping.mappings)
        
        print(output)
        return output
