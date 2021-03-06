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
from calc import Calculator
from val import Validator
from data import *
from ref_data import RefData

parser = etree.XMLParser(remove_comments=True, encoding='utf8')

xml = etree.parse(os.path.join('tests','test_104A.xml'), parser)

def test_calcs(version):
    print 'Prueba de calculos:'
    calcs = Calculator()
    calcs.load_xml(version)
    calcs.load_xsl()
    calcs.calc(xml)

    #for x in calcs.get_calculations():
    #    print x
    #print 'Listo'


def test_vals(version):
    print 'Prueba de validaciones:'
    valid = Validator()
    valid.load_xml(version)
    valid.load_xsl()
    valid.validate(xml)

    for x in valid.get_validations():
        print x
    print 'Listo'


def test_xml_file_load():
    print 'Prueba de carga:'
    ref_data = RefData()
        
    lstContribuyentes = ListaContribuyentes()
    lstContribuyentes.load()
        
    declaracion = Declaracion()
    try:
        declaracion = declaracion.cargar_declaracion_guardada(xml, lstContribuyentes, ref_data)
        print 'Listo'
    except Exception as ex:
        print str(ex)
        return 

    test_calcs(declaracion)
    test_vals(declaracion)



def run_tests():
    test_xml_file_load()


if __name__ == '__main__':
    run_tests()
    
