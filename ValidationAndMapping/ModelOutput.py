# ModelOutput is a wrapper class for the output of the model. 
# It contains the output content, mappings and stores the calculate score for this content.
import Score

class ModelOutput:
    content: str
    mappings: list
    score: Score

    