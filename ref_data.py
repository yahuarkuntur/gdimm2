import os
from lxml import etree


# TODO: create a singleton
def get_xpath_nodes(code):
    parser = etree.XMLParser(remove_comments=True, encoding='utf8')
    tree = etree.parse(os.path.join('XML','DtsRfr.xml'), parser)
    return tree.find('/*[@codigo="'+str(code)+'"]')



def get_data_list(code):
    list = []
    nodes = get_xpath_nodes(code)
    
    if nodes is None:
        return None
    
    for node in nodes:
        codigo = node.find('codigo')
        nombre = node.find('nombre')
        list.append([codigo.text, nombre.text])

    return list


def get_datos_formularios():
    list = []
    nodes = get_xpath_nodes(5)
    
    if nodes is None:
        return None

    for node in nodes:
        codigo = node.attrib.get('codigo')
        nombre = node.attrib.get('nombre')
        periodicidad = node.attrib.get('periodicidad')
        version = node.attrib.get('version')
        desc = node.attrib.get('descripcion_impuesto')
        list.append([version, nombre + ' - '  + desc])

    return list


def get_periodicidad(version):
    nodes = get_xpath_nodes(5)
    
    if nodes is None:
        return None
   
    # TODO use XPath?
    for node in nodes:
        if node.attrib.get('version') == version :
            return node.attrib.get('periodicidad')

    return None











