# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
from ValidationAndMapping import Score

#Score Managers
# from ValidationAndMapping.Quality import Quality
from ValidationAndMapping.Accuracy import Accuracy
from WebApp.Models import Mapping
from typing import List

class ScoreManager:

    @staticmethod
    def scoreOutput(mappings: List[Mapping]) -> float:
        """
        This method processes the list of Mapping objects and returns a score.
        
        Args:
            mappings (List[Mapping]): A list of Mapping objects to score.
        
        Returns:
            str: The computed score as a string.
        """
        print("Received mappings for scoring:", mappings[0].mappings)
        
        # Create accuracy and quality objects to score each mapping
        accuracy_scorer = Accuracy()

        # Numbers to store the aggregate of each type of score
        accuracy_score = 0

        # Iterate over all of the mappings
        for map in mappings:
            accuracy_score = accuracy_scorer.calculateAccuracy(map)
        
        return accuracy_score
