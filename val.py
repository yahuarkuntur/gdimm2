#!/usr/bin/env python

import os
from lxml import etree
import glob


class Validator:

    xml_parser  = None
    val_xml     = None
    val_xsl     = None
    validations = None

    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True, encoding='utf8')
        self.validations = []


    def load_xml(self, version): 
        files = glob.glob(os.path.join('XSL', 'VAL*.xml'))
        for filename in files:
            xml = etree.parse(filename, self.parser)
            root = xml.getroot()
            if root.attrib.get('version') == version:
                self.val_xml = xml
                return True
        return False
        

    def load_xsl(self, filename):
        self.val_xsl = etree.XSLT(etree.parse(os.path.join('XSLT', filename), self.parser))


    def get_validations(self):
        return self.validations


    def validate(self, test_xml):
        if self.val_xml is None:
            print 'XML de validaciones no definido!'
            return
        
        if self.val_xsl is None:
            print 'XSL de validaciones no definido!'
            return

        self.validations = []

        # iteramos los campos de la declaracion
        for node in test_xml.find('detalle'):
            numero  = node.attrib.get('numero')
            valor   = node.text

            # obtenemos las formulas de validacion del campo 
            campos = self.val_xml.find('/campo[@numero="'+numero+'"]')

            # no hay validaciones para este campo... continuar
            if campos is None:
                continue

            # iterar y aplicar cada formula de calculo
            for formula in campos:
                tipo    = formula.attrib.get('tipoFormula') 

                if tipo != "V":
                    continue

                validacion = formula.attrib.get('validacion') 
                mensajeError = formula.attrib.get('mensajeError') 
                severidad = formula.attrib.get('severidad') 
                condicionFormulaCalculo = formula.attrib.get('condicionFormulaCalculo') 

                result = self.val_xsl(test_xml, formula=validacion, condicion=condicionFormulaCalculo)

                new_val = str(result.find('value').text).strip()

                if new_val == 'ERR':
                    #print 'Campo:', numero, 'ERROR', mensajeError, 'severidad:', severidad
                    self.validations.append({'campo': numero, 'severidad': severidad, 'error': mensajeError})



# test
if __name__ == '__main__':
    parser = etree.XMLParser(remove_comments=True, encoding='utf8')
    declaracion = etree.parse(os.path.join('tests','104ORI_JUN2011.xml'), parser)

    valid = Validator()
    valid.load_xml('04200902') # iva mensual
    valid.load_xsl('validaciones.xsl')

    valid.validate(declaracion)

    for x in valid.get_validations():
        print x



        
        



    
    



        



    
    


