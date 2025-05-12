from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm
from ..Models import MappingEntry
class DescriptionSimilarity:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT model

    def score(self, mapping: MappingEntry) -> float:
        # For now, we'll just score the first MappingEntry in the first Mapping object
        entry = mapping
        sap_desc = entry.sap.description
        mimosa_desc = entry.mimosa.description

        # Encode descriptions
        sap_vector = self.model.encode(sap_desc)
        mimosa_vector = self.model.encode(mimosa_desc)

        # Cosine similarity
        score = np.dot(sap_vector, mimosa_vector) / (
            norm(sap_vector) * norm(mimosa_vector)
        )

        return score
