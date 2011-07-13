#!/usr/bin/env python

import os
from lxml import etree


class Calculator:

    xml_parser  = None
    calc_xml    = None
    calc_xsl    = None
    calculations  = None

    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True, encoding='utf8')
        self.calculations = []

    def load_xml(self, filename): 
        self.calc_xml = etree.parse(os.path.join('XML', filename), self.parser)

    def load_xsl(self, filename):
        self.calc_xsl = etree.XSLT(etree.parse(os.path.join('XSL', filename), self.parser))

    def get_calculations(self):
        return self.calculations

    def calc(self, test_xml):
        if self.calc_xml is None:
            print 'XML de calculos no definido!'
            return
        
        if self.calc_xsl is None:
            print 'XSL de calculos no definido!'
            return

        self.calculations = []

        #print etree.tostring(test_xml, encoding='utf8', pretty_print=True)

        # iteramos los campos de la declaracion
        for node in test_xml.find('detalle'):
            numero  = node.attrib.get('numero')
            valor   = node.text

            # obtenemos las formulas de calculo del campo 
            campos = self.calc_xml.find('/campo[@numero="'+numero+'"]')

            # no hay calculos para este campo... continuar
            if campos is None:
                continue

            # iterar y aplicar cada formula de calculo
            for formula in campos:
                validacion = formula.attrib.get('validacion') 
                mensajeError = formula.attrib.get('mensajeError') 
                condicionFormulaCalculo = formula.attrib.get('condicionFormulaCalculo') 

                result = self.calc_xsl(test_xml, formula=validacion, condicion=condicionFormulaCalculo)

                new_val = result.find('value').text

                if new_val is not None:
                    #    print 'Campo:', numero, 'Valor:', valor, 'Calculo:', new_val, 'Error:', mensajeError
                    self.calculations.append({'campo': numero, 'valor': valor, 'calculo': new_val})



# test
if __name__ == '__main__':
    parser = etree.XMLParser(remove_comments=True, encoding='utf8')
    declaracion = etree.parse(os.path.join('tests','104ORI_JUN2011.xml'), parser)

    calcs = Calculator()
    calcs.load_xml('CAL0402.xml') # TODO obtener del mapeo
    calcs.load_xsl('calculos.xsl')

    calcs.calc(declaracion)

    for x in calcs.get_calculations():
        print x

        
        



    
    



        



    
    



