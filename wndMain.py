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
from ref_data import *
import configuration
from wndDeclaracion import wndDeclaracion
from wndContribuyente import wndContribuyente

ezGlade.set_file(configuration.GLADE_FILE)


class wndAcerca(ezGlade.BaseWindow):

    def on_wndAcerca_close(self, *args):
        self.win.destroy()

    def on_wndAcerca_response(self, *args):
        self.win.destroy()


class wndMain(ezGlade.BaseWindow):

    lista_contribuyentes = None
    declaracion   = None

    def load_contribuyentes(self):
        "Carga el combobox con la lista de contribuyentes e incluye la opción de editar"

        self.lista_contribuyentes.clear()
        self.lista_contribuyentes.append(['','Editar lista de contribuyentes...'])

        lstContribuyentes = ListaContribuyentes()
        lstContribuyentes.load()
        for item in lstContribuyentes.get_elements():
            self.lista_contribuyentes.append([item.get_ruc(), item.get_nombre()])


    def post_init(self):
        self.declaracion = Declaracion()
        
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
        self.cmbFormularios.clear()
        lista_formularios = gtk.ListStore(str, str)
        self.cmbFormularios.set_model(lista_formularios)
        lista_datos = get_datos_formularios()

        for code, name in lista_datos:
            lista_formularios.append([name, code])
        
        cell_formularios = gtk.CellRendererText()
        self.cmbFormularios.pack_start(cell_formularios, False)
        self.cmbFormularios.add_attribute(cell_formularios, 'text', 0)
        
        self.cmbFormularios.set_active(0)

        # combo de anios
        self.cmbAnio.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbAnio.set_model(list_store)
        lista_datos = get_data_list(30) # anios
        lista_datos.reverse()

        for code, name in lista_datos:
            list_store.append([name, code])

        cell_anios = gtk.CellRendererText()
        self.cmbAnio.pack_start(cell_anios, False)
        self.cmbAnio.add_attribute(cell_anios, 'text', 0)
        self.cmbAnio.set_active(0)


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
        else:
            lstContribuyentes = ListaContribuyentes() # TODO cargar una sola vez?
            lstContribuyentes.load()
            contribuyente = lstContribuyentes.find_by_ruc(codigo_contribuyente)
            if contribuyente is not None:
                self.declaracion.set_contribuyente(contribuyente)


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
                        # TODO cargar declaracion XML
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


    def on_rbSemestral_toggled(self, widget, *args):
        self.cmbPeriodo.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbPeriodo.set_model(list_store)
        lista_datos = []

        if widget.get_active() :
            lista_datos = get_data_list(40) # periodos
        else:
            lista_datos = get_data_list(20) # meses

        for code, name in lista_datos:
            list_store.append([name, code])  

        cell_periodo = gtk.CellRendererText()
        self.cmbPeriodo.pack_start(cell_periodo, False)
        self.cmbPeriodo.add_attribute(cell_periodo, 'text', 0)

        self.cmbPeriodo.set_active(0)   

        self.vbPeriodo.show() 
        
    

    def on_cmbFormularios_changed(self, widget, *args):
        modelo = widget.get_model()
        iter = widget.get_active_iter()
        codigo_formulario = modelo.get_value(iter, 1)

        self.cmbPeriodo.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbPeriodo.set_model(list_store)
        lista_datos = []

        periodicidad = get_periodicidad(codigo_formulario)

        if periodicidad == "MENSUAL":
            lista_datos = get_data_list(20) # meses
        elif periodicidad == "MENSUAL_SEMESTRAL":
            self.hbPeriodo.show()
            if self.rbSemestral.get_active() :
                lista_datos = get_data_list(40) # periodos 
            else:
                lista_datos = get_data_list(20) # meses
        else: # anual
            lista_datos = get_data_list(40) # periodos

        for code, name in lista_datos:
            list_store.append([name, code])  

        cell_periodo = gtk.CellRendererText()
        self.cmbPeriodo.pack_start(cell_periodo, False)
        self.cmbPeriodo.add_attribute(cell_periodo, 'text', 0)

        self.cmbPeriodo.set_active(0)   

        self.vbPeriodo.show()   



    def on_btnAceptar_clicked(self, *args):
        if self.declaracion.get_contribuyente() is None:
            ezGlade.DialogBox("No se ha seleccionado el contribuyente", "error")
            return

        # obtener formulario TODO factorize
        aiter = self.cmbFormularios.get_active_iter()
        model = self.cmbFormularios.get_model()
        if aiter is not None:
            self.declaracion.set_formulario(str(model.get_value(aiter, 1)))

        # obtener anio
        aiter = self.cmbAnio.get_active_iter()
        model = self.cmbAnio.get_model()
        if aiter is not None:
            self.declaracion.set_anio(str(model.get_value(aiter, 1)))

        # obtener mes o periodo
        aiter = self.cmbPeriodo.get_active_iter()
        model = self.cmbPeriodo.get_model()
        if aiter is not None:
            self.declaracion.set_mes(str(model.get_value(aiter, 1)))
        

        # crear ventana del formulario de declaracion
        vDeclaracion = wndDeclaracion()
        #vDeclaracion.set_codigo_formulario('04200901')
        vDeclaracion.set_declaracion(self.declaracion)
        vDeclaracion.load_widgets_from_xml()
        vDeclaracion.show()



