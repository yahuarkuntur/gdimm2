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


def RGBToHTMLColor(int_color):
    """ convert an int color to #RRGGBB """
    Blue =  int_color & 255
    Green = (int_color >> 8) & 255
    Red =   (int_color >> 16) & 255
    rgb_tuple = (Red, Green, Blue)
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    return hexcolor


def get_active_text(combobox):
    iter = combobox.get_active_iter()
    model = combobox.get_model()
    if iter is None:
        return None
    return str(model.get_value(iter, 1))



# tests
if __name__ == '__main__':
    color = 16711680
    print color, '=', RGBToHTMLColor(16711680)

