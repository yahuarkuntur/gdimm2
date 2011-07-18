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
            periodicidad = node.attrib.get('periodicidad')
            nombre = node.attrib.get('nombre')
            codigo = node.attrib.get('version')
            desc = node.attrib.get('descripcion_impuesto')
            list.append([codigo, nombre + ' .- '  + desc])

        return list


    def get_periodicidad(self, version):
        nodes = self.get_xpath_nodes(5)
    
        if nodes is None:
            return None

        for node in nodes:
            periodicidad = node.attrib.get('periodicidad')
            codigo = node.attrib.get('version')
            if codigo == version:
                return periodicidad
        return None


    def get_mes_por_codigo(self, code):
        nodes = self.tree.find('/*[@codigo="20"]')
    
        if nodes is None:
            return None

        for node in nodes:
            codigo = node.find('codigo')
            nombre = node.find('nombre')
            if codigo.text == code:
                return nombre.text
        return None

    
    def get_semestre_por_codigo(self, code):
        nodes = self.tree.find('/*[@codigo="40"]')
    
        if nodes is None:
            return None

        for node in nodes:
            codigo = node.find('codigo')
            nombre = node.find('nombre')
            if codigo.text == code:
                return nombre.text
        return None



# tests
if __name__ == '__main__':
    ref = RefData()

    print ref.get_mes_por_codigo('5')
    print ref.get_semestre_por_codigo('06')









