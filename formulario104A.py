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


ezGlade.set_file(configuration.GLADE_FILE)


class wndDeclaracion(ezGlade.BaseWindow):
    
    codigo = None

    def set_codigo_formulario(self, codigo):
        self.codigo = codigo 
    
    
    def load_widgets_from_xml(self):
        if not self.codigo :
            print 'Codigo de formulario no definido.'
            return;
        tree = etree.parse(os.path.join('XML','CMPFRM-GNU.xml'))
        
        # formulario 104A
        form = tree.find("version[@codigo='"+self.codigo+"']") 

        for c in form:
            top = int(c.attrib.get("top"))
            left = int(c.attrib.get("left"))
            width = int(c.attrib.get("width"))
            height = int(c.attrib.get("height"))
            label = c.attrib.get("etiqueta")
            bold = c.attrib.get("fontBold")
            editable = c.attrib.get("editable")
            tablaReferencial = c.attrib.get("tablaReferencial")
            if c.attrib.get("tipoControl") == "L": # etiqueta
                lbl = gtk.Label(label)
                if bold != "Falso":
                    lbl.set_markup("<b>"+label+"</b>")
                self.fixed1.put(lbl, left/10, top/10)
                lbl.show()
            elif c.attrib.get("tipoControl") == "T": # caja de texto
                entry = gtk.Entry(max=0)
                entry.set_size_request(width/10, height/10)
                if editable == "Falso":
                    entry.set_editable(False)
                entry.set_text("0.0")
                entry.set_property('xalign', 1)
                self.fixed1.put(entry, left/10, top/10)
                entry.show()
            elif c.attrib.get("tipoControl") == "M":# monetario
                adjustment = gtk.Adjustment(value=0, lower=0, upper=1000000000, step_incr=1, page_incr=1, page_size=0)
                spin = gtk.SpinButton(adjustment=adjustment, climb_rate=0.1, digits=2)
                spin.set_numeric(True)
                spin.set_size_request(width/10, height/10)
                if editable == "Falso":
                    spin.set_editable(False)
                self.fixed1.put(spin, left/10, top/10)
                spin.show()
            elif c.attrib.get("tipoControl") == "C":# combo
                combo = gtk.combo_box_new_text()
                combo.set_size_request(width/10, height/10)
                if tablaReferencial != "-1":
                    # llenar combo segun XML
                    lista_datos = get_data_list(tablaReferencial)
                    for elemento in lista_datos:
                        combo.append_text(elemento[1])
                self.fixed1.put(combo, left/10, top/10)
                combo.show()
    
        
    def post_init(self):
        # poner el titulo de la ventana
        title = self.wndDeclaracion.get_title()
        self.wndDeclaracion.set_title(title)
        # ponel la etiqueta del formulario
        subtitle = self.lblNombreFormulario.get_text()
        self.lblNombreFormulario.set_markup("<b>"+subtitle+"</b>")
        self.wndDeclaracion.maximize()


    def on_btnCancel_clicked(self, widget, *args):
        # verificar si se han guardado los cambios!!!
        error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format="Los datos no guardados se perderan. Salir?", buttons=gtk.BUTTONS_OK_CANCEL)
        if error_dlg.run() == gtk.RESPONSE_OK:
            self.win.destroy()
        error_dlg.destroy()
        
        
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
