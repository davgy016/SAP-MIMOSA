import pytest
from ValidationAndMapping.Accuracy.InfoOmitted import InfoOmitted
from ValidationAndMapping.Models import FieldMapping, MappingEntry, Mapping


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

@pytest.fixture
def info_omitted():
    return InfoOmitted()

def test_info_omitted_initialization(info_omitted):
    """Test that InfoOmitted initializes correctly with schema data"""
    assert info_omitted.schema is not None
    assert isinstance(info_omitted.schema, dict)
    assert isinstance(info_omitted.any_field_index, dict)

def test_score_overall_empty_mapping(info_omitted):
    """Test score_overall with empty mapping list"""
    assert info_omitted.score_overall([]) == 0

def test_score_overall_single_entity(info_omitted, sample_mapping):
    """Test score_overall with a single entity mapping"""
    # Get the first mapping entry from the sample mapping
    mapping_entry = sample_mapping.mappings[0]
    score = info_omitted.score_overall([mapping_entry])
    print(f'Test single overall{score}')
    # Score should be between 0 and 1
    assert 0 <= score <= 1

def test_score_single_empty_mappings(info_omitted, sample_mapping):
    """Test score_single with empty mappings list"""
    mapping_entry = sample_mapping.mappings[0]
    score = info_omitted.score_single(mapping_entry, [])
    
    assert score == 0

def test_score_single_same_entity(info_omitted, sample_mapping):
    """Test score_single with multiple mappings of same entity"""
    mapping_entry = sample_mapping.mappings[0]
    # Create a duplicate mapping for the same entity
    duplicate_entry = MappingEntry(
        sap=mapping_entry.sap,
        mimosa=mapping_entry.mimosa
    )
    score = info_omitted.score_single(mapping_entry, [mapping_entry, duplicate_entry])
    print(f'Test duplicate {score}')

    
    assert 0 <= score <= 1

def test_score_single_different_entity(info_omitted, sample_mapping):
    """Test score_single with mappings of different entities"""
    mapping_entry = sample_mapping.mappings[0]
    # Create a mapping for a different entity
    different_sap = FieldMapping(
        platform="SAP PM",
        entityName="ALM_ME_STOBJT",
        fieldName="FIELD1",
        description="Test Field",
        dataType="CHAR(10)",
        notes="Test notes",
        fieldLength="10"
    )
    different_mimosa = FieldMapping(
        platform="MIMOSA CCOM",
        entityName="DifferentAsset",
        fieldName="Field1",
        description="Test Field",
        dataType="CHAR(10)",
        notes="Test notes",
        fieldLength="10"
    )
    different_entry = MappingEntry(sap=different_sap, mimosa=different_mimosa)
    
    score = info_omitted.score_overall([mapping_entry, different_entry])
    print(f'Test 2 entities {score}')

    
    assert 0 <= score <= 1

def test_score_overall(info_omitted, sample_mapping):
    score = info_omitted.score_overall(sample_mapping.mappings)

    print(f'Test overall {score}')
    assert 0 <= score <= 1

def test_score_overall_with_duplicate(info_omitted, sample_mapping):
    mappings_with_duplicate = sample_mapping.mappings

    mappings_with_duplicate.append(sample_mapping.mappings[0])
    score = info_omitted.score_overall(mappings_with_duplicate)

    print(f'Test overall with a duplicate {score}')
    assert 0 <= score <= 1