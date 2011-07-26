#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

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
            version = node.attrib.get('version')
            desc = node.attrib.get('descripcion_impuesto')
            list.append([version, nombre + ' .- '  + desc])

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
        # TODO en el XML del SRI el valor de ORI, SUS es 0,1, pero valida como "O", "S"
        list = []
        nodes = self.get_xpath_nodes(50)
    
        if nodes is None:
            return None
    
        for node in nodes:
            nombre = node.find('nombre')
            code = nombre.text[0]
            list.append([code, nombre.text])

        return list


# tests
if __name__ == '__main__':
    ref = RefData()

    print ref.get_mes_por_codigo('5')
    print ref.get_semestre_por_codigo('06')
    print ref.get_ori_sus()









