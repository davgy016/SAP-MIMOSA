from ValidationAndMapping.Accuracy.SapValidator import SapValidator
from ValidationAndMapping.Models import Mapping, MappingEntry, FieldMapping

def make_entry(label, dtype, length):
    sap = FieldMapping(
        platform="SAP PM", entityName="WorkOrder",
        fieldName=label, description="…",
        dataType=dtype, notes="", fieldLength=str(length)
    )
    mimosa = sap.copy(deep=True)  # not used here
    return MappingEntry(sap=sap, mimosa=mimosa)

def test_sap_doc_validator():
    # assuming your SAPdata.json contains QMNUM as CHAR(12) length 12
    m_good = Mapping(mapID="1", LLMType="x", mappings=[make_entry("QMNUM","CHAR(12)",12)])
    m_bad  = Mapping(mapID="2", LLMType="x", mappings=[make_entry("FAKE","CHAR(5)",5)])

    assert SapValidator.score(m_good) == 1.0
    assert SapValidator.score(m_bad)  == 0.0