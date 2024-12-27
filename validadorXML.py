import xmlschema
from lxml import etree

def validar_xml(xml, esquema):
    if isinstance(xml, str):
        # Convert the string to an XML element
        xml = etree.fromstring(xml)
    
    schema = xmlschema.XMLSchema(esquema)  # Adicione o caminho para o seu arquivo XSD
    xml_string = etree.tostring(xml)
    if schema.is_valid(xml_string):
        print("XML válido.")
    else:
        print("XML inválido.", schema.validate(xml_string))