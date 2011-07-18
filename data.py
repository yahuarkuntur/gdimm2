#!/usr/bin/env python
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
from exceptions import *


class Declaracion:
    _mes = None
    _anio = None
    #_tipo = None
    _periodicidad = None
    _formulario = None
    _contribuyente = None
    _anticipada = False
    _original   = '1'
    _sustituye  = ''
    _alias_formulario = ''
    
    def __init__(self):
        pass

    def set_mes(self, mes):
        self._mes = mes

    def set_anio(self, anio):
        self._anio = anio

    def set_tipo(self, tipo):
        self._tipo = tipo

    def set_periodicidad(self, periodicidad):
        self._periodicidad = periodicidad


    def set_formulario(self, formulario):
        self._formulario = formulario

    def set_contribuyente(self, contribuyente):
        self._contribuyente = contribuyente

    def set_anticipada(self, anticipada):
        self._anticipada = anticipada

    def set_original(self, original):
        self._original = original

    def set_sustituye(self, sustituye):
        self._sustituye = sustituye

    def set_alias_formulario(self, alias_formulario):
        self._alias_formulario = alias_formulario


    def get_mes(self):
        return self._mes

    def get_anio(self):
        return self._anio

    def get_tipo(self):
        return self._tipo

    def get_formulario(self):
        return self._formulario

    def get_contribuyente(self):
        return self._contribuyente

    def get_anticipada(self):
        return self._anticipada

    def get_original(self):
        return self._original

    def get_sustituye(self):
        return self._sustituye

    def get_alias_formulario(self):
        return self._alias_formulario

    def get_periodicidad(self):
        return self._periodicidad




class Contribuyente:
    _ruc = None
    _nombre = None
    _tipo_doc_representante = None
    _doc_representante = None
    
    def __init__(self):
        self._data = etree.Element("ruc", numero = "")
        self._nombre = etree.SubElement(self._data, "razon_social")
        self._tipo_doc_representante = etree.SubElement(self._data, "tipoDocRepLegal") ## C
        self._doc_representante = etree.SubElement(self._data, "identificacionRepLegal")
    
    def load(self, data):
        self._data = data
        
        for i in self._data:
            if i.tag == "razon_social":
                self._nombre = i
            elif i.tag == "tipoDocRepLegal":
                self._tipo_doc_representante = i
            elif i.tag == "identificacionRepLegal":
                self._doc_representante = i
    
    def set_ruc(self, ruc):
        self._data.set("numero", ruc)
    
    def set_nombre(self, nombre):
        self._nombre.text = str(nombre)

    def set_tipo_documento(self, tipo_documento):
        self._tipo_doc_representante.text = tipo_documento

    def set_documento(self, documento):
        self._doc_representante.text = documento

    def get_ruc(self):
        return self._data.get("numero")

    def get_nombre(self):
        return self._nombre.text

    def get_tipo_documento(self):
        return self._tipo_doc_representante.text

    def get_documento(self):
        return self._doc_representante.text

    def __str__(self):
        return tostring(self._data)
        
    def get_element(self):
        return self._data

class ListaContribuyentes:
    archivo = ""
    lista = []

    def __init__(self):
        self.ruta = os.path.join("XML")
        self.filename =  os.path.join("XML", "DtsRuc.xml")
        if not os.path.isdir(self.ruta):
            os.makedirs(self.ruta, mode=0700)


    def count(self):
        return len(self.lista)


    def exists_replace(self, ruc):
        for item in self.lista:
            if item.get_ruc() == ruc :
                return self.lista.index(item)
                
        return None


    def find_by_ruc(self, ruc):
        for item in self.lista:
            if item.get_ruc() == ruc :
                return item
        return None


    def add(self, contribuyente):
        try:
            if not (contribuyente.get_ruc() and contribuyente.get_nombre() and contribuyente.get_tipo_documento() and contribuyente.get_documento()):
                raise Warning('Faltan datos en el contribuyente')
        except AttributeError:
            raise TypeError('El argumento no es un objeto tipo contribuyente')
        
        item_index = self.exists_replace(contribuyente.get_ruc())
        if item_index:
            self.lista[item_index] = contribuyente
        else:
            self.lista.append(contribuyente)


    def remove(self, contribuyente):
        if type(contribuyente)==str:
            oContribuyente = self.find_by_ruc(contribuyente)
        else:
            oContribuyente = contribuyente
        
        if oContribuyente:
            self.lista.remove(oContribuyente)


    def save(self):
        list_size = len(self.lista)
        if list_size > 0:
            data = etree.Element("datos_ruc")
            
            for item in self.lista:
                data.insert(list_size, item.get_element())

            f = open(self.filename, 'w+')
            f.write(etree.tostring(data, encoding='utf8', pretty_print=True))
            f.close()
    

    def load(self):
        if os.path.exists(self.filename):
            parser = etree.XMLParser(remove_comments=True, encoding='utf8')
            data = etree.parse(self.filename, parser)
            root = data.getroot()
            self.lista = []
            for item in root:
                contrib = Contribuyente()
                contrib.load(item)
                self.lista.append(contrib)
        else:
            print 'No existe la ruta:', self.filename


    def get_elements(self):
        return self.lista
        
