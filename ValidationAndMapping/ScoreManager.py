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

        # only the Accuracy.calculateAccuracy keys
        core_metrics = [
            "SAPSimilarity",
            "MIMOSASimilarity",
            "DescriptionSimilarity",
            "DataType",
            "Accuracy",
        ]

        # prepare accumulators for those five metrics
        overall_sums = {m: 0.0 for m in core_metrics}
        counts       = {m: 0   for m in core_metrics}
        details      = []

        for e in entries:
            # get 0..1 scores from Accuracy
            scores = acc.calculateAccuracy(e)

            # override/add the per-entry InfoOmitted
            scores["InfoOmitted"] = info.score_single(e, entries)

            # record the detail row 
            details.append(AccuracyResult(
                sapSimilarity         = scores["SAPSimilarity"]    ,
                mimosaSimilarity      = scores["MIMOSASimilarity"] ,
                descriptionSimilarity = scores["DescriptionSimilarity"] ,
                dataType              = scores["DataType"]             ,
                accuracyRate          = scores["Accuracy"]            ,
                infoOmitted           = scores["InfoOmitted"]         ,
            ))

            # accumulate only the *core* metrics
            for m in core_metrics:
                val = scores.get(m)
                if val is None:
                    continue
                overall_sums[m] += scores[m]
                counts[m]       += 1

        # compute overall averages for core metrics
        overall = AccuracyResult(
            sapSimilarity         = (overall_sums["SAPSimilarity"]    / counts["SAPSimilarity"])     if counts["SAPSimilarity"]    else None,
            mimosaSimilarity      = (overall_sums["MIMOSASimilarity"] / counts["MIMOSASimilarity"])  if counts["MIMOSASimilarity"] else None,
            descriptionSimilarity = (overall_sums["DescriptionSimilarity"] / counts["DescriptionSimilarity"])  if counts["DescriptionSimilarity"] else None,
            dataType              = (overall_sums["DataType"]              / counts["DataType"])               if counts["DataType"]              else None,
            accuracyRate          = (overall_sums["Accuracy"]              / counts["Accuracy"])               if counts["Accuracy"]              else None,
            infoOmitted           = info.score_overall(entries)        ,
        )
        

        return {
            "overall": overall,
            "singlePairAccuracydetails": details
        }

