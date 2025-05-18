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
from .Models import AccuracyResult

class ScoreManager:
    
    # This method processes a list of MappingEntry objects and returns Overall mapping accuracy result and per mapping entry accuracy result.
    @staticmethod
    def scoreOutputWithDetails(mappings: list) -> dict:
        """
        Returns both the overall aggregated accuracy metrics and a list of per-mapping accuracy results.
        """
        accuracy_scorer = Accuracy()
        n = len(mappings)

        # Initialize accumulators
        accum = {
            "Accuracy":             0.0,
            "DescriptionSimilarity":0.0,
            "FieldLength":          0.0,
            "DataType":             0.0,
            "SAPSimilarity":        0.0,
            "InfoOmitted":          0.0,
            "MIMOSASimilarity":     0.0,
        }
        details = []

        if n == 0:
            # return zeroed-out AccuracyResult and empty details
            return {
                "overall": AccuracyResult(),  
                "details": []
            }

        # Score each pair
        for entry in mappings:
            scores = accuracy_scorer.calculateAccuracy(entry)

            # Build the per-entry AccuracyResult, using .get(...) so missing keys → 0
            details.append(
                AccuracyResult(
                    accuracyRate=             scores.get("Accuracy", 0.0) * 100,
                    descriptionSimilarity=    scores.get("DescriptionSimilarity", 0.0) * 100,
                    fieldLength=              scores.get("FieldLength", 0.0) * 100,
                    dataType=                 scores.get("DataType", 0.0) * 100,
                    sapSimilarity=            scores.get("SAPSimilarity", 0.0) * 100,
                    infoOmitted=              scores.get("InfoOmitted", 0.0) * 100,
                    mimosaSimilarity=         scores.get("MIMOSASimilarity", 0.0) * 100,
                )
            )

            # Accumulate for overall
            for k in accum:
                # normalize by n right away
                accum[k] += scores.get(k, 0.0) / n

        # Build the overall AccuracyResult
        overall = AccuracyResult(
            accuracyRate=             accum["Accuracy"] * 100,
            descriptionSimilarity=    accum["DescriptionSimilarity"] * 100,
            fieldLength=              accum["FieldLength"] * 100,
            dataType=                 accum["DataType"] * 100,
            sapSimilarity=            accum["SAPSimilarity"] * 100,
            infoOmitted=              accum["InfoOmitted"] * 100,
            mimosaSimilarity=         accum["MIMOSASimilarity"] * 100,
        )

        return {
            "overall": overall,
            "details": details
        }   

