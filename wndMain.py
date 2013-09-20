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
    print 'pygtk required'
    sys.exit(1)
try:
    import gtk
    import gtk.glade
except:
    print 'glade required'
    sys.exit(1)

from data import *
from ref_data import RefData
import configuration
from wndDeclaracion import wndDeclaracion
from wndContribuyente import wndContribuyente
from utils import *


ezGlade.set_file(configuration.GLADE_FILE)


class wndAcerca(ezGlade.BaseWindow):

    def on_wndAcerca_close(self, *args):
        self.win.destroy()

    def on_wndAcerca_response(self, *args):
        self.win.destroy()


class wndMain(ezGlade.BaseWindow):

    lista_contribuyentes = None
    declaracion   = None
    ref_data    = None

    def load_contribuyentes(self):
        "Carga el combobox con la lista de contribuyentes e incluye la opción de editar"

        self.lista_contribuyentes.clear()
        self.lista_contribuyentes.append(['Editar lista de contribuyentes...', ''])

        lstContribuyentes = ListaContribuyentes()
        lstContribuyentes.load()
        for item in lstContribuyentes.get_elements():
            self.lista_contribuyentes.append([item.get_ruc() + ' - ' + item.get_nombre(), item.get_ruc() ])


    def post_init(self):
        self.ref_data = RefData()

        self.declaracion = Declaracion()
        
        self.lista_contribuyentes = gtk.ListStore(str, str)
        self.load_contribuyentes()

        self.cmbContribuyente.set_model(self.lista_contribuyentes)
        self.cmbContribuyente.clear()
        cell_nombre = gtk.CellRendererText()
        self.cmbContribuyente.pack_start(cell_nombre, False)
        self.cmbContribuyente.add_attribute(cell_nombre, 'text', 0)

        #Combo para el manejo de formularios
        self.cmbFormularios.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbFormularios.set_model(list_store)
        lista_datos = self.ref_data.get_datos_formularios()

        for code, name in lista_datos:
            list_store.append([name, code])
        
        cell_formulario = gtk.CellRendererText()
        self.cmbFormularios.pack_start(cell_formulario, False)
        self.cmbFormularios.add_attribute(cell_formulario, 'text', 0)
        self.cmbFormularios.set_active(0)

        # combo de anios
        self.cmbAnio.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbAnio.set_model(list_store)
        lista_datos = self.ref_data.get_data_list(30) # anios
        lista_datos.reverse()

        for code, name in lista_datos:
            list_store.append([name, code])

        cell_anios = gtk.CellRendererText()
        self.cmbAnio.pack_start(cell_anios, False)
        self.cmbAnio.add_attribute(cell_anios, 'text', 0)
        self.cmbAnio.set_active(0)
        
        # version del dimm en status bar
        context_id = self.stGeneral.get_context_id("Statusbar context")
        self.stGeneral.push(context_id, self.ref_data.get_version_dimm())

        # tray icon
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_file(os.path.join('ui', 'intro.png'))
        self.statusIcon.connect("popup-menu", self.on_statusIcon_right_click)
        self.statusIcon.set_tooltip("gDimm2")        


    def on_statusIcon_right_click(self, icon, button, time):
        menu = gtk.Menu()

        about = gtk.MenuItem("Acerca de")
        quit = gtk.MenuItem("Salir")
        
        about.connect("activate", self.on_btnAbout_clicked)
        quit.connect("activate", gtk.main_quit)
        
        menu.append(about)
        menu.append(quit)
        
        menu.show_all()
        
        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusIcon)


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

        codigo_contribuyente = self.lista_contribuyentes.get_value(iter, 1)

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
        self.swMain.hide()

        dialog = gtk.FileChooserDialog("Abrir...", self.win, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_current_folder(os.path.join('XML_Declaraciones'))

        filter = gtk.FileFilter()
        filter.set_name("Archivos XML")
        filter.add_mime_type("application/xml")
        filter.add_pattern("*.xml")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename() # archivo 
            parser = etree.XMLParser(remove_comments=True, encoding='utf8')
            xml = etree.parse(filename, parser)
            dialog.destroy()
        else:
            dialog.destroy()
            return

        lstContribuyentes = ListaContribuyentes() # TODO cargar una sola vez?
        lstContribuyentes.load()
        
        self.declaracion = Declaracion()
        try:
            self.declaracion = self.declaracion.cargar_declaracion_guardada(xml, lstContribuyentes, self.ref_data)
            self.declaracion.set_archivo(filename)
        except Exception as ex:
            ezGlade.DialogBox(str(ex), 'error', self.win)
            return

        # crear ventana del formulario de declaracion
        vDeclaracion = wndDeclaracion()
        vDeclaracion.set_declaracion(self.declaracion)
        vDeclaracion.load_widgets_from_xml()
        vDeclaracion.xml = xml # asignacion directa del xml cargado
        vDeclaracion.update_container_from_xml()
        vDeclaracion.push_statusbar_info(filename)
        vDeclaracion.show()


    def on_btnHelp_clicked(self, *args):
        ezGlade.DialogBox("Abrir archivo de ayuda en HTML", "info")


    def on_btnClose_clicked(self, *args):
        "Botón que cierra la pantalla principal y termina la aplicación"
        gtk.main_quit()
        sys.exit(0)

    
    def on_rbSustitutiva_toggled(self, widget, *args):
        if widget.get_active() :
            self.hbSustituye.show()
        else:
            self.hbSustituye.hide() 



    def on_rbSemestral_toggled(self, widget, *args):
        version = get_active_text(self.cmbFormularios)
        nombre = self.ref_data.get_nombre_formulario(version)
    
        self.cmbPeriodo.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbPeriodo.set_model(list_store)
        lista_datos = []

        if widget.get_active() :
            lista_datos = self.ref_data.get_data_list(40) # periodos
            self.declaracion.set_periodicidad("SEMESTRAL")
            codigo_version = self.ref_data.get_codigo_version_formulario(nombre, "SEMESTRAL")
        else:
            lista_datos = self.ref_data.get_data_list(20) # meses
            self.declaracion.set_periodicidad("MENSUAL")
            codigo_version = self.ref_data.get_codigo_version_formulario(nombre, "MENSUAL")

        self.declaracion.set_version(version)
        self.declaracion.set_codigo_version(codigo_version)
        

        for code, name in lista_datos:
            list_store.append([name, code])  

        cell_periodo = gtk.CellRendererText()
        self.cmbPeriodo.pack_start(cell_periodo, False)
        self.cmbPeriodo.add_attribute(cell_periodo, 'text', 0)
        self.cmbPeriodo.set_active(0)   

        self.vbPeriodo.show() 
        
    

    def on_cmbFormularios_changed(self, widget, *args):
        version = get_active_text(widget)
        nombre = self.ref_data.get_nombre_formulario(version)

        self.cmbPeriodo.clear()
        list_store = gtk.ListStore(str, str)
        self.cmbPeriodo.set_model(list_store)
        lista_datos = []

        periodicidad = self.ref_data.get_periodicidad(version)

        if periodicidad == "MENSUAL_SEMESTRAL":
            self.hbPeriodo.show()
            if self.rbSemestral.get_active() :
                lista_datos = self.ref_data.get_data_list(40) # periodos 
                self.declaracion.set_periodicidad("SEMESTRAL")
                codigo_version = self.ref_data.get_codigo_version_formulario(nombre, "SEMESTRAL")
            else:
                lista_datos = self.ref_data.get_data_list(20) # meses
                self.declaracion.set_periodicidad("MENSUAL")
                codigo_version = self.ref_data.get_codigo_version_formulario(nombre, "MENSUAL")
        elif periodicidad == "MENSUAL":
            self.hbPeriodo.hide()
            lista_datos = self.ref_data.get_data_list(20) # meses
            self.declaracion.set_periodicidad("MENSUAL")
            codigo_version = self.ref_data.get_codigo_version_formulario(nombre, "MENSUAL")
        else:
            self.declaracion.set_periodicidad("ANUAL")
            codigo_version = self.ref_data.get_codigo_version_formulario(nombre, "ANUAL")

        self.declaracion.set_version(version)
        self.declaracion.set_codigo_version(codigo_version)

        for code, name in lista_datos:
            list_store.append([name, code])  

        cell_periodo = gtk.CellRendererText()
        self.cmbPeriodo.pack_start(cell_periodo, False)
        self.cmbPeriodo.add_attribute(cell_periodo, 'text', 0)
        self.cmbPeriodo.set_active(0)   

        self.vbPeriodo.show()   



    def on_btnAceptar_clicked(self, *args):
        # contribuyente
        if self.declaracion.get_contribuyente() is None:
            ezGlade.DialogBox("No se ha seleccionado el contribuyente", "error")
            return

        # alias del formulario
        version = get_active_text(self.cmbFormularios)
        alias = self.ref_data.get_nombre_formulario(version)
        alias = alias.replace("FORMULARIO ", "")
        self.declaracion.set_alias_formulario(alias)

        # archivo nulo
        self.declaracion.set_archivo(None)

        # obtener anio
        anio = get_active_text(self.cmbAnio)
        self.declaracion.set_anio(anio)

        # obtener mes o periodo
        periodo = get_active_text(self.cmbPeriodo)
        self.declaracion.set_mes(periodo)

        # original o sustitutiva
        if self.rbSustitutiva.get_active():
            self.declaracion.set_original('S')
            self.declaracion.set_sustituye(self.txtSustituye.get_text())
        else:
            self.declaracion.set_original('O')
            self.declaracion.set_sustituye('')        

        # crear ventana del formulario de declaracion
        vDeclaracion = wndDeclaracion()
        vDeclaracion.set_declaracion(self.declaracion)
        vDeclaracion.load_widgets_from_xml()
        vDeclaracion.push_statusbar_info("Nueva declaración")
        vDeclaracion.show()



