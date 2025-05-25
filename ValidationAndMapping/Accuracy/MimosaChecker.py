#Mimosa similarity compares the mimosa side of the mapping to to the schema to see if it is a valid field.

from ..Models import FieldMapping, FieldState, FieldCheck
import xml.etree.ElementTree as ET
import os

# class FieldState(Enum):
#     CORRECT = "correct"
#     INCORRECT = "incorrect"
#     NARF = "not a real field"

# class FieldCheck(BaseModel):
#     entityName: FieldState
#     fieldName: FieldState
#     description: FieldState
#     dataType: FieldState
#     fieldLength: FieldState

# class FieldMapping(BaseModel):
#     platform: str
#     entityName: str
#     fieldName: str
#     description: str
#     dataType: str
#     notes: str
#     fieldLength: str


class MimosaChecker:
    def checkField(self, field: FieldMapping) -> FieldCheck:
        #clean each field
        field.entityName = field.entityName.replace(" ","").strip()
        field.fieldName = field.fieldName.replace(" ","").strip()
        field.description = field.description.strip()
        field.dataType = field.dataType.replace(" ","").strip()


        self.counter = 0
        fieldCheck = FieldCheck()
        if self._getRoot() == False:
            return fieldCheck

        # look for entity name 
        fieldCheck.entityName = FieldState.NARF
        for entity in self.root:
            if field.entityName == entity.get("name"):
                fieldCheck.entityName = FieldState.CORRECT
                # if found look for field names
                try:
                    foundField = self._findWithName(self.root,field.fieldName)[0]
                except IndexError as e:
                    print("Couldn't find a field",e)
                    foundField = None
                print("foundField",foundField)
                print(self.counter)
                if foundField == None:
                    fieldCheck.fieldName = FieldState.NARF
                    fieldCheck.dataType = FieldState.NARF
                    fieldCheck.description = FieldState.NARF
                    fieldCheck.fieldLength = FieldState.NARF
                else:
                    fieldCheck.fieldName = FieldState.CORRECT

                    #check the data type
                    if self._checkDataType(foundField,field.dataType):
                        fieldCheck.dataType = FieldState.CORRECT
                    else:
                        fieldCheck.dataType = FieldState.INCORRECT

                    #there are no restrictions on field length so will always be correct
                    fieldCheck.fieldLength = FieldState.CORRECT

                    #check field description
                    if self._checkDescription(foundField, field.description):
                        fieldCheck.description = FieldState.CORRECT
                    else:
                        fieldCheck.description = FieldState.INCORRECT


        return fieldCheck

    def _getRoot(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, '..', 'Data', 'mimosaSchema.xsd')

        try:
            tree = ET.parse(schema_path)
            self.root = tree.getroot()
            self.xsd_namespace = "{http://www.w3.org/2001/XMLSchema}"

            return True
        except FileNotFoundError:
            print("Mimosa schema file not found")
            return False
        except ET.ParseError as e:
            print(f"Not able to parse mimosa schema: {e}")
            return False
    
    def _findWithName(self, root, name):
        self.counter += 1
        foundField = []
        for child in root:
            if child.get("name") == name:
                foundField.append(child)
            foundField.extend(self._findWithName(child, name))
        return foundField
    
    def _findAnnotation(self, element, name):
        for child in element:
            if child.tag == self.xsd_namespace + "annotation":
                try:
                    if element.get("name") == name:
                        return child[0].text
                except TypeError:
                    pass
            else:
                text = self._findAnnotation(child, name)
                if text is not None:
                    return text
        return None

    
    def _checkDataType(self, element, expected):
        if expected in element.get("type"):
            return True
        else:
            return False
        
    def _checkDescription(self, element, expected):
        """
        Return True if the schema’s annotation for this element
        contains the expected description (case-insensitive).
        """
        annotation = self._findAnnotation(self.root, element.get("name"))
        if not annotation:
            return False

        # compare case-insensitive, allow substring match
        return expected.strip().lower() in annotation.strip().lower()