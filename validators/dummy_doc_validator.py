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


class DummyDocValidator(BaseDocumentValidator):
    """ Validacion de cedula solo como digitos """

    def __init__(self, doc_number):
        BaseDocumentValidator.__init__(self, doc_number)


    def check(self):
        p = re.compile('^\d{10,13}$')
        if p.match(self.doc_number) is None:
            raise gDimmDocumentException("El documento no es válido")

    


# tests
if __name__ == '__main__':
    cedulas = ['1801239680', '1001690237', '1002584074', '1001690237001', '1234567890']
    for c in cedulas:
        validator = DummyDocValidator(c)
        try:
            print c, validator.check()
        except gDimmDocumentException as dex:
            print dex.value

    
    

