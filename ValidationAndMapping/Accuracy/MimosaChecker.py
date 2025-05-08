from ..Models import FieldMapping, FieldState, FieldCheck
import xml.etree.ElementTree as ET
import os


# class FieldCheck(BaseModel):
#     entityName: FieldState
#     fieldName: FieldState
#     description: FieldState
#     dataType: FieldState
#     fieldLength: FieldState

class MimosaChecker:
    def checkField(self, field: FieldMapping) -> FieldCheck:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, '..', 'Data', 'mimosaSchema.xsd')
        
        try:
            tree = ET.parse(schema_path)
            root = tree.getroot()
            xsd_namespace = "{http://www.w3.org/2001/XMLSchema}"

            for complex_type in root.findall(f'.//{xsd_namespace}complexType'):
                if complex_type.get('abstract') == "true":
                    print(f"Found complexType: {complex_type.get('name') or complex_type.tag}")
        except FileNotFoundError:
            print("Mimosa schema file not found")
        except ET.ParseError as e:
            print(f"Not able to parse mimosa schema: {e}")

        return None
    


