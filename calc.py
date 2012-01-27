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


class Calculator:

    xml_parser  = None
    calc_xml    = None
    calc_xsl    = None
    #calculations  = None
    declaration = None
    

    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True, encoding='utf8')
        #self.calculations = []


    def load_xml(self, declaration): 
        self.declaration = declaration
        files = glob.glob(os.path.join('XSL', 'CAL*.xml'))
        for filename in files:
            xml = etree.parse(filename, self.parser)
            root = xml.getroot()
            if root.attrib.get('version') == self.declaration.get_version():
                self.calc_xml = xml
                print filename
                return True
        return False
        

    def load_xsl(self, filename):
        self.calc_xsl = etree.XSLT(etree.parse(os.path.join('XSLT', filename), self.parser))


    #def get_calculations(self):
    #    return self.calculations


    def calc(self, test_xml):
        if self.calc_xml is None:
            print 'XML de calculos no definido!'
            return
        
        if self.calc_xsl is None:
            print 'XSL de calculos no definido!'
            return

        #self.calculations = []

        # fecha de declaracion para validar contra fechas vigentes de calculos
        fecha_declaracion = datetime.strptime(self.declaration.get_fecha_declaracion(), "%Y-%m-%d")

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
                tipo    = formula.attrib.get('tipoFormula') 

                if tipo != "C":
                    continue

                validacion = formula.attrib.get('validacion') 
                mensajeError = formula.attrib.get('mensajeError') 
                condicionFormulaCalculo = formula.attrib.get('condicionFormulaCalculo') 
                fecha_vigencia_desde = formula.attrib.get('fechaVigenciaDesde').strip()
                fecha_vigencia_hasta = formula.attrib.get('fechaVigenciaHasta').strip()
                
                # parsear las fechas de vigencia
                vigencia_desde = datetime.strptime(fecha_vigencia_desde, "%Y%m%d") 
                
                if fecha_vigencia_hasta != "" :
                    vigencia_hasta = datetime.strptime(fecha_vigencia_hasta, "%Y%m%d") 
                else:
                    vigencia_hasta = None

                # fuera del rango de vigencia
                if vigencia_hasta is not None and ( vigencia_hasta < fecha_declaracion or fecha_declaracion < vigencia_desde ) :
                    #print fecha_vigencia_desde, fecha_vigencia_hasta, ' periodo NO vigente' 
                    continue

                # antes del periodo de vigencia
                if vigencia_hasta is None and ( vigencia_desde > fecha_declaracion ) :
                    #print fecha_vigencia_desde, ' NO vigente' 
                    continue
                
                #print '(',fecha_vigencia_desde,',',fecha_vigencia_hasta, ') sigue vigente'

                result = self.calc_xsl(test_xml, formula=validacion, condicion=condicionFormulaCalculo)

                new_val = result.find('value').text

                if new_val is not None:
                    new_val = new_val.replace(',', '.') # se corrije 2,4 => 2.4
                    new_val = float(new_val) / 100.0 
                    node.text = str(new_val) # se actualiza el valor del XML directamente




