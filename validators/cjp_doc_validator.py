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
from base_document_validator import *


class CJPDocValidator(BaseDocumentValidator):
    """ Validacion de cedula. http://carlosjulioperezq.blogspot.com/2007/03/validacin-de-cdula-ruc-y-pasaporte.html """

    def __init__(self, doc_number):
        BaseDocumentValidator.__init__(self, doc_number)

    def check(self):
        numero = self.doc_number
        suma    = 0
        residuo = 0
        pri = False
        pub = False
        nat = False
        numeroProvincias = 22
        modulo = 11
                  
        # solo se permiten 10 digitos
        p = re.compile('^\d{10,13}$')
        if p.match(numero) is None:
            raise gDimmDocumentException('Solo se admiten de 10 a 13 digitos.')

        # Los primeros dos digitos corresponden al codigo de la provincia 
        provincia = int(numero[0:2])
        
        if provincia < 1 or provincia > numeroProvincias:           
            raise gDimmDocumentException('El código de la provincia (dos primeros dígitos) es inválido.')
    
        # Aqui almacenamos los digitos de la cedula en variables.
        valores = [ int(numero[x]) for x in range(9) ]

        # El tercer digito es: 
        # 9 para sociedades privadas y extranjeros
        # 6 para sociedades publicas
        # menor que 6 (0,1,2,3,4,5) para personas naturales
        if valores[2] in [7, 8] :
            raise gDimmDocumentException('El tercer dígito ingresado es inválido')
    
        # Solo para personas naturales (modulo 10)
        if valores[2] < 6 :
            nat = True
            for x in range(9):
                valores[x] = valores[x] * (2 - x % 2)
                if valores[x] >= 10 :
                    valores[x] -= 9
            modulo = 10
    
        # Solo para sociedades publicas (modulo 11)            
        # Aqui el digito verficador esta en la posicion 9, en las otras 2 en la pos. 10 
        elif valores[2] == 6 :
            pub = True          
            valores[0] *= 3
            valores[1] *= 2
            valores[2] *= 7
            valores[3] *= 6
            valores[4] *= 5
            valores[5] *= 4
            valores[6] *= 3
            valores[7] *= 2
            valores[8] = 0
             
        # Solo para entidades privadas (modulo 11) */         
        elif valores[2] == 9 :
            pri = True
            valores[0] *= 4
            valores[1] *= 3
            valores[2] *= 2
            valores[3] *= 7
            valores[4] *= 6
            valores[5] *= 5
            valores[6] *= 4
            valores[7] *= 3
            valores[8] *= 2
    
        suma = sum(valores)
        residuo = suma % modulo
    
        # Si residuo=0, dig.ver.=0, caso contrario 10 - residuo
        if residuo == 0 :
            digitoVerificador = 0
        else :
            digitoVerificador = modulo - residuo
    
        # ahora comparamos el elemento de la posicion 10 con el dig. ver.
        if pub :
            if digitoVerificador != int(numero[8]) :
               raise gDimmDocumentException('El ruc de la empresa del sector público es incorrecto.')
                 
            # El ruc de las empresas del sector publico terminan con 0001       
            if numero[9:] != '0001' :
               raise gDimmDocumentException('El ruc de la empresa del sector público debe terminar con 0001')
             
        elif pri :
            if digitoVerificador != int(numero[9]) :
                raise gDimmDocumentException('El ruc de la empresa del sector privado es incorrecto.')

            if numero[10:] != '001' :
                raise gDimmDocumentException('El ruc de la empresa del sector privado debe terminar con 001')

        elif nat :
            if digitoVerificador != int(numero[9]) :
                raise gDimmDocumentException('El número de cédula de la persona natural es incorrecto.')

            if len(numero) > 10 and numero[10:] != '001' :
                raise gDimmDocumentException('El ruc de la persona natural debe terminar con 001')
    


# tests
if __name__ == '__main__':
    cedulas = ['1801239680', '1001690237', '1002584074', '1001690237001', '1234567890']
    for c in cedulas:
        validator = CJPDocValidator(c)
        try:
            print c, validator.check()
        except gDimmDocumentException as dex:
            print dex.value

    
    

