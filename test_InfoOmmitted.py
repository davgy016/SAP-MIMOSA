import pytest
from ValidationAndMapping.Accuracy.InfoOmitted import InfoOmitted
from ValidationAndMapping.Models import FieldMapping, MappingEntry, Mapping


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
    sapField2 = FieldMapping(
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
    sapField3 = FieldMapping(
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
    sapField4 = FieldMapping(
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
    sapField5 = FieldMapping(
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
    sapField6 = FieldMapping(
        platform="SAP PM",
        entityName="AUFK (ORder number)",
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
        MappingEntry(sap=sapField1, mimosa=mimosa_field1),
        MappingEntry(sap=sapField2, mimosa=mimosa_field2),
        MappingEntry(sap=sapField3, mimosa=mimosa_field3),
        MappingEntry(sap=sapField4, mimosa=mimosa_field4),
        MappingEntry(sap=sapField5, mimosa=mimosa_field5),
        MappingEntry(sap=sapField6, mimosa=mimosa_field6)
    ]

    mapping = Mapping(
        mapID="001",
        LLMType="Go",
        mappings=mapping_entries
    )

    return mapping

@pytest.fixture
def infoOmitted():
    return InfoOmitted()

def test_infoOmittedInitialisation(infoOmitted):
    """Test that InfoOmitted initializes correctly with schema data"""
    assert infoOmitted.schema is not None
    assert isinstance(infoOmitted.schema, dict)
    assert isinstance(infoOmitted.anyFieldIndex, dict)

def test_scoreOverallEmptyMapping(infoOmitted):
    """Test scoreOverall with empty mapping list"""
    assert infoOmitted.scoreOverall([]) == 0

def test_scoreOverallSingleEntity(infoOmitted, sampleMapping):
    """Test scoreOverall with a single entity mapping"""
    # Get the first mapping entry from the sample mapping
    mappingEntry = sampleMapping.mappings[0]
    score = infoOmitted.scoreOverall([mappingEntry])
    print(f'Test single overall{score}')
    # Score should be between 0 and 1
    assert 0 <= score <= 1

def test_scoreSingleEmptyMappings(infoOmitted, sampleMapping):
    """Test scoreSingle with empty mappings list"""
    mappingEntry = sampleMapping.mappings[0]
    score = infoOmitted.scoreSingle(mappingEntry, [])
    
    assert score == 0

def test_scoreSingleSameEntity(infoOmitted, sampleMapping):
    """Test scoreSingle with multiple mappings of same entity"""
    mappingEntry = sampleMapping.mappings[0]
    # Create a duplicate mapping for the same entity
    duplicateEntry = MappingEntry(
        sap=mappingEntry.sap,
        mimosa=mappingEntry.mimosa
    )
    score = infoOmitted.scoreSingle(mappingEntry, [mappingEntry, duplicateEntry])
    print(f'Test duplicate {score}')

    
    assert 0 <= score <= 1

def test_scoreSingleDifferentEntity(infoOmitted, sampleMapping):
    """Test scoreSingle with mappings of different entities"""
    mappingEntry = sampleMapping.mappings[0]
    # Create a mapping for a different entity
    differentSap = FieldMapping(
        platform="SAP PM",
        entityName="ALM_ME_STOBJT",
        fieldName="FIELD1",
        description="Test Field",
        dataType="CHAR(10)",
        notes="Test notes",
        fieldLength="10"
    )
    differentMimosa = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="DifferentAsset",
        fieldName="Field1",
        description="Test Field",
        dataType="CHAR(10)",
        notes="Test notes",
        fieldLength="10"
    )
    differentEntry = MappingEntry(sap=differentSap, mimosa=differentMimosa)
    
    score = infoOmitted.scoreOverall([mappingEntry, differentEntry])
    print(f'Test 2 entities {score}')

    
    assert 0 <= score <= 1

def test_scoreOverall(infoOmitted, sampleMapping):
    score = infoOmitted.scoreOverall(sampleMapping.mappings)

    print(f'Test overall {score}')
    assert 0 <= score <= 1

def test_scoreOverallWithDuplicate(infoOmitted, sampleMapping):
    mappingsWithDuplicate = sampleMapping.mappings

    mappingsWithDuplicate.append(sampleMapping.mappings[0])
    score = infoOmitted.scoreOverall(mappingsWithDuplicate)

    print(f'Test overall with a duplicate {score}')
    assert 0 <= score <= 1