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
        fieldName="PartNumber",
        description="Manufacturer's Part Number",
        dataType="cct:TextType",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="15"
    )

    mapping_entry = MappingEntry(sap=sap_field, mimosa=mimosa_field)

    mapping = Mapping(
        mapID="001",
        LLMType="Go",
        mappings=[mapping_entry]
    )

    return [mapping]

def test_mimosaChecker(sample_mapping):
    mc = MimosaChecker()
    fieldCheck = mc.checkField(sample_mapping[0].mappings[0].mimosa)
    print("EnityName",fieldCheck.entityName,"FieldName",fieldCheck.fieldName,"Description",fieldCheck.description,"DataType",fieldCheck.dataType,"FieldLength",fieldCheck.fieldLength)


