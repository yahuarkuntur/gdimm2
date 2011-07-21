#!/usr/bin/env python

import os
from lxml import etree
from calc import Calculator
from val import Validator

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


def run_tests():
    test_calcs()
    test_vals()


if __name__ == '__main__':
    run_tests()
    
