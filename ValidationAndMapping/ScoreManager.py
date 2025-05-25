# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
from .Score import Score

#Score Managers
# from ValidationAndMapping.Quality import Quality
from .Accuracy import Accuracy
from .Models import MappingEntry
from typing import List
from .Models import AccuracyResult

class ScoreManager:
    
    # This method processes a list of MappingEntry objects and returns Overall mapping accuracy result and per mapping entry accuracy result.
    @staticmethod
    def scoreOutputWithDetails(entries: list[MappingEntry]) -> dict:
        acc = Accuracy()
        n   = len(entries)
        keys = [
            "Accuracy",
            "DescriptionSimilarity",
            "FieldLength",
            "DataType",
            "SAPSimilarity",
            "MIMOSASimilarity",
        ]

        # zero out accumulators
        overall_sum = {k: 0.0 for k in keys}
        details     = []

        if n == 0:
            return {"overall": AccuracyResult(), "singlePairAccuracydetails": []}

        for e in entries:
            scores = acc.calculateAccuracy(e)

            # build per‐entry detail
            details.append(AccuracyResult(
                accuracyRate          = scores["Accuracy"]          * 100,
                descriptionSimilarity = scores["DescriptionSimilarity"] * 100,
                fieldLength           = scores["FieldLength"]           * 100,
                dataType              = scores["DataType"]              * 100,
                sapSimilarity         = scores["SAPSimilarity"]         * 100,
                mimosaSimilarity      = scores["MIMOSASimilarity"]      * 100,
            ))

            # accumulate
            for k in keys:
                overall_sum[k] += scores[k] / n

        # build overall result
        overall = AccuracyResult(
          accuracyRate          = overall_sum["Accuracy"]          * 100,
          descriptionSimilarity = overall_sum["DescriptionSimilarity"] * 100,
          fieldLength           = overall_sum["FieldLength"]           * 100,
          dataType              = overall_sum["DataType"]              * 100,
          sapSimilarity         = overall_sum["SAPSimilarity"]         * 100,
          mimosaSimilarity      = overall_sum["MIMOSASimilarity"]      * 100,
        )

        return {
            "overall": overall,
            "singlePairAccuracydetails": details
        }

