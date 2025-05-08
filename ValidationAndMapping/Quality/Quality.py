# The Quality manager calculates the quality of the model output using a series of engines to calculate a quality score.

#import engine classes to use
import Concisness
import InfoOmmitted

class Quality:
    def calculateScore(content: str):
        return float