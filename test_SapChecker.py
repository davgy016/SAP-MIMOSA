# tests/test_sapchecker_entities.py
import pytest
from ValidationAndMapping.Accuracy.SAPChecker import SAPChecker
from ValidationAndMapping.Models import FieldMapping, FieldState

@pytest.fixture(scope="module")
def checker():
    return SAPChecker()

def test_normaliseStripsParentheses(checker):
    # simulate exactly what Excel gives you
    rawName = "AUFK (OrderMaster)"
    normalised = checker.normaliseTable(rawName)
    assert normalised == "AUFK"

    rawName2 = "   afih   (MaintenanceOrderHeader)  "
    assert checker.normaliseTable(rawName2) == "AFIH"

@pytest.mark.parametrize("entityIn,expectedTable", [
    ("AUFK (OrderMaster)", "AUFK"),
    ("AFIH (MaintenanceOrderHeader)", "AFIH"),
])
def test_entitynameAliasAndEntityCorrect(entityIn, expectedTable, checker):
    """
    If JSON had no top-level TableName but fields listed CheckTable=expectedTable,
    then incoming entityName=entityIn should still be recognized.
    """
    # pick a field we know lives in that table via CheckTable in sapSchema.json
    fm = FieldMapping(
        platform    = "SAP PM",
        entityName  = entityIn,
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

def test_unknownEntityRemainsIncorrect(checker):
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
