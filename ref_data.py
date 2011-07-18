import os
from lxml import etree


class RefData:

    tree = None
    parser  = None

    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True, encoding='utf8')    
        self.tree = etree.parse(os.path.join('XML','DtsRfr.xml'), self.parser)


    def get_xpath_nodes(self, code):
        return self.tree.find('/*[@codigo="'+str(code)+'"]')


    def get_data_list(self, code):
        list = []
        nodes = self.get_xpath_nodes(code)
    
        if nodes is None:
            return None
    
        for node in nodes:
            codigo = node.find('codigo')
            nombre = node.find('nombre')
            list.append([codigo.text, nombre.text])

        return list


    def get_datos_formularios(self):
        list = []
        nodes = self.get_xpath_nodes(5)
    
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


    def get_periodicidad(self, version):
        nodes = self.get_xpath_nodes(5)
    
        if nodes is None:
            return None
   
        # TODO use XPath?
        for node in nodes:
            if node.attrib.get('version') == version :
                return node.attrib.get('periodicidad')

        return None











