#!/usr/bin/env python

import os
from lxml import etree
import glob
from datetime import date, datetime


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
                fecha_vigencia = formula.attrib.get('fechaVigenciaHasta')
                fecha_vigencia.strip()
                
                # solo calculos vigentes
                if fecha_vigencia != "" and datetime.today() > datetime.strptime(fecha_vigencia, "%Y%m%d"):
                    continue

                result = self.val_xsl(test_xml, formula=validacion, condicion=condicionFormulaCalculo)

                new_val = str(result.find('value').text).strip()
                
                if new_val != 'true':
                    self.validations.append({'campo': numero, 'severidad': severidad, 'error': mensajeError})
   
    



