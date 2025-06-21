import pytest

from ValidationAndMapping.Accuracy import DescriptionSimilarity, FieldLength, Accuracy
from ValidationAndMapping.Accuracy.MimosaChecker import MimosaChecker
from ValidationAndMapping.Models import FieldMapping, MappingEntry, Mapping
from ValidationAndMapping.ScoreManager import ScoreManager


@pytest.fixture
def sampleMapping():
    sapField = FieldMapping(
        platform="SAP PM",
        entityName="Equipment",
        fieldName="AUFNR",
        description="Work Order Digit",
        dataType="CHAR(12)",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="12"
    )

    mimosaField = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="Asset",
        fieldName="PartNumber",
        description="Manufacturer's Part Number",
        dataType="cct:TextType",
        notes="Primary identifier for the work order in SAP PM",
        fieldLength="15"
    )

    mappingEntry = MappingEntry(sap=sapField, mimosa=mimosaField)

    mapping = Mapping(
        mapID="001",
        LLMType="Go",
        mappings=[mappingEntry]
    )

    return [mapping]

def test_mimosaChecker(sampleMapping):
    mc = MimosaChecker()
    fieldCheck = mc.checkField(sampleMapping[0].mappings[0].mimosa)
    print("EnityName",fieldCheck.entityName,"FieldName",fieldCheck.fieldName,"Description",fieldCheck.description,"DataType",fieldCheck.dataType,"FieldLength",fieldCheck.fieldLength)


