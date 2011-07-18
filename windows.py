#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

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

ezGlade.set_file(configuration.GLADE_FILE)




class wndEditContribuyente(ezGlade.BaseWindow):

    def set_model(self, modelo):
        self.model = modelo

    def post_init(self):
        self.modeloTipo = gtk.ListStore(str,str)

        self.modeloTipo.append(['Cédula', "C"])
        self.modeloTipo.append(['Pasaporte', "P"])

        self.cmbTipoDocumento.set_model(self.modeloTipo)

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
        contrib.set_nombre(self.eRazonSocial.get_text())
        contrib.set_documento(self.eDocumento.get_text())

        iter = self.cmbTipoDocumento.get_active_iter()
        if iter:
            contrib.set_tipo_documento( self.modeloTipo.get_value(iter, 1) )

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
            ezGlade.DialogBox("Debe seleccionar al menos un item", type = 'warning', window = self.win)
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

class wndAcerca(ezGlade.BaseWindow):

    def on_wndAcerca_close(self, *args):
        self.win.destroy()

    def on_wndAcerca_response(self, *args):
        self.win.destroy()

class gDIMM:

    def __init__(self):
        pass

    def start(self):
        mainWindow = wndMain()
        mainWindow.show()
        gtk.main()

class wndMain(ezGlade.BaseWindow):
    lista_contribuyentes = None

    def load_contribuyentes(self):
        "Carga el combobox con la lista de contribuyentes e incluye la opción de editar"

        self.lista_contribuyentes.clear()
        self.lista_contribuyentes.append(['','Editar lista de contribuyentes...'])

        lstContribuyentes = ListaContribuyentes()
        lstContribuyentes.load()
        for item in lstContribuyentes.get_elements():
            self.lista_contribuyentes.append([item.get_ruc(), item.get_nombre()])

    def post_init(self):
        self.lista_contribuyentes = gtk.ListStore(str, str)
        self.load_contribuyentes()

        self.cmbContribuyente.set_model(self.lista_contribuyentes)

        self.cmbContribuyente.clear()
        cell_ruc = gtk.CellRendererText()
        cell_nombre = gtk.CellRendererText()

        self.cmbContribuyente.pack_end(cell_ruc, False)
        self.cmbContribuyente.pack_start(cell_nombre, False)
        self.cmbContribuyente.add_attribute(cell_ruc, 'text', 0)
        self.cmbContribuyente.add_attribute(cell_nombre, 'text', 1)

        #Combo para el manejo de formularios
        formularios = gtk.ListStore(str, str)
        self.cmbFormularios.set_model(formularios)

        lista_formularios = [
                            ["102", "Formulario 102: Impuesto a la renta personas naturales"],
                            ["102a", "Formulario 102A: Impuesto a la renta peronas naturales (no obligados a llevar contabilidad)"],
                            ["103", "Formulario 103: Retenciones en la fuente del impuesto a la renta"],
                            ["104", "Formulario 104: Impuesto al Valor Agregado"],
                            ["104a", "Formulario 104A:  Impuesto al Valor Agregado (No obligados a llevar contabilidad)"],
                            ["105", "Formulario 105: Impuesto a los Consumos Especiales"],
                            ["106", "Formulario 106: Formulario Múltiple de Pago"],
                            ["108", "Formulario 108: I.R. sobre ingresos de herencias, legados y donaciones"]
                            ]
        for elemento in lista_formularios:
            formularios.append(elemento)

        cell_imagen = gtk.CellRendererPixbuf()
        cell_imagen.set_property("stock-id", "gtk-edit")
        self.cmbFormularios.pack_start(cell_imagen, False)

        cell_formularios = gtk.CellRendererText()
        self.cmbFormularios.pack_start(cell_formularios, False)
        self.cmbFormularios.add_attribute(cell_formularios, 'text', 1)


    def destroy(self, *args):
        gtk.main_quit()

    def on_btnAbout_clicked(self, *args):
        vAcercaDe = wndAcerca()
        vAcercaDe.set_parent(self)
        vAcercaDe.set_modal(True)
        vAcercaDe.show()

    def on_cmbContribuyente_changed(self, widget, *args):
        "Señal que se dispara cuando se cambia la selección de un contribuyente de la lista"

        iter = widget.get_active_iter()
        if not iter:
            return # Para cortar el proceso cuando se vuelva a disparar el evento al desmarcar el item actualmente seleccionado

        codigo_contribuyente = self.lista_contribuyentes.get_value(iter, 0)

        if codigo_contribuyente == "":
            widget.set_active(-1) #Hace que se deseleccione el item del combobox

            frmContribuyentes = wndContribuyente()
            frmContribuyentes.set_parent(self)
            frmContribuyentes.set_modal(True)
            frmContribuyentes.show()


    def on_btnNuevaDeclaracion_clicked(self, *args):
        self.swMain.show()

    def on_btnEditar_clicked(self, *args):
        def myresponse(widget, response):
            if response == 0:
                widget.destroy()
            else:
                filename = widget.get_filename()
                if filename:
                    if os.path.isfile(filename):
                        pass
                        # Hay que verificar el archivo antes de intentar abrirlo
                else:
                    ezGlade.DialogBox("Debe seleccionar un archivo", "error")

        fcArchivo = gtk.FileChooserDialog(title="Abrir declaración", parent=self.win, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL, 0, gtk.STOCK_OK, 1) )

        # Filtro de archivos
        filtro = gtk.FileFilter()
        filtro.set_name("Declaraciones en formato XML")
        filtro.add_pattern("*.xml")

        fcArchivo.set_filter(filtro)

        fcArchivo.connect("response", myresponse)
        fcArchivo.show()



    def on_btnHelp_clicked(self, *args):
        ezGlade.DialogBox("Abrir archivo de ayuda en HTML", "info")

    def on_btnClose_clicked(self, *args):
        "Botón que cierra la pantalla principal y termina la aplicación"
        gtk.main_quit()
        sys.exit(0)

    def on_cmbFormularios_changed(self, widget, *args):
        modelo = widget.get_model()
        iter = widget.get_active_iter()

        codigo_formulario = modelo.get_value(iter, 0)

        if codigo_formulario == "104" or "104a":
            self.vbPeriodo.show()
