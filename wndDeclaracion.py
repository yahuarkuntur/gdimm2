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


import os, sys
import ezGlade

try:
    from lxml import etree
except:
    print 'Se requiere lxml'
    sys.exit(1)

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


import configuration
from ref_data import RefData
from calc import Calculator
from val import Validator
from utils import *


ezGlade.set_file(configuration.GLADE_FILE)


class wndDeclaracion(ezGlade.BaseWindow):
    
    widget_container = dict()
    xml = None
    declaracion = None
    ref_data = None
    calcs = None
    validations = None


    def on_numericfield_changed(self, entry):
        text = entry.get_text()
        text = unicode(text).strip()
        entry.set_text(''.join([i for i in text if i in '0123456789.']))


    def set_declaracion(self, declaracion):
        self.declaracion = declaracion 
        self.calcs = Calculator()
        if not self.calcs.load_xml(self.declaracion):
            ezGlade.DialogBox("ERROR: No se pudo cargar el XML de cálculos para " + self.declaracion.get_version(), "error")
            self.calcs = None
            return
        
        self.validations = Validator()
        if not self.validations.load_xml(self.declaracion):
            ezGlade.DialogBox("ERROR: No se pudo cargar el XML de validaciones para " + self.declaracion.get_version(), "error")
            self.validations = None
            return
        
        self.calcs.load_xsl()    
        self.validations.load_xsl()


    def load_widget_contribuyente(self, number, text, width, height, left, top, tooltip):
        entry = gtk.Entry(max=0)
        entry.set_size_request(width, height)
        entry.set_tooltip_text(tooltip)
        entry.set_editable(False)
        entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#cccccc")) # color deshabilitado ;)
        entry.set_text(text)
        entry.set_property('xalign', 1)
        self.fixed1.put(entry, left, top)
        self.widget_container[number] = entry
        entry.show()


    def load_combo_custom_data(self, number, value, width, height, left, top, tooltip, lista_datos):
        combo = gtk.combo_box_new_text()
        combo.set_size_request(width, height)
        combo.set_tooltip_text(tooltip)
        list_store = gtk.ListStore(str, str)
        combo.set_model(list_store)
        for code, name in lista_datos:
            if value == code :
               list_store.append([name, code])
        combo.set_active(0)
        self.fixed1.put(combo, left, top)
        self.widget_container[number] = combo
        combo.show()


    def load_combo_contribuyente(self, number, value, width, height, left, top, tooltip, ref_table):
        combo = gtk.combo_box_new_text()
        combo.set_size_request(width, height)
        combo.set_tooltip_text(tooltip)
        if ref_table != "-1":
            list_store = gtk.ListStore(str, str)
            combo.set_model(list_store)
            lista_datos = self.ref_data.get_data_list(ref_table)
            for code, name in lista_datos:
                if value == code :
                    list_store.append([name, code])
            combo.set_active(0)
        self.fixed1.put(combo, left, top)
        self.widget_container[number] = combo
        combo.show()

    
    def load_widgets_from_xml(self):
        
        contribuyente = self.declaracion.get_contribuyente()

        if contribuyente is None:
            ezGlade.DialogBox("No existen datos del contribuyente", "error")
            return

        tree = etree.parse(os.path.join('XML','CMPFRM.xml'))
        
        version = self.declaracion.get_codigo_version()

        if version is None:
            ezGlade.DialogBox("Código de formulario no definido", "error")
            return

        form = tree.find("version[@codigo='"+version+"']") 

        if form is None:
            ezGlade.DialogBox("Error al cargar el formulario", "error")
            return

        self.widget_container = dict()

        y_scale     = 10
        x_scale     = 12
        start_top   = 1200
        font_factor = 1000

        for c in form:
            numero = str(int(c.attrib.get("numero"))) # se eliminan ceros de la izq
            top = (int(c.attrib.get("top")) - start_top ) / y_scale
            left = int(c.attrib.get("left")) / x_scale
            width = int(c.attrib.get("width")) / x_scale
            height = int(c.attrib.get("height")) / y_scale
            label = c.attrib.get("etiqueta")
            editable = c.attrib.get("editable")
            tablaReferencial = c.attrib.get("tablaReferencial")
            mensajeAyuda = c.attrib.get("mensajeAyuda")
            tipoControl = c.attrib.get("tipoControl")
            colorLetra = c.attrib.get("colorLetra")
            fontSize = str(int(c.attrib.get("fontSize")) * font_factor)

            # campos escritos desde la configuracion
            if numero in [ '101', '102', '198', '201', '202', '31', '104' ]:
                if numero == '202': # razon social
                    self.load_widget_contribuyente(numero, contribuyente.get_nombre(), width, height, left, top, mensajeAyuda)
                elif numero == '201': # RUC
                    self.load_widget_contribuyente(numero, contribuyente.get_ruc(), width, height, left, top, mensajeAyuda)
                elif numero == '101': # mes
                    self.load_combo_contribuyente(numero, self.declaracion.get_mes(), width, height, left, top, mensajeAyuda, tablaReferencial)
                elif numero == '102': # año
                    self.load_combo_contribuyente(numero, self.declaracion.get_anio(), width, height, left, top, mensajeAyuda, tablaReferencial)
                elif numero == '198': # cedula rep. legal
                    self.load_widget_contribuyente(numero, contribuyente.get_documento(), width, height, left, top, mensajeAyuda)
                elif numero == '31': # original o sustitutiva
                    self.load_combo_custom_data(numero, self.declaracion.get_original(), width, height, left, top, mensajeAyuda, self.ref_data.get_ori_sus())
                elif numero == '104': # formulario sustituye
                    self.load_widget_contribuyente(numero, self.declaracion.get_sustituye(), width, height, left, top, mensajeAyuda)
                continue

            if tipoControl == "L": # etiqueta
                lbl = gtk.Label(label)
                color = RGBToHTMLColor(int(colorLetra))
                lbl.set_markup('<span color="'+color+'" size="'+fontSize+'">'+label+'</span>');
                self.fixed1.put(lbl, left, top)
                lbl.show()
            elif tipoControl in ["T", 'M']: # caja de texto
                entry = gtk.Entry(max=0)
                entry.set_size_request(width, height)
                entry.set_tooltip_text(mensajeAyuda)
                if editable != "SI":
                    entry.set_editable(False)
                    entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#cccccc")) # color deshabilitado ;)
                if tipoControl == "T":
                    entry.set_text("")
                else:
                    entry.set_text("0")
                entry.set_property('xalign', 1)
                self.fixed1.put(entry, left, top)
                entry.connect("changed", self.on_numericfield_changed) # validacion solo numeros y punto (.)
                entry.connect("focus-out-event", self._onEntryTextFocusOut)
                self.widget_container[numero] = entry
                entry.show()
            elif tipoControl == "C":# combo
                combo = gtk.combo_box_new_text()
                combo.set_size_request(width, height)
                combo.set_tooltip_text(mensajeAyuda)

                if numero == '921':
                    combo.connect("changed", self._cmdBancos_changed) # binds change event

                if tablaReferencial != "-1":
                    list_store = gtk.ListStore(str, str)
                    combo.set_model(list_store)
                    # llenar combo segun datos referenciales
                    if numero in ['238', '219', '222', '243'] :
                        lista_datos = self.ref_data.get_data_list_2(tablaReferencial)
                    else: 
                        lista_datos = self.ref_data.get_data_list(tablaReferencial)

                    if not len(lista_datos):
                        ezGlade.DialogBox("Error al cargar tabla referencial " + str(tablaReferencial) + ' del campo ' + str(numero), "error")

                    for code, name in lista_datos:
                        list_store.append([name, code])
                    combo.set_active(0)
                self.fixed1.put(combo, left, top)
                self.widget_container[numero] = combo
                combo.show()

        # poner el titulo de la ventana
        title = self.wndDeclaracion.get_title()
        self.wndDeclaracion.set_title(title + self.declaracion.get_alias_formulario())


    def _cmdBancos_changed(self, widget, *args):
        """ Metodo disparado al cambiar la seleccion de la forma de pago """
        if not "922" in self.widget_container:
            return
    
        aiter = widget.get_active_iter()
        model = widget.get_model()

        if aiter is None:
            return

        widget2 = self.widget_container["922"]
        widget2.set_sensitive(True)
        biter = widget2.get_active_iter()
        bmodel = widget2.get_model()

        # 3 = Declaración Sin Valor a Pagar
        # 2 = Otras Formas de Pago
        # 1 = Convenio De Debito

        if model.get_value(aiter, 1) not in ['2', '3']:
            widget2.set_active(0)
            return

        # usar item codigo 89 = Declaraciones en cero
        if model.get_value(aiter, 1) == '3' :
            index = 0
            biter = bmodel.get_iter_first()
            while biter :
                if bmodel.get_value(biter, 1) == "89":
                    widget2.set_sensitive(False)
                    break
                biter = bmodel.iter_next(biter)
                index += 1
            widget2.set_active(index)
            return
        # usar item codigo 16 = RED BANCARIA
        elif model.get_value(aiter, 1) == '2' :
            index = 0
            biter = bmodel.get_iter_first()
            while biter :
                if bmodel.get_value(biter, 1) == "16":
                    widget2.set_sensitive(False)
                    break
                biter = bmodel.iter_next(biter)
                index += 1
            widget2.set_active(index)
            return


        
    def post_init(self):
        self.ref_data = RefData()
        self.wndDeclaracion.maximize()


    def push_statusbar_info(self, text):
        context_id = self.statusbar.get_context_id("Statusbar context")
        self.statusbar.push(context_id, text)
   

    def generate_xml_from_container(self):

        self.xml = None
    
        root = etree.Element("formulario")
        root.set('version', '0.2' )

        cabecera = etree.SubElement(root, "cabecera")
        codigo_version_formulario = etree.SubElement(cabecera, "codigo_version_formulario")
        codigo_version_formulario.text = self.declaracion.get_codigo_version()
        ruc = etree.SubElement(cabecera, "ruc")
        ruc.text = self.declaracion.get_contribuyente().get_ruc()
        codigo_moneda = etree.SubElement(cabecera, "codigo_moneda")
        codigo_moneda.text = '1'

        detalle = etree.SubElement(root, "detalle")

        for num, obj in self.widget_container.iteritems():
            if obj.__class__ is gtk.Entry:
                campo = etree.SubElement(detalle, "campo")
                campo.set('numero', num )
                text = obj.get_text()
                campo.text = unicode(text).strip()
            elif obj.__class__ is gtk.ComboBox:
                campo = etree.SubElement(detalle, "campo")
                campo.set('numero', num )
                aiter = obj.get_active_iter()
                model = obj.get_model()
                if aiter is not None:
                    campo.text = str(model.get_value(aiter, 1))
                else:
                    print 'Iterador nulo para', num
                    campo.text = '0'
            
        self.xml = root
        
    
    def do_validations(self):
        if self.validations is None:
            ezGlade.DialogBox("ERROR: El motor de validaciones no fué creado.", "error")
            return

        self.do_calculations()

        self.validations.validate(self.xml)
        validations = self.validations.get_validations()

        return validations


    def update_container_from_xml(self):
        for num, obj in self.widget_container.iteritems():
            campo = self.xml.find('detalle/campo[@numero="'+str(num)+'"]')
            if campo is None or campo.text is None:
                continue
            if obj.__class__ is gtk.Entry: # actualizar textbox
                obj.set_text(campo.text)
            elif obj.__class__ is gtk.ComboBox: # actualizar combos
                index = 0
                bmodel = obj.get_model()
                biter = bmodel.get_iter_first()
                while biter :
                    if bmodel.get_value(biter, 1) == campo.text:
                        break
                    biter = bmodel.iter_next(biter)
                    index += 1
                obj.set_active(index)
                   


    def do_calculations(self):
        if self.calcs is None:
            ezGlade.DialogBox("ERROR: El motor de cálculos no fué creado.", "error")
            return

        self.generate_xml_from_container()
        self.calcs.calc(self.xml) # actualizar el XML segun los calculos del XSLT
        self.update_container_from_xml() # actualizar el formulario segun los cambios al XML
        

    def _onEntryTextFocusOut(self, *args):
        self.do_calculations()


    def on_btnCancelar_clicked(self, widget, *args):
        # verificar si se han guardado los cambios!!!
        error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format="Los datos no guardados se perderán. Salir?", buttons=gtk.BUTTONS_OK_CANCEL)
        if error_dlg.run() == gtk.RESPONSE_OK:
            self.win.destroy()
        error_dlg.destroy()


    def _generar_nombre_archivo(self):
        alias = self.declaracion.get_alias_formulario()
        filename = alias
        if self.declaracion.get_original():
            filename += 'ORI_'
        else:
            filename += 'SUS_'
    
        if self.declaracion.get_periodicidad() == "SEMESTRAL":
            mes = self.ref_data.get_semestre_por_codigo(self.declaracion.get_mes())
        elif self.declaracion.get_periodicidad() == "MENSUAL":
            mes = self.ref_data.get_mes_por_codigo(self.declaracion.get_mes())
            mes = mes[:3]
        else:
            mes = ''

        filename += mes + str(self.declaracion.get_anio())

        return filename


    def on_btnGuardar_clicked(self, widget, *args):
        validations = self.do_validations()

        text = "El formulario presenta los siguientes errores: \n\n"
        for item in validations:
            text += item['severidad'] + ': ' + item['error'] + "\n"

        text += "\nDesea continuar de todas formas? \n"

        if len(validations):
            error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format=text, buttons=gtk.BUTTONS_OK_CANCEL)
            if error_dlg.run() != gtk.RESPONSE_OK:
                error_dlg.destroy()    
                return
            error_dlg.destroy()


        if self.declaracion.get_archivo() is not None:
            curr_file = self.declaracion.get_archivo()
            f = open(curr_file, 'w+')
            f.write(etree.tostring(self.xml, encoding='utf8', pretty_print=True))
            f.close()
            return

        dialog = gtk.FileChooserDialog("Guardar ...", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_current_name(self._generar_nombre_archivo())
        dialog.set_current_folder(os.path.join('XML_Declaraciones'))

        filter = gtk.FileFilter()
        filter.set_name("Archivos XML")
        filter.add_mime_type("application/xml")
        filter.add_pattern("*.xml")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            outfile = dialog.get_filename() # archivo destino
            outfile = outfile + '.xml'
            f = open(outfile, 'w+')
            f.write(etree.tostring(self.xml, encoding='utf8', pretty_print=True))
            f.close()
            self.declaracion.set_archivo(outfile)

        dialog.destroy()


