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












