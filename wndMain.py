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
from wndDeclaracion import wndDeclaracion

ezGlade.set_file(configuration.GLADE_FILE)


class wndAcerca(ezGlade.BaseWindow):

    def on_wndAcerca_close(self, *args):
        self.win.destroy()

    def on_wndAcerca_response(self, *args):
        self.win.destroy()


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
        # TODO obtener desde los datos referenciales
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


    def on_btnAceptar_clicked(self, *args):
        # TODO pasar la informacion del contribuyente y el formulario seleccionado 
        vDeclaracion = wndDeclaracion()
        vDeclaracion.set_codigo_formulario('04200901')
        vDeclaracion.load_widgets_from_xml()
        vDeclaracion.show()



