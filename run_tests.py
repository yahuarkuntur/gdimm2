#!/usr/bin/env python

import os
from lxml import etree
from calc import Calculator
from val import Validator
from data import *
from ref_data import RefData

parser = etree.XMLParser(remove_comments=True, encoding='utf8')

declaracion = etree.parse(os.path.join('tests','104ORI_JUN2011.xml'), parser)

def test_calcs():
    print 'Prueba de calculos:'
    calcs = Calculator()
    calcs.load_xml('04200902') # iva mensual
    calcs.load_xsl('calculos.xsl')

    calcs.calc(declaracion)

    for x in calcs.get_calculations():
        print x
    print 


def test_vals():
    print 'Prueba de validaciones:'
    valid = Validator()
    valid.load_xml('04200902') # iva mensual
    valid.load_xsl('validaciones.xsl')

    valid.validate(declaracion)

    for x in valid.get_validations():
        print x
    print

def test_xml_file_load():

    import ezGlade
    from wndDeclaracion import wndDeclaracion
    import configuration

    ezGlade.set_file(configuration.GLADE_FILE)

    # inicializa objeto declaracion
    #declaracion = Declaracion()

    # inicializa datos de contribuyentes
    contribuyentes = ListaContribuyentes()
    contribuyentes.load()

    # inicializa datos referenciales
    ref_data = RefData()

    xml = etree.parse(os.path.join('tests','104ORI_JUN2011.xml'), parser)

    cabecera = xml.find('cabecera')

    # TODO codigo_version_formulario hace referencia a <datosFormulariosVersiones codigo="10">
    codigo_version_formulario = cabecera.find('codigo_version_formulario').text
    ruc = cabecera.find('ruc').text

    print codigo_version_formulario, ruc

    contribuyente = contribuyentes.find_by_ruc(ruc)

    print contribuyente.get_nombre()

    if contribuyente is None:
        print 'Error al cargar el contribuyente'

    declaracion = ref_data.get_objeto_declaracion(codigo_version_formulario)

    declaracion.set_contribuyente(contribuyente)

    declaracion.set_anio("2011")

    declaracion.set_mes("6")

    declaracion.set_original('S')
    declaracion.set_sustituye("")

    # crear ventana del formulario de declaracion
    vDeclaracion = wndDeclaracion()
    vDeclaracion.set_declaracion(declaracion)
    vDeclaracion.load_widgets_from_xml()
    vDeclaracion.show()


def run_tests():
    #test_calcs()
    #test_vals()
    test_xml_file_load()


if __name__ == '__main__':
    run_tests()
    
