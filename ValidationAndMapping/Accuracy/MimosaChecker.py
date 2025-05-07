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
        fieldCheck = FieldCheck()
        foundElement = None
        if self._getRoot() == False:
            return fieldCheck
        
        # look for entity name 
        fieldCheck.entityName = FieldState.NARF
        for entity in self.root:
            if field.entityName == entity.get("name"):
                fieldCheck.entityName = FieldState.CORRECT
                # if found 
                for element in self._find_all_recursive(entity, f"{self.xsd_namespace}element"):
                    #   parse all elements of type iterating through parent types
                    #   check if field name is in elements
                    if field.fieldName in element.get("name"):
                        fieldCheck.fieldName = FieldState.CORRECT
                            # if fieldName found
                        # check description 
                        # check data type
                        # check fieldLength
                        foundElement = element
                        break

                # if not field name found look for one in the whole thing
                if fieldCheck.fieldName == FieldState.UNCHECKED:
                    fieldCheck.fieldName = FieldState.NARF
                    for element in self._find_all_recursive(self.root, f"{self.xsd_namespace}element"):
                        if field.fieldName in element.get("name"):
                            fieldCheck.fieldName = FieldState.INCORRECT
                            foundElement = element
                            break

        #if field was found check types
        if foundElement is not None:
            print(foundElement.tag)

        #if no field found dataType, description and fieldLength can't be checked
        else:
            fieldCheck.dataType = FieldState.NARF
            fieldCheck.description = FieldState.NARF
            fieldCheck.fieldLength = FieldState.NARF


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
    

    def _find_all_recursive(self, element, tag):
        """
        Recursively finds all elements with the specified tag within the given element
        and its descendants.

        Args:
            element: The root element to start the search from.
            tag: The tag name to search for.

        Returns:
            A list of elements matching the tag.
        """
        results = []
        for child in element:
            if child.tag == tag:
                results.append(child)
            results.extend(self._find_all_recursive(child, tag))
        return results