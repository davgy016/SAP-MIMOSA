import pytest

from ValidationAndMapping.Accuracy import DescriptionSimilarity, FieldLength, Accuracy
from ValidationAndMapping.Accuracy.MimosaChecker import MimosaChecker
from ValidationAndMapping.Models import FieldMapping, MappingEntry, Mapping
from ValidationAndMapping.ScoreManager import ScoreManager


@pytest.fixture
def sample_mapping():
    sap_field = FieldMapping(
        platform="SAP PM",
        entityName="Equipment",
        fieldName="AUFNR",
        description="Work Order Digit",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="12"
    )

    mimosa_field = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="WorkOrder.WorkOrderID",
        description="Work Order Number",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="15"
    )

    mapping_entry = MappingEntry(sap=sap_field, mimosa=mimosa_field)

    mapping = Mapping(
        mapID="001",
        LLMType="Go",
        mappings=[mapping_entry]
    )

    return mapping


def test_descriptionSimilarity(sample_mapping):
    sim = DescriptionSimilarity()
    score = sim.score(mapping=sample_mapping.mappings[0])
    print("Description Similarity score:", score)
    assert score == pytest.approx(0.9, abs=0.2), "Descriptions are not similar enough"

def test_fieldLength(sample_mapping):
    fl = FieldLength()
    score = fl.score(mapping=sample_mapping.mappings[0])
    print("Field Length score:", score)
    assert score == pytest.approx(0.9, abs=0.2), "Field Lengths are not similar enough"

def test_accuracy(sample_mapping):
    acc = Accuracy()
    score = acc.calculateAccuracy(mapping=sample_mapping.mappings[0])
    print("Accuracy Score:",score)
    assert score["Accuracy"] == pytest.approx(0.6, abs=0.2), "Mappings are not similar enough"

def test_scoreManager_scoreOutput(sample_mapping):
    sm = ScoreManager()
    score = sm.scoreOutput(sample_mapping)
    print("Score manager output", score)
    assert score["Accuracy"] == pytest.approx(0.6, abs=0.2), "Mappings are not similar enough"



