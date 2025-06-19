# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
from .Score import Score

#Score Managers
# from ValidationAndMapping.Quality import Quality
from .Accuracy import Accuracy, InfoOmitted
from .Models import MappingEntry
from typing import List
from .Models import AccuracyResult

class ScoreManager:
    
    # This method processes a list of MappingEntry objects and returns Overall mapping accuracy result and per mapping entry accuracy result.
    @staticmethod
    def scoreOutputWithDetails(entries: list[MappingEntry]) -> dict:
        acc = Accuracy()
        info = InfoOmitted()
        n   = len(entries)
        keys = [
            "Accuracy",
            "DescriptionSimilarity",
            "DataType",
            "SAPSimilarity",
            "MIMOSASimilarity",
            # "InfoOmitted",
        ]

        # zero out accumulators
        overall_sum = {k: 0.0 for k in keys}
        details     = []
        missingFieldsList = info.getMissingFields(entries)

        if n == 0:
            return {"overall": AccuracyResult(), "singlePairAccuracydetails": []}

        for e in entries:
            scores = acc.calculateAccuracy(e)

            # compute coverage for this entry
            infoSingle = info.scoreSingle(e, entries)

            # build per‐entry detail
            details.append(AccuracyResult(
                accuracyRate          = scores["Accuracy"]          ,
                descriptionSimilarity = scores["DescriptionSimilarity"] ,
                dataType              = scores["DataType"]              ,
                sapSimilarity         = scores["SAPSimilarity"]         ,
                mimosaSimilarity      = scores["MIMOSASimilarity"]      ,
                infoOmitted           = infoSingle                     ,
            ))

            # accumulate
            for k in keys:
                overall_sum[k] += scores[k] / n
        
        # build overall result
        overall = AccuracyResult(
          accuracyRate          = overall_sum["Accuracy"]          ,
          descriptionSimilarity = overall_sum["DescriptionSimilarity"] ,
          dataType              = overall_sum["DataType"]              ,
          sapSimilarity         = overall_sum["SAPSimilarity"]         ,
          mimosaSimilarity      = overall_sum["MIMOSASimilarity"]      ,
          infoOmitted           = info.scoreOverall(entries)         ,
          missingFields         = missingFieldsList                    ,
        )

        return {
            "overall": overall,
            "singlePairAccuracydetails": details
        }

