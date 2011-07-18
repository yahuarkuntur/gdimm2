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
            version_formulario = node.attrib.get('version_formulario')
            #codigo = node.attrib.get('version')
            codigo = node.attrib.get('nombre')
            desc = node.attrib.get('descripcion_impuesto')
            list.append([codigo, nombre + ' .- '  + desc])

        return list


    def get_periodicidad(self, nombre):
        nodes = self.tree.findall('datosFormulariosVersiones/formularioVersion[@nombre="'+nombre+'"]')

        list = []

        for node in nodes:
            p = node.attrib.get('periodicidad')
            if p not in list:
                list.append(p)
        return list


    def get_codigo_version_formulario(self, nombre, periodicidad):
        nodes = self.tree.findall('datosFormulariosVersiones/formularioVersion[@nombre="'+nombre+'"]')

        for node in nodes:
            if node.attrib.get('periodicidad') == periodicidad:
                return node.attrib.get('versionVigente')
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

    #print ref.get_periodicidad('FORMULARIO 104A')
    #print ref.get_periodicidad('FORMULARIO 104')
    #print ref.get_periodicidad('FORMULARIO 101')
    #print ref.get_periodicidad('FORMULARIO 102')
    #print ref.get_periodicidad('FORMULARIO 102A')
    #print ref.get_periodicidad('FORMULARIO 105')

    #print ref.get_codigo_version_formulario('FORMULARIO 104A', 'MENSUAL')
    #print ref.get_codigo_version_formulario('FORMULARIO 104A', 'SEMESTRAL')

    print ref.get_mes_por_codigo('5')
    print ref.get_semestre_por_codigo('06')









