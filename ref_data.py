#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
###


import os
from lxml import etree
from data import Declaracion


class RefData:

    tree = None
    parser  = None

    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True, encoding='utf8')    
        self.tree = etree.parse(os.path.join('XML','DtsRfr.xml'), self.parser)

    def get_version_dimm(self):
        root = self.tree.getroot()
        return root.attrib.get('version')


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
            if codigo is not None and nombre is not None:
                list.append([codigo.text, nombre.text])

        return list


    def get_data_list_2(self, code):
        """ Retorna la lista de nodos (codigo, descripcion) """
        list = []
        nodes = self.get_xpath_nodes(code)
    
        if nodes is None:
            return None
    
        for node in nodes:
            codigo = node.find('codigo')
            desc = node.find('descripcion')
            if codigo is not None and desc is not None:
                list.append([codigo.text, desc.text])

        return list


    def get_datos_formularios(self):
        list = []
        nodes = self.get_xpath_nodes(5)
    
        if nodes is None:
            return None

        for node in nodes:
            periodicidad = node.attrib.get('periodicidad')
            nombre = node.attrib.get('nombre')
            version = node.attrib.get('version')
            desc = node.attrib.get('descripcion_impuesto')
            list.append([version, nombre + ' - '  + desc])

        return list


    def get_codigo_version_formulario(self, nombre, periodicidad):
        nodes = self.tree.findall('datosFormulariosVersiones/formularioVersion[@nombre="'+nombre+'"]')

        for node in nodes:
            if node.attrib.get('periodicidad') == periodicidad:
                return node.attrib.get('versionVigente')
        return None


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


    def get_nombre_formulario(self, version):
        nodes = self.get_xpath_nodes(5)
    
        if nodes is None:
            return None

        for node in nodes:
            nombre = node.attrib.get('nombre')
            codigo = node.attrib.get('version')
            if codigo == version:
                return nombre
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


    def get_ori_sus(self):
        # FIXME en el XML del SRI el valor de ORI, SUS es 0,1, pero valida como "O", "S"
        list = []
        nodes = self.get_xpath_nodes(50)
    
        if nodes is None:
            return None
    
        for node in nodes:
            nombre = node.find('nombre')
            code = nombre.text[0]
            list.append([code, nombre.text])

        return list

    
    def get_objeto_declaracion(self, codigo_version):
        nodes = self.get_xpath_nodes(10)

        if nodes is None:
            return None

        for node in nodes:
            nombre = node.attrib.get('nombre')
            periodicidad = node.attrib.get('periodicidad')
            version = node.attrib.get('versionVigente')
            if version == codigo_version:
                declaracion = Declaracion()
                declaracion.set_periodicidad(periodicidad)
                formulario = self.tree.find('datosFormularios/formulario[@nombre="'+nombre+'"]')
                declaracion.set_codigo_version(codigo_version) # se obtiene de <datosFormularios codigo="10">
                declaracion.set_version(formulario.attrib.get('version')) # codigo version para validaciones/calculos
                alias = nombre.replace("FORMULARIO ", "")
                declaracion.set_alias_formulario(alias)
                return declaracion
        return None
    


# tests
if __name__ == '__main__':
    ref = RefData()
    print ref.get_version_dimm()
    #print ref.get_mes_por_codigo('5')
    #print ref.get_semestre_por_codigo('06')
    #print ref.get_ori_sus()
    #declaracion = ref.get_objeto_declaracion('04200902')
    #print 'widgets', declaracion.get_codigo_version()
    #print 'calculos', declaracion.get_version()
    #print 'periodicidad', declaracion.get_periodicidad()
    









