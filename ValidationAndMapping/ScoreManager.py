# Manager class used by ModelOutput that take in the model output as 
# a string and uses the Accuracy and Quality managers to calculate accuracy and quality scores. 
# A Score object is created using accuracy, quality and an aggregate of these two called total score 
# this object is then returned to the ModelOutput to be stored.

# Score class used to store results
from .Score import Score

#Score Managers
# from ValidationAndMapping.Quality import Quality
from .Accuracy import Accuracy, InfoOmitted
from .Models import Mapping
from typing import List
from .Models import AccuracyResult

class ScoreManager:

    @staticmethod
    def scoreOutput(mappings: list) -> dict:
        """
        This method processes a list of MappingEntry objects and returns aggregated accuracy metrics.
        Args:
            mappings (List[MappingEntry]): A list of MappingEntry objects to score.
        Returns:
            dict: The computed accuracy metrics as a dictionary.
        """
        print("Received mappings for scoring:", mappings)
        accuracy_scorer = Accuracy()
        info_ommitted = InfoOmitted()

        output = {
            "Accuracy": 0,
            "DataType": 0,
            "DescriptionSimilarity": 0,
            "SAPSimilarity": 0,
            "InfoOmitted": 0,
            "MimosaSimilarity": 0
        }
        n = len(mappings)
        if n == 0:
            return output
        for map in mappings:
            acc = accuracy_scorer.calculateAccuracy(map)
            output["Accuracy"] += acc["Accuracy"] / n
            output["DescriptionSimilarity"] += acc["DescriptionSimilarity"] / n
            output["DataType"] += acc["DataType"] / n
            output["SAPSimilarity"] += acc["SAPSimilarity"] / n
            output["InfoOmitted"] += info_ommitted.score_single(map,mappings) / n
            output["MimosaSimilarity"] += acc["MimosaSimilarity"] / n
        return output

    # This method processes a list of MappingEntry objects and returns Overall mapping accuracy result and per mapping entry accuracy result.
    @staticmethod
    def scoreOutputWithDetails(mappings: list) -> dict:
        """
        Returns both the overall aggregated accuracy metrics and a list of per-mapping-pair accuracy results.
        """
        accuracy_scorer = Accuracy()
        info_ommitted = InfoOmitted()

        n = len(mappings)
        overall = {
            "Accuracy": 0,
            "DataType": 0,
            "DescriptionSimilarity": 0,
            "SAPSimilarity": 0,
            "InfoOmitted": 0,
            "MimosaSimilarity": 0
        }
        singlePairAccuracydetails = []
        if n == 0:
            return {"overall": AccuracyResult(), "details": details}
        for map in mappings:
            acc = accuracy_scorer.calculateAccuracy(map)
            overall["Accuracy"] += acc["Accuracy"] / n
            overall["DescriptionSimilarity"] += acc["DescriptionSimilarity"] / n
            overall["DataType"] += acc["DataType"] / n
            overall["SAPSimilarity"] += acc["SAPSimilarity"] / n
            overall["InfoOmitted"] += info_ommitted.score_single(map,mappings) / n
            overall["MimosaSimilarity"] += acc["MimosaSimilarity"] / n
            singlePairAccuracydetails.append(AccuracyResult(
                accuracyRate=acc["Accuracy"],
                descriptionSimilarity=acc["DescriptionSimilarity"],
                mimosaSimilarity=acc["MimosaSimilarity"],
                sapSimilarity=acc["SAPSimilarity"],
                dataType=acc["DataType"],
                infoOmitted=info_ommitted.score_single(map,mappings),
            ))
        overall_result = AccuracyResult(
            accuracyRate=overall["Accuracy"],
            descriptionSimilarity=overall["DescriptionSimilarity"],
            mimosaSimilarity=overall["MimosaSimilarity"],
            sapSimilarity=overall["SAPSimilarity"],
            dataType=overall["DataType"],
            infoOmitted=info_ommitted.score_overall(mappings),
        )
        return {"overall": overall_result, "singlePairAccuracydetails": singlePairAccuracydetails}      

