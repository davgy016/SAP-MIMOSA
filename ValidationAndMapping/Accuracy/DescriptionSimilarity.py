# DescriptionSimilarity compares the descriptions associated with each mapped field and scores how similar these descriptions are.
from sentence_transformers import SentenceTransformer
import Mapping

class DescriptionSimilarity:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT model

    def score(mappings: list):
        print(mappings[0].sap_description)
        
        # Natural language processing to compare meaning https://hyperskill.org/learn/step/22997
        return mappings