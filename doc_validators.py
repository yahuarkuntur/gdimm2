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

import re


class gDimmDocumentException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value


def validar_digitos(ced):
    """ Validacion de cedula solo como digitos """
    p = re.compile('^\d{10}$')
    if p.match(ced) is None:
        return False
    return True



def cedula_valida(ced):
    """ Validacion de cedula. http://www.coplec.org """
    valores = [ int(ced[x]) * (2 - x % 2) for x in range(9) ]
    suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
    return int(ced[9]) == 10 - int(str(suma)[-1:])


def ruc_valido(doc):
    """ validacion de RUC """
    if len ( doc ) != 13:
        raise gDimmDocumentException("Longitud del documento no válida")
    if doc[10:13] != "001":
        raise gDimmDocumentException("RUC no termina en 001")
    if not validar_digitos(doc[:10]) :
        raise gDimmDocumentException("Primeros 10 digitos inválidos")



def verify(doc, tipo):
    """ Validacion de cedula/ruc. https://github.com/jonathanf """
    if tipo == 'P':
        raise gDimmDocumentException("No se validan pasaportes")

    if tipo == 'R':
        if len ( doc ) != 13:
            raise gDimmDocumentException("Longitud del documento no válida")
        if doc[10:13] == "000":
            raise gDimmDocumentException("RUC terminado en 000")
    else:
        if len ( doc ) != 10:
            raise gDimmDocumentException("Longitud del documento no válida")
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
        
                
    if resultado == verificador:
        # El documento es válido ;)
        return
    else:
        raise gDimmDocumentException("El documento no es válido")



# tests
if __name__ == '__main__':
    #print cedula_valida('1002584074')
    #print cedula_valida('1001690237')
    #print cedula_valida('1002003004')
    #print cedula_valida('1801239680')

    #verify('1002584074', 'C')
    #verify('1001690237', 'C')
    #verify('1002003004', 'C')
    #verify('1801239680', 'C')
    cedulas = ['1801239680', '1001690237', 'abc1234567', '1234', '12345678901323']
    for c in cedulas:
        print c, validar_digitos(c)



    


