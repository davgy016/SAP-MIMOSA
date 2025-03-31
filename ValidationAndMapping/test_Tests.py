import pytest

from Accuracy import DescriptionSimilarity
import Mapping

#tests for description similarity
@pytest.fixture
def sample_mapping():
    # create a sample mapping list
    mapping = Mapping.Mapping(
        sap_fieldName="AUKUS",
        sap_fieldLength=10,
        sap_dataType="String",
        sap_description="This sentence is kinda cool",
        mimosa_fieldName="AUKUS_MIM",
        mimosa_fieldLength=10,
        mimosa_dataType="String",
        mimosa_description="This sentence is kinda cool"
    )    
    return [mapping]

def test_descriptionSimilarity(sample_mapping):
    sim = DescriptionSimilarity()
    score = sim.score(mappings=sample_mapping)
    assert score == pytest.approx(0.8, abs=0.2), "Descriptions are not similar"
