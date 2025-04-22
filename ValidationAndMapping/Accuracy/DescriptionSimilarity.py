# DescriptionSimilarity compares the descriptions associated with each mapped field and scores how similar these descriptions are.
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm
from WebApp.Models import Mapping

class DescriptionSimilarity:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT model

    def score(self, mappings: list):
        # Get the sap and mimosa descriptions from the mapping object
        sap_desc = mappings[0].sap_description
        mimosa_desc = mappings[0].mimosa_description

        #encode descriptions
        sap_vector = self.model.encode(sap_desc)
        mimosa_vector = self.model.encode(mimosa_desc)

        #measure similarity https://hyperskill.org/learn/step/22997

        score = np.dot(sap_vector, mimosa_vector) / (
            norm(sap_vector) * norm(mimosa_vector)
        )

        print(score)

        return score