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


import sys
from wndMain import *


class gDIMM2:

    def __init__(self):
        pass


    def start(self):
        mainWindow = wndMain()
        mainWindow.show()
        gtk.main()


def main(argv):
    app = gDIMM2()
    app.start()


if __name__ == '__main__':
	main(sys.argv)
