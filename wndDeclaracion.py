#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


ezGlade.set_file(configuration.GLADE_FILE)


class wndDeclaracion(ezGlade.BaseWindow):
    
    widget_container = dict()
    xml = None
    declaracion = None
    ref_data = None
    calcs = None
    validations = None


    def set_declaracion(self, declaracion):
        self.declaracion = declaracion 
        self.calcs = Calculator()
        if not self.calcs.load_xml(self.declaracion.get_version()):
            ezGlade.DialogBox("ERROR: No se pudo cargar el XML de cálculos para " + self.declaracion.get_version(), "error")
            self.calcs = None
            return
        
        self.validations = Validator()
        if not self.validations.load_xml(self.declaracion.get_version()):
            ezGlade.DialogBox("ERROR: No se pudo cargar el XML de validaciones para " + self.declaracion.get_version(), "error")
            self.validations = None
            return
        
        self.calcs.load_xsl('calculos.xsl')    
        self.validations.load_xsl('validaciones.xsl')


    def load_widget_contribuyente(self, number, text, width, height, left, top, tooltip):
        entry = gtk.Entry(max=0)
        entry.set_size_request(width/10, height/10)
        entry.set_tooltip_text(tooltip)
        entry.set_editable(False)
        entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#cccccc")) # color deshabilitado ;)
        entry.set_text(text)
        entry.set_property('xalign', 1)
        self.fixed1.put(entry, left/10, top/10)
        self.widget_container[number] = entry
        entry.show()


    def load_combo_contribuyente(self, number, value, width, height, left, top, tooltip, ref_table):
        combo = gtk.combo_box_new_text()
        combo.set_size_request(width/10, height/10)
        combo.set_tooltip_text(tooltip)
        if ref_table != "-1":
            list_store = gtk.ListStore(str, str)
            combo.set_model(list_store)
            lista_datos = self.ref_data.get_data_list(ref_table)
            for code, name in lista_datos:
                if value == code :
                    list_store.append([name, code])
            combo.set_active(0)
        self.fixed1.put(combo, left/10, top/10)
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

        for c in form:
            numero = str(int(c.attrib.get("numero"))) # se eliminan ceros de la izq
            top = int(c.attrib.get("top")) - 1200
            left = int(c.attrib.get("left"))
            width = int(c.attrib.get("width"))
            height = int(c.attrib.get("height"))
            label = c.attrib.get("etiqueta")
            bold = c.attrib.get("fontBold")
            editable = c.attrib.get("editable")
            tablaReferencial = c.attrib.get("tablaReferencial")
            mensajeAyuda = c.attrib.get("mensajeAyuda")

            # campos escritos desde la configuracion
            if numero in [ '101', '102', '198', '199', '201', '202', '31', '104' ]:
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
                elif numero == '199': # RUC contador NULO
                    self.load_widget_contribuyente(numero, "", width, height, left, top, mensajeAyuda)
                elif numero == '31': # original o sustitutiva
                    self.load_combo_contribuyente(numero, self.declaracion.get_original(), width, height, left, top, mensajeAyuda, tablaReferencial)
                elif numero == '104': # formulario sustituye
                    self.load_widget_contribuyente(numero, self.declaracion.get_sustituye(), width, height, left, top, mensajeAyuda)
                continue

            if c.attrib.get("tipoControl") == "L": # etiqueta
                lbl = gtk.Label(label)
                if bold != "Falso":
                    lbl.set_markup("<b>"+label+"</b>")
                self.fixed1.put(lbl, left/10, top/10)
                lbl.show()
            elif c.attrib.get("tipoControl") in ["T", 'M']: # caja de texto
                entry = gtk.Entry(max=0)
                entry.set_size_request(width/10, height/10)
                entry.set_tooltip_text(mensajeAyuda)
                if editable != "SI":
                    entry.set_editable(False)
                    entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#cccccc")) # color deshabilitado ;)
                entry.set_text("0")
                entry.set_property('xalign', 1)
                self.fixed1.put(entry, left/10, top/10)
                entry.connect("key-release-event", self._onTabKeyReleased) # bind TAB event
                self.widget_container[numero] = entry
                entry.show()
            elif c.attrib.get("tipoControl") == "C":# combo
                combo = gtk.combo_box_new_text()
                combo.set_size_request(width/10, height/10)
                combo.set_tooltip_text(mensajeAyuda)
                if tablaReferencial != "-1":
                    list_store = gtk.ListStore(str, str)
                    combo.set_model(list_store)
                    # llenar combo segun datos referenciales
                    lista_datos = self.ref_data.get_data_list(tablaReferencial)
                    for code, name in lista_datos:
                        list_store.append([name, code])
                    combo.set_active(0)
                self.fixed1.put(combo, left/10, top/10)
                self.widget_container[numero] = combo
                combo.show()

        # poner el titulo de la ventana
        title = self.wndDeclaracion.get_title()
        self.wndDeclaracion.set_title(title + self.declaracion.get_alias_formulario())
    
        
    def post_init(self):
        self.ref_data = RefData()
        self.wndDeclaracion.maximize()
   

    def generate_xml_from_container(self):

        self.xml = None
    
        root = etree.Element("formulario")
        root.set('version', '0.2' )

        cabecera = etree.SubElement(root, "cabecera")
        codigo_version_formulario = etree.SubElement(cabecera, "codigo_version_formulario")
        codigo_version_formulario.text = self.declaracion.get_version()
        ruc = etree.SubElement(cabecera, "ruc")
        ruc.text = self.declaracion.get_contribuyente().get_ruc()
        codigo_moneda = etree.SubElement(cabecera, "codigo_moneda")
        codigo_moneda.text = '1'

        detalle = etree.SubElement(root, "detalle")

        for num, obj in self.widget_container.iteritems():
            if obj.__class__ is gtk.Entry:
                campo = etree.SubElement(detalle, "campo")
                campo.set('numero', num )
                campo.text = str(obj.get_text())
            elif obj.__class__ is gtk.ComboBox:
                campo = etree.SubElement(detalle, "campo")
                campo.set('numero', num )
                aiter = obj.get_active_iter()
                model = obj.get_model()
                if aiter is not None:
                    campo.text = str(model.get_value(aiter, 1))
                else:
                    campo.text = '0'
            
        self.xml = root
        
    
    def do_validations(self):
        if self.validations is None:
            ezGlade.DialogBox("ERROR: El motor de validaciones no fué creado.", "error")
            return

        self.validations.validate(self.xml)
        validations = self.validations.get_validations()

        return validations


    def do_calculations(self):
        if self.calcs is None:
            ezGlade.DialogBox("ERROR: El motor de cálculos no fué creado.", "error")
            return

        self.calcs.calc(self.xml)
        calculations = self.calcs.get_calculations()

        # se modifica el valor del widget y el XML con el valor calculado por la XSLT
        for item in calculations:
            widget = self.widget_container[item['campo']]
            campo = self.xml.find('detalle/campo[@numero="'+item['campo']+'"]')
            campo.text = item['calculo']
            
            if widget.__class__ is gtk.Entry:
                widget.set_text(item['calculo'])


    def _onTabKeyReleased(self, widget, event, *args):
        if event.keyval == gtk.keysyms.Tab:
            self.generate_xml_from_container()
            self.do_calculations()
            return True


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

        text = "El formulario presenta los siguientes errores: \n"
        for item in validations:
            text += item['severidad'] + ': ' + item['error'] + "\n"

        text += "Desea continuar de todas formas? \n"

        error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format=text, buttons=gtk.BUTTONS_OK_CANCEL)
        if error_dlg.run() != gtk.RESPONSE_OK:
            error_dlg.destroy()    
            return
        error_dlg.destroy()

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
            self.generate_xml_from_container() # generar XML
            self.do_calculations()  # realizar calculos
            f = open(outfile, 'w+')
            f.write(etree.tostring(self.xml, encoding='utf8', pretty_print=True))
            f.close()

        dialog.destroy()

        
    def destroy(self, *args):
        self.win.destroy()



