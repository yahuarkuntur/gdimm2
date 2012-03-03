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
import glob
from datetime import date, datetime


class Validator:

    parser      = None
    val_xml     = None
    val_xsl     = None
    validations = None
    declaration = None


    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True, encoding='utf8')
        self.validations = []


    def load_xml(self, declaration): 
        self.declaration = declaration
        files = glob.glob(os.path.join('XSL', 'VAL*.xml'))
        for filename in files:
            xml = etree.parse(filename, self.parser)
            root = xml.getroot()
            if root.attrib.get('version') == self.declaration.get_version():
                self.val_xml = xml
                print filename
                return True
        return False
        

    def load_xsl(self):
        filename = 'trans.xsl'
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

        # fecha de declaracion para validar contra fechas vigentes de calculos
        fecha_declaracion = datetime.strptime(self.declaration.get_fecha_declaracion(), "%Y-%m-%d")

        # iteramos los calculos del XML
        for campos in self.val_xml.getroot():

            numero  = campos.attrib.get('numero')   

            for formula in campos:
                
                tipo    = formula.attrib.get('tipoFormula') 
                validacion = formula.attrib.get('validacion') 
                mensajeError = formula.attrib.get('mensajeError') 
                severidad = formula.attrib.get('severidad') 
                condicionFormulaCalculo = formula.attrib.get('condicionFormulaCalculo') 
                fecha_vigencia_desde = formula.attrib.get('fechaVigenciaDesde')
                fecha_vigencia_hasta = formula.attrib.get('fechaVigenciaHasta')

                if tipo != "V":
                    continue       

                campo = test_xml.find('detalle/campo[@numero="'+numero+'"]')

                # parsear las fechas de vigencia
                vigencia_desde = datetime.strptime(fecha_vigencia_desde, "%Y%m%d") 
                
                if fecha_vigencia_hasta != "" :
                    vigencia_hasta = datetime.strptime(fecha_vigencia_hasta, "%Y%m%d") 
                else:
                    vigencia_hasta = None

                # fuera del rango de vigencia
                if vigencia_hasta is not None and ( vigencia_hasta < fecha_declaracion or fecha_declaracion < vigencia_desde ) :
                    continue

                # antes del periodo de vigencia
                if vigencia_hasta is None and ( vigencia_desde > fecha_declaracion ) :
                    continue

                result = self.val_xsl(test_xml, formula=validacion, condicion=condicionFormulaCalculo)

                new_val = str(result.find('value').text).strip()
                
                if new_val != 'true':
                    self.validations.append({'campo': numero, 'severidad': severidad, 'error': mensajeError})


