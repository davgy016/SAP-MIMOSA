import pytest

from ValidationAndMapping.Accuracy import DescriptionSimilarity, FieldLength, Accuracy
from ValidationAndMapping.Accuracy.MimosaChecker import MimosaChecker
from ValidationAndMapping.Models import FieldMapping, MappingEntry, Mapping
from ValidationAndMapping.ScoreManager import ScoreManager



@pytest.fixture
def sampleMapping():
    # First mapping entry - Work Order
    sapField1 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK",
        fieldName="AUFNR",
        description="Work Order Digit",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="12"
    )

    mimosaField1 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="WorkOrder.WorkOrderID",
        description="Work Order Number",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="15"
    )

    # Second mapping entry - Equipment
    sapField2 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK",
        fieldName="EQUNR",
        description="Equipment Number",
        dataType="CHAR(18)",
        notes="Unique identifier for equipment in SAP PM",
        fieldLength="18"
    )

    mimosaField2 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="Asset.AssetID",
        description="Asset Identifier",
        dataType="CHAR(18)",
        notes="Unique identifier for asset in MIMOSA",
        fieldLength="18"
    )

    # Third mapping entry - Maintenance Plan
    sapField3 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK",
        fieldName="PLNNR",
        description="Maintenance Plan Number",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan",
        fieldLength="12"
    )

    mimosaField3 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="AUFK",
        fieldName="MaintenancePlan.PlanID",
        description="Maintenance Plan Identifier",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan in MIMOSA",
        fieldLength="12"
    )
    # Third mapping entry - Maintenance Plan
    sapField4 = FieldMapping(
        platform="SAP PM",
        entityName="NOT REAL",
        fieldName="PLNNR",
        description="Maintenance Plan Number",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan",
        fieldLength="12"
    )

    mimosaField4 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="AUFK",
        fieldName="MaintenancePlan.PlanID",
        description="Maintenance Plan Identifier",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan in MIMOSA",
        fieldLength="12"
    )
    sapField5 = FieldMapping(
        platform="SAP PM",
        entityName="NOT REAL",
        fieldName="EQUNR",
        description="Equipment Number",
        dataType="CHAR(18)",
        notes="Unique identifier for equipment in SAP PM",
        fieldLength="18"
    )

    mimosaField5 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="Asset.AssetID",
        description="Asset Identifier",
        dataType="CHAR(18)",
        notes="Unique identifier for asset in MIMOSA",
        fieldLength="18"
    )
    sapField6 = FieldMapping(
        platform="SAP PM",
        entityName="NOT REAL",
        fieldName="EQU",
        description="Equipment Number",
        dataType="CHAR(18)",
        notes="Unique identifier for equipment in SAP PM",
        fieldLength="18"
    )

    mimosaField6 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="Asset.AssetID",
        description="Asset Identifier",
        dataType="CHAR(18)",
        notes="Unique identifier for asset in MIMOSA",
        fieldLength="18"
    )

    mappingEntries = [
        MappingEntry(sap=sapField1, mimosa=mimosaField1),
        MappingEntry(sap=sapField2, mimosa=mimosaField2),
        MappingEntry(sap=sapField3, mimosa=mimosaField3),
        MappingEntry(sap=sapField4, mimosa=mimosaField4),
        MappingEntry(sap=sapField5, mimosa=mimosaField5),
        MappingEntry(sap=sapField6, mimosa=mimosaField6)
    ]

    mapping = Mapping(
        mapID="001",
        LLMType="Go",
        mappings=mappingEntries
    )

    return mapping

def test_descriptionSimilarity(sampleMapping):
    sim = DescriptionSimilarity()
    score = sim.score(mapping=sampleMapping.mappings[0])
    print("Description Similarity score:", score)
    assert score == pytest.approx(0.9, abs=0.2), "Descriptions are not similar enough"

def test_accuracy(sampleMapping):
    acc = Accuracy()
    score = acc.calculateAccuracy(sampleMapping.mappings[0])
    print("Accuracy Score:",score)
    assert score["Accuracy"] == pytest.approx(0.6, abs=0.2), "Mappings are not similar enough"

def test_scoreManagerScoreOutput(sampleMapping):
    sm = ScoreManager()
    score = sm.scoreOutputWithDetails(sampleMapping.mappings)
    print("Score manager output", score)
    assert score["overall"].accuracyRate == pytest.approx(0.6, abs=0.2), "Mappings are not similar enough"



