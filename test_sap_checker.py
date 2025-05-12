# tests/test_sap_checker.py

import pytest
from ValidationAndMapping.Accuracy.SAPChecker import SAPChecker
from ValidationAndMapping.Models import FieldMapping, FieldCheck, FieldState

@pytest.fixture(scope="module")
def checker():
    # default constructor uses Data/sapSchema.json
    return SAPChecker()

def make_field(platform, entity, field, desc, dtype, length):
    return FieldMapping(
        platform   = platform,
        entityName = entity,
        fieldName  = field,
        description= desc,
        dataType   = dtype,
        notes      = "",
        fieldLength= str(length)
    )

def test_check_existing_field_correct(checker):
    # Using real table/field from sapSchema.json:
    # TableName = "EAMSC_JOB_OPTION", Field = "MANDT", Description="Client", SAP Type="CLNT", Length=3
    fm = make_field(
        "SAP PM", 
        "EAMSC_JOB_OPTION", 
        "MANDT",
        "Client", 
        "CLNT", 
        3
    )
    fc: FieldCheck = checker.checkField(fm)

    # All aspects should be correct
    assert fc.entityName   == FieldState.CORRECT
    assert fc.fieldName    == FieldState.CORRECT
    assert fc.dataType     == FieldState.CORRECT
    assert fc.fieldLength  == FieldState.CORRECT
    assert fc.description  == FieldState.CORRECT

def test_check_existing_field_mismatch(checker):
    # Same table/field but wrong metadata should flag the incorrect parts:
    fm = make_field(
        "SAP PM",
        "EAMSC_JOB_OPTION",
        "MANDT",
        "Wrong Description",  # bad description
        "CHAR",               # wrong type
        10                    # wrong length
    )
    fc = checker.checkField(fm)

    # Field exists, so entityName & fieldName still correct
    assert fc.entityName   == FieldState.CORRECT
    assert fc.fieldName    == FieldState.CORRECT

    # The metadata should be marked incorrect
    assert fc.dataType     == FieldState.INCORRECT
    assert fc.fieldLength  == FieldState.INCORRECT
    assert fc.description  == FieldState.INCORRECT
