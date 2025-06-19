# Description similarity compares the meaning of descriptions across a mapping to see if the fields are likely to contain similar information.

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
        sapDesc = entry.sap.description
        mimosaDesc = entry.mimosa.description

        # Encode descriptions
        sapVector = self.model.encode(sapDesc)
        mimosaVector = self.model.encode(mimosaDesc)

        # Cosine similarity
        score = np.dot(sapVector, mimosaVector) / (
            norm(sapVector) * norm(mimosaVector)
        )

        return score
