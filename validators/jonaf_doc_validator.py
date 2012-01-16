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


class JonathanDocValidator(BaseDocumentValidator):
    """ Validacion de cedula/ruc. https://github.com/jonathanf """

    def __init__(self, doc_number):
        BaseDocumentValidator.__init__(self, doc_number)


    def check(self):
        doc = self.doc_number
        try:
            int(doc)
        except:
            raise gDimmDocumentException("El documento debe contener sólo caracteres numéricos")

        if ( int ( doc[0:2] ) < 1 or int ( doc[0:2] ) > 24 ):
            raise gDimmDocumentException("Los primeros caracteres deben contener códigos de provincias válidas")
        
        if doc[2] == '6':
            tipo_ruc = "publico"
            coeficiente = "32765432"
            verificador = int ( doc[8] )
        else:
            if doc[2] == "9":
                tipo_ruc = "juridico"
                coeficiente = "432765432"
            else:
                if int ( doc[2] ) < 6:
                    tipo_ruc = "natural"
                    coeficiente = "212121212"
                else:
                    raise gDimmDocumentException("Error en el tercer dígito del documento")
            verificador = int ( doc[9] )

        resultado = 0
        suma = 0
        if tipo_ruc == "publico":
            for i in range(8):
                resultado += ( int ( doc[i] ) * int ( coeficiente[i] ) )
                residuo = resultado % 11
            if residuo == 0:
                resultado = residuo
            else:
                resultado = 11 - residuo
                
        if tipo_ruc == "juridico":
            for i in range(9):
                resultado += ( int ( doc[i] ) * int ( coeficiente[i] ) )
                residuo = resultado % 11
                if residuo == 0:
                    resultado = residuo
                else:
                    resultado = 11 - residuo
        
        if tipo_ruc == "natural":
            for i in range(9):
                suma = ( int ( doc[i] ) * int ( coeficiente[i] ) )
                if suma > 10 :
                    str_suma = str ( suma )
                    suma = int ( str_suma[0] ) + int (str_suma [1])
                resultado += suma
            residuo = resultado % 10
            if residuo == 0:
                resultado = residuo
            else:
                resultado = 10 - residuo
                
        if resultado != verificador:
            raise gDimmDocumentException("El documento no es válido")
    


# tests
if __name__ == '__main__':
    cedulas = ['1801239680', '1001690237', '1002584074', '1001690237001', '1234567890']
    for c in cedulas:
        validator = JonathanDocValidator(c)
        try:
            print c, validator.check()
        except gDimmDocumentException as dex:
            print dex.value

    
    

