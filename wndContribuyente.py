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
import ezGlade

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

from data import *
import configuration
from validators.base_document_validator import gDimmDocumentException

ezGlade.set_file(configuration.GLADE_FILE)

class wndEditContribuyente(ezGlade.BaseWindow):

    def set_model(self, modelo):
        self.model = modelo


    def post_init(self):
        self.eRazonSocial.connect("changed", self.on_eRazonSocial_changed)
        self.eRUC.connect("changed", self.on_numericfield_changed)
        self.eDocumento.connect("changed", self.on_numericfield_changed)

        self.modeloTipo = gtk.ListStore(str,str)

        self.modeloTipo.append(['Cédula', "C"])
        #self.modeloTipo.append(['Pasaporte', "P"])
        
        self.cmbTipoDocumento.set_model(self.modeloTipo)
        self.cmbTipoDocumento.set_active(0)

        if not self.eRUC.get_editable():
            self.eRUC.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#cccccc")) # color deshabilitado ;)


    def on_numericfield_changed(self, entry):
        text = entry.get_text().strip()
        entry.set_text(''.join([i for i in text if i in '0123456789']))


    def on_eRazonSocial_changed(self, entry):
        text = entry.get_text()
        text = unicode(text).upper()
        entry.set_text(text)


    def set_data(self, oContribuyente):
        def search(user_data):
            for row in self.modeloTipo:
                if self.modeloTipo.get_value(row.iter, 1) == user_data:
                    return row.iter
            return None

        self.eRUC.set_text(oContribuyente.get_ruc())
        self.eRazonSocial.set_text(oContribuyente.get_nombre())
        self.eDocumento.set_text(oContribuyente.get_documento())

        myIter = search( oContribuyente.get_tipo_documento() )
        if myIter:
            self.cmbTipoDocumento.set_active_iter(myIter)


    def on_btnSave_clicked(self, widget, *args):
        contrib = Contribuyente()
        contrib.set_ruc(self.eRUC.get_text())
        contrib.set_nombre(self.eRazonSocial.get_text().upper())
        contrib.set_documento(self.eDocumento.get_text())

        iter = self.cmbTipoDocumento.get_active_iter()
        if iter:
            contrib.set_tipo_documento( self.modeloTipo.get_value(iter, 1) )
            
        try:
			contrib.verify_documents()
        except gDimmDocumentException as dex:
            ezGlade.DialogBox(dex.value, type = 'error', window = self.win)
            return None
			
        try:
            self.model.add(contrib)
        except Warning:
            ezGlade.DialogBox("No puede dejar campos en blanco", type = 'error', window = self.win)
            return None

        self.parent.load_list()
        self.win.destroy()

    def on_btnCancel_clicked(self, widget, *args):
        self.win.destroy()


class wndNuevoContribuyente(wndEditContribuyente):
    def __init__(self):
        wndEditContribuyente.__init__(self)


class wndContribuyente(ezGlade.BaseWindow):
    "Ventana de edición de la lista de contribuyentes"

    lista_contribuyentes = None


    def load_list(self):
        cont = 1

        self.lista_contribuyentes.clear()
        for item in self.lstContribuyentes.get_elements():
            self.lista_contribuyentes.append([item.get_ruc(),item.get_nombre()])
            cont+=1


    def post_init(self):
        self.lista_contribuyentes = gtk.ListStore(str, str)

        self.lstContribuyentes = ListaContribuyentes()
        self.lstContribuyentes.load()
        self.load_list()

        self.trContribuyentes.set_model(self.lista_contribuyentes)

        # create the TreeViewColumn to display the data
        self.columna_ruc = gtk.TreeViewColumn('RUC')
        self.columna_nombre = gtk.TreeViewColumn('Nombre')

        # add tvcolumn to treeview
        self.trContribuyentes.append_column(self.columna_ruc)
        self.trContribuyentes.append_column(self.columna_nombre)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.columna_ruc.pack_start(self.cell, True)
        self.columna_nombre.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.columna_ruc.add_attribute(self.cell, 'text', 0)
        self.columna_nombre.add_attribute(self.cell, 'text', 1)

        self.trContribuyentes.set_search_column(0)
        self.columna_ruc.set_sort_column_id(0)
        self.columna_nombre.set_sort_column_id(1)


    def get_selected(self):
        treeselection = self.trContribuyentes.get_selection()
        (model, iter) = treeselection.get_selected()
        if not iter:
            ezGlade.DialogBox("Debe seleccionar al menos un ítem", type = 'warning', window = self.win)
            return (None,None)
        else:
            return (model, iter)


    def on_btnNuevo_clicked(self, widget, *args):
        wNuevo = wndNuevoContribuyente()
        wNuevo.set_parent(self)
        wNuevo.set_modal(True)
        wNuevo.set_model(self.lstContribuyentes)
        wNuevo.show()


    def on_btnEditar_clicked(self, widget, *args):
        (model, iter) = self.get_selected()
        if iter:
            ruc = model.get_value(iter, 0)
            contrib = self.lstContribuyentes.find_by_ruc(ruc)

            wEditar = wndEditContribuyente()
            wEditar.set_parent(self)
            wEditar.set_modal(True)
            wEditar.set_model(self.lstContribuyentes)
            wEditar.set_data(contrib)
            wEditar.show()


    def on_btnBorrar_clicked(self, widget, *args):
        error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format="Está seguro de eliminar?", buttons=gtk.BUTTONS_OK_CANCEL)

        if error_dlg.run() == gtk.RESPONSE_CANCEL:
            error_dlg.destroy()
            return

        error_dlg.destroy()

        (model, iter) = self.get_selected()
        if iter:
            ruc = model.get_value(iter, 0)
            if ruc:
                self.lstContribuyentes.remove(ruc)
                model.remove(iter)


    def on_trContribuyentes_select_cursor_row(self, widget, *args):
        pass


    def on_btnClose_clicked(self, widget, *args):
        self.win.destroy()


    def on_btnSave_clicked(self, widget, *args):
        self.lstContribuyentes.save()
        self.parent.load_contribuyentes()
        self.win.destroy()



