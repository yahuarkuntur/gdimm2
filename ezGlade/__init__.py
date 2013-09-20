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


import sys, os

try:
    import pygtk
    pygtk.require("2.0")
except:
    print 'pygtk required'
    sys.exit(1)
try:
    import gtk
    import gtk.glade
except:
    print 'glade required'
    sys.exit(1)

GLADE_FILE = ""

def set_file(filename):
	global GLADE_FILE
	
	if not os.path.exists (filename):
		raise IOException
	
	GLADE_FILE = filename

def idle_events():
	while gtk.events_pending():
		gtk.main_iteration()

def DialogBox(message, type = 'error', window = None):
	def closeHandler(self, response):
		self.destroy()

	message_type = {
			"error" : gtk.MESSAGE_ERROR,
			"warning" : gtk.MESSAGE_WARNING,
			"info" : gtk.MESSAGE_INFO}

	wndDialog = gtk.MessageDialog(parent = window, flags= gtk.DIALOG_MODAL, type = message_type[type], buttons = gtk.BUTTONS_OK, message_format = message)
	wndDialog.connect("response", closeHandler)
	wndDialog.show()

class BaseWindow:
	"Base class to define the widgets and methods to be used for each window"
	windowname = ''

	def __init__(self):
		#Gets the window name from the class name
		self.windowname = str(self.__class__).split(".")[1]

		if self.windowname:
			self.wTree = gtk.glade.XML(GLADE_FILE, self.windowname)
			self.win = self.wTree.get_widget(self.windowname)
			self.wTree.signal_autoconnect(self)
			self.win.connect("destroy", self.destroy)
			
			#Reads all the defined controls associated to a single window and makes them
			#available for the current class as properties (Ex: If I have a widget name txtName I would just
			#call it self.txtName whenever I need to use it
			for control in self.wTree.get_widget_prefix(''):
				self.__dict__[control.get_name()] = control
			
		self.post_init()

	def init(self):
		"Función virtual que debe ser sobreescrita para especificar los valores de arranque del formulario"
		pass

	def post_init(self):
		"Función que se ejecuta luego de haber creado el formulario base y conectado las señales"
		pass

	def show(self):
		"Llama al método show del widget correspondiente a la ventana"

		if self.win:
			self.win.show()

	def hide(self):
		if self.win:
			self.win.hide()

	def set_modal(self, bool = False):
		self.win.set_modal(bool)

	def destroy(self, *args):
		pass

	def set_parent(self, parent):
		"Establece la clase padre y la ventana padre para el objeto actual"
		if parent:
			self.parent = parent
			self.win.set_transient_for(parent.win)

