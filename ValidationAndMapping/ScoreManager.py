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

        output = {
            "Accuracy": 0,
            "DataType": 0,
            "DescriptionSimilarity": 0,
            "FieldLength": 0,
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
            output["FieldLength"] += acc["FieldLength"] / n
            output["DataType"] += acc["DataType"] / n
            output["SAPSimilarity"] += acc["SAPSimilarity"] / n
            output["InfoOmitted"] += acc["InfoOmitted"] / n
            output["MimosaSimilarity"] += acc["MimosaSimilarity"] / n
        return output

    # This method processes a list of MappingEntry objects and returns Overall mapping accuracy result and per mapping entry accuracy result.
    @staticmethod
    def scoreOutputWithDetails(mappings: list) -> dict:
        """
        Returns both the overall aggregated accuracy metrics and a list of per-mapping-pair accuracy results.
        """
        accuracy_scorer = Accuracy()
        n = len(mappings)
        overall = {
            "Accuracy": 0,
            "DataType": 0,
            "DescriptionSimilarity": 0,
            "FieldLength": 0,
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
            overall["FieldLength"] += acc["FieldLength"] / n
            overall["DataType"] += acc["DataType"] / n
            overall["SAPSimilarity"] += acc["SAPSimilarity"] / n
            overall["InfoOmitted"] += acc["InfoOmitted"] / n
            overall["MimosaSimilarity"] += acc["MimosaSimilarity"] / n
            singlePairAccuracydetails.append(AccuracyResult(
                accuracyRate=acc["Accuracy"] * 100,
                descriptionSimilarity=acc["DescriptionSimilarity"] * 100,
                mimosaSimilarity=acc["MimosaSimilarity"] * 100,
                sapSimilarity=acc["SAPSimilarity"] * 100,
                dataType=acc["DataType"] * 100,
                infoOmitted=acc["InfoOmitted"] * 100,
                fieldLength=acc["FieldLength"] * 100
            ))
        overall_result = AccuracyResult(
            accuracyRate=overall["Accuracy"] * 100,
            descriptionSimilarity=overall["DescriptionSimilarity"] * 100,
            mimosaSimilarity=overall["MimosaSimilarity"] * 100,
            sapSimilarity=overall["SAPSimilarity"] * 100,
            dataType=overall["DataType"] * 100,
            infoOmitted=overall["InfoOmitted"] * 100,
            fieldLength=overall["FieldLength"] * 100
        )
        return {"overall": overall_result, "singlePairAccuracydetails": singlePairAccuracydetails}      

