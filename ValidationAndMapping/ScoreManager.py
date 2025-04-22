# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
from ValidationAndMapping import Score

#Score Managers
from ValidationAndMapping import Quality
from ValidationAndMapping import Accuracy
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
        
        # Logic for scoring the mappings would go here
        # For now, we'll just return a placeholder score.
        # You can replace this with your actual scoring logic.
        
        score = 0.9
        
        return score
