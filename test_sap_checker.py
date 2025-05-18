# tests/test_sapchecker_entities.py
import pytest
from ValidationAndMapping.Accuracy.SAPChecker import SAPChecker
from ValidationAndMapping.Models import FieldMapping, FieldState

@pytest.fixture(scope="module")
def checker():
    return SAPChecker()

def test_normalize_strips_parentheses(checker):
    # simulate exactly what Excel gives you
    raw_name = "AUFK (OrderMaster)"
    normalized = checker._normalize_table(raw_name)
    assert normalized == "AUFK"

    raw_name2 = "   afih   (MaintenanceOrderHeader)  "
    assert checker._normalize_table(raw_name2) == "AFIH"

@pytest.mark.parametrize("entity_in,expected_tbl", [
    ("AUFK (OrderMaster)", "AUFK"),
    ("AFIH (MaintenanceOrderHeader)", "AFIH"),
])
def test_entityname_alias_and_entity_correct(entity_in, expected_tbl, checker):
    """
    If JSON had no top-level TableName but fields listed CheckTable=expected_tbl,
    then incoming entityName=entity_in should still be recognized.
    """
    # pick a field we know lives in that table via CheckTable in sapSchema.json
    fm = FieldMapping(
        platform    = "SAP PM",
        entityName  = entity_in,
        fieldName   = "QMNUM",                # we know QMNUM → CheckTable=AUFK
        description = "Notification Number",
        dataType    = "CHAR(12)",
        notes       = "",
        fieldLength = "12"
    )
    fc = checker.checkField(fm)
    # entityName should now be CORRECT even though "AUFK" never appeared
    assert fc.entityName == FieldState.CORRECT
    # and because QMNUM is a real field, fieldName must be CORRECT as well
    assert fc.fieldName == FieldState.CORRECT

def test_unknown_entity_remains_incorrect(checker):
    fm = FieldMapping(
        platform    = "SAP PM",
        entityName  = "NONEXISTENT (FooBar)",
        fieldName   = "QMNUM",
        description = "Notification Number",
        dataType    = "CHAR(12)",
        notes       = "",
        fieldLength = "12"
    )
    fc = checker.checkField(fm)
    # should fall back to INCORRECT (or NARF) on entityName
    assert fc.entityName in (FieldState.INCORRECT, FieldState.NARF)
