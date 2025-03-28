# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
import Score

#Score Managers
import Quality
import Accuracy

class ScoringManager:
    def scoreOutput(content: str):
        return Score