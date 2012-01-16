#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from base_document_validator import *


class CoplecDocValidator(BaseDocumentValidator):
    """ Validacion de cedula. http://www.coplec.org """

    def __init__(self, doc_number):
        BaseDocumentValidator.__init__(self, doc_number)


    def cedula_valida(self):
        ced = self.doc_number
        valores = [ int(ced[x]) * (2 - x % 2) for x in range(9) ]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        return int(ced[9]) == 10 - int(str(suma)[-1:])

    def ruc_valido(self):
        """ validacion de RUC """
        doc = self.doc_number
        if len ( doc ) != 13:
            raise gDimmDocumentException("Longitud del documento no válida")
        if doc[10:13] != "001":
            raise gDimmDocumentException("RUC no termina en 001")
        if not self.cedula_valida() :
            raise gDimmDocumentException("Primeros 10 digitos inválidos")

    def check(self):
        if len ( self.doc_number ) > 10:
            self.ruc_valido()
        
        if not self.cedula_valida() :
            raise gDimmDocumentException("Numero de cédula inválida.")
    


# tests
if __name__ == '__main__':
    cedulas = ['1801239680', '1001690237', '1002584074', '1001690237001', '1234567890']
    for c in cedulas:
        validator = CoplecDocValidator(c)
        try:
            print c, validator.check()
        except gDimmDocumentException as dex:
            print dex.value

    
    

