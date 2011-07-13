#!/usr/bin/env python
import os
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
from ref_data import get_data_list
from calc import Calculator


ezGlade.set_file(configuration.GLADE_FILE)


class wndDeclaracion(ezGlade.BaseWindow):
    
    codigo = None
    widget_container = dict()
    xml = None

    def set_codigo_formulario(self, codigo):
        self.codigo = codigo 
    
    
    def load_widgets_from_xml(self):
        if not self.codigo :
            print 'Codigo de formulario no definido.'
            return;
        tree = etree.parse(os.path.join('XML','CMPFRM-GNU.xml'))
        
        # formulario 104A
        form = tree.find("version[@codigo='"+self.codigo+"']") 

        self.widget_container = dict()

        for c in form:
            # campos escritos desde la configuracion
            numero = c.attrib.get("numero")
            if numero in ['0101', '0102', '0104', '0031', '0198', '0199', '0201', '0202']:
                continue
            # conversion a numero de campo entero
            numero = int(numero)
            numero = str(numero)
            top = int(c.attrib.get("top"))
            left = int(c.attrib.get("left"))
            width = int(c.attrib.get("width"))
            height = int(c.attrib.get("height"))
            label = c.attrib.get("etiqueta")
            bold = c.attrib.get("fontBold")
            editable = c.attrib.get("editable")
            tablaReferencial = c.attrib.get("tablaReferencial")
            mensajeAyuda = c.attrib.get("mensajeAyuda")
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
                entry.set_text("0.0")
                entry.set_property('xalign', 1)
                self.fixed1.put(entry, left/10, top/10)
                entry.connect("key-release-event", self._onTabKeyReleased) # bind TAB event
                self.widget_container[numero] = entry
                entry.show()
            #elif c.attrib.get("tipoControl") == "M":# monetario
            #    adjustment = gtk.Adjustment(value=0, lower=0, upper=1000000000, step_incr=1, page_incr=1, page_size=0)
            #    spin = gtk.SpinButton(adjustment=adjustment, climb_rate=0.1, digits=2)
            #    spin.set_numeric(True)
            #    spin.set_size_request(width/10, height/10)
            #    spin.set_tooltip_text(mensajeAyuda)
            #    if editable != "SI":
            #        spin.set_editable(False)
            #    self.fixed1.put(spin, left/10, top/10)
            #    spin.show()
            elif c.attrib.get("tipoControl") == "C":# combo
                combo = gtk.combo_box_new_text()
                combo.set_size_request(width/10, height/10)
                combo.set_tooltip_text(mensajeAyuda)
                if tablaReferencial != "-1":
                    list_store = gtk.ListStore(str, str)
                    combo.set_model(list_store)
                    # llenar combo segun datos referenciales

                    lista_datos = get_data_list(tablaReferencial)

                    for code, name in lista_datos:
                        list_store.append([name, code])

                    combo.set_active(0)
                self.fixed1.put(combo, left/10, top/10)
                self.widget_container[numero] = combo
                combo.show()
    
        
    def post_init(self):
        # poner el titulo de la ventana
        title = self.wndDeclaracion.get_title()
        self.wndDeclaracion.set_title(title)
        # ponel la etiqueta del formulario
        subtitle = self.lblNombreFormulario.get_text()
        self.lblNombreFormulario.set_markup("<b>"+subtitle+"</b>")
        self.wndDeclaracion.maximize()
   

    def generate_xml_from_container(self):

        self.xml = None
    
        root = etree.Element("formulario")
        root.set('version', '0.2' ) # TODO

        cabecera = etree.SubElement(root, "cabecera")
        codigo_version_formulario = etree.SubElement(cabecera, "codigo_version_formulario")
        codigo_version_formulario.text = '04200903' # TODO
        ruc = etree.SubElement(cabecera, "ruc")
        ruc.text = '1002003004001' # TODO
        codigo_moneda = etree.SubElement(cabecera, "codigo_moneda")
        codigo_moneda.text = '1' # TODO

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
        

    def do_calculations(self):
        calcs = Calculator()
        calcs.load_xml('CAL0402.xml')
        calcs.load_xsl('calculos.xsl')
        calcs.calc(self.xml)
        calculations = calcs.get_calculations()

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
        error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format="Los datos no guardados se perderan. Salir?", buttons=gtk.BUTTONS_OK_CANCEL)
        if error_dlg.run() == gtk.RESPONSE_OK:
            self.win.destroy()
        error_dlg.destroy()

    
    def on_btnGuardar_clicked(self, widget, *args):
        dialog = gtk.FileChooserDialog("Guardar ...", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_current_name('test') # TODO generar nombre en base al periodo
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
        gtk.main_quit()


class gDIMM2:

    def __init__(self):
        pass

    def start(self):
        mainWindow = wndDeclaracion()
        mainWindow.set_codigo_formulario('04200901')
        mainWindow.load_widgets_from_xml()
        mainWindow.show()
        gtk.main()



def main():
    app = gDIMM2()
    app.start()

if __name__ == '__main__':
    main()
