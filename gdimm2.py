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

#<Actualizar Url="https://declaraciones.sri.gov.ec/rec-declaraciones-internet/login/indexAction.jspa?m=5"/>
#<enviarDeclaracion Url="https://declaraciones.sri.gov.ec/rec-declaraciones-internet"/>


import sys
import logging
from windows import gDIMM

def main(argv):
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
	app = gDIMM()
	app.start()

if __name__ == '__main__':
	main(sys.argv)
