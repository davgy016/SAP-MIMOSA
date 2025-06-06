import pytest

from ValidationAndMapping.Accuracy import DescriptionSimilarity, FieldLength, Accuracy
from ValidationAndMapping.Accuracy.MimosaChecker import MimosaChecker
from ValidationAndMapping.Models import FieldMapping, MappingEntry, Mapping
from ValidationAndMapping.ScoreManager import ScoreManager



@pytest.fixture
def sample_mapping():
    # First mapping entry - Work Order
    sap_field1 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK",
        fieldName="AUFNR",
        description="Work Order Digit",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="12"
    )

    mimosa_field1 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="WorkOrder.WorkOrderID",
        description="Work Order Number",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="15"
    )

    # Second mapping entry - Equipment
    sap_field2 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK",
        fieldName="EQUNR",
        description="Equipment Number",
        dataType="CHAR(18)",
        notes="Unique identifier for equipment in SAP PM",
        fieldLength="18"
    )

    mimosa_field2 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="Asset.AssetID",
        description="Asset Identifier",
        dataType="CHAR(18)",
        notes="Unique identifier for asset in MIMOSA",
        fieldLength="18"
    )

    # Third mapping entry - Maintenance Plan
    sap_field3 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK",
        fieldName="PLNNR",
        description="Maintenance Plan Number",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan",
        fieldLength="12"
    )

    mimosa_field3 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="AUFK",
        fieldName="MaintenancePlan.PlanID",
        description="Maintenance Plan Identifier",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan in MIMOSA",
        fieldLength="12"
    )
    # Third mapping entry - Maintenance Plan
    sap_field4 = FieldMapping(
        platform="SAP PM",
        entityName="NOT REAL",
        fieldName="PLNNR",
        description="Maintenance Plan Number",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan",
        fieldLength="12"
    )

    mimosa_field4 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="AUFK",
        fieldName="MaintenancePlan.PlanID",
        description="Maintenance Plan Identifier",
        dataType="CHAR(12)",
        notes="Identifier for maintenance plan in MIMOSA",
        fieldLength="12"
    )
    sap_field5 = FieldMapping(
        platform="SAP PM",
        entityName="NOT REAL",
        fieldName="EQUNR",
        description="Equipment Number",
        dataType="CHAR(18)",
        notes="Unique identifier for equipment in SAP PM",
        fieldLength="18"
    )

    mimosa_field5 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="Asset.AssetID",
        description="Asset Identifier",
        dataType="CHAR(18)",
        notes="Unique identifier for asset in MIMOSA",
        fieldLength="18"
    )
    sap_field6 = FieldMapping(
        platform="SAP PM",
        entityName="NOT REAL",
        fieldName="EQU",
        description="Equipment Number",
        dataType="CHAR(18)",
        notes="Unique identifier for equipment in SAP PM",
        fieldLength="18"
    )

    mimosa_field6 = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="Asset.AssetID",
        description="Asset Identifier",
        dataType="CHAR(18)",
        notes="Unique identifier for asset in MIMOSA",
        fieldLength="18"
    )

    mapping_entries = [
        MappingEntry(sap=sap_field1, mimosa=mimosa_field1),
        MappingEntry(sap=sap_field2, mimosa=mimosa_field2),
        MappingEntry(sap=sap_field3, mimosa=mimosa_field3),
        MappingEntry(sap=sap_field4, mimosa=mimosa_field4),
        MappingEntry(sap=sap_field5, mimosa=mimosa_field5),
        MappingEntry(sap=sap_field6, mimosa=mimosa_field6)
    ]

    mapping = Mapping(
        mapID="001",
        LLMType="Go",
        mappings=mapping_entries
    )

    return mapping

def test_descriptionSimilarity(sample_mapping):
    sim = DescriptionSimilarity()
    score = sim.score(mapping=sample_mapping.mappings[0])
    print("Description Similarity score:", score)
    assert score == pytest.approx(0.9, abs=0.2), "Descriptions are not similar enough"

def test_accuracy(sample_mapping):
    acc = Accuracy()
    score = acc.calculateAccuracy(sample_mapping.mappings[0])
    print("Accuracy Score:",score)
    assert score["Accuracy"] == pytest.approx(0.6, abs=0.2), "Mappings are not similar enough"

def test_scoreManager_scoreOutput(sample_mapping):
    sm = ScoreManager()
    score = sm.scoreOutputWithDetails(sample_mapping.mappings)
    print("Score manager output", score)
    assert score["Overall"] == pytest.approx(0.6, abs=0.2), "Mappings are not similar enough"



