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
        sap_description="SAP Field Example",
        mimosa_fieldName="AUKUS_MIM",
        mimosa_fieldLength=10,
        mimosa_dataType="String",
        mimosa_description="MIMOSA Field Example"
    )    
    return [mapping]

def test_descriptionSimilarity(sample_mapping):
    assert sample_mapping == DescriptionSimilarity.score(sample_mapping)
