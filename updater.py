#!/usr/bin/env python
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


import urllib2 
import os, glob
import shutil
from zipfile import ZipFile
from distutils import dir_util
from time import strptime, strftime, mktime
from datetime import date, datetime
from lxml import etree

""" Actualizador del sistema. """
class gDimmUpdater:
    
    download_url = 'http://descargas.sri.gov.ec/download/declaraciones/ActuDimm.zip'

    download_dest_file_path = os.path.join('updates', 'update.zip')

    unzipped_dest_path  = os.path.join('updates', 'update')

    lastupdate_xml_file = os.path.join('updates', 'last_update.xml')

    last_update = None

    def __init__(self):
        pass


    def need_update(self):
        """ Verifica si es necesario actualizar el sistema """
        remotefile = urllib2.urlopen(self.download_url)
        file_info = remotefile.info()
        last_mod = file_info['Last-Modified']

        date_object = strptime(last_mod, "%a, %d %b %Y %H:%M:%S GMT")

        remote_file_date = date(date_object.tm_year, date_object.tm_mon, date_object.tm_mday).isoformat()

        if not os.path.isfile(self.lastupdate_xml_file):
            self._create_last_update_file(str(date.today()))

        parser = etree.XMLParser(remove_comments=True, encoding='utf8')
        xml = etree.parse(self.lastupdate_xml_file, parser)
        root = xml.getroot()
        last_update = root.attrib.get('last_update')

        if remote_file_date != last_update:
            print remote_file_date, '!=', last_update, 'update needed!'
            self.last_update = remote_file_date
            return True

        return False


    def download(self):
        """ Descarga el archivo de actualizacion """
        if os.path.isfile(self.download_dest_file_path):
            os.remove(self.download_dest_file_path)            

        mysock = urllib2.urlopen(self.download_url)
        fileToSave = mysock.read()
        oFile = open(self.download_dest_file_path, 'wb')
        oFile.write(fileToSave)
        oFile.close()


    def unzip(self):
        """ Descomprime los archivos """
        zipfile = ZipFile(self.download_dest_file_path)

        if not os.path.isdir(self.unzipped_dest_path):
            os.makedirs(self.unzipped_dest_path, mode=0700)

        zipfile.extractall(self.unzipped_dest_path)


    def copy_files(self):
        """ Reemplaza los nuevos archivos XML """
        dir_util.copy_tree(os.path.join(self.unzipped_dest_path, 'XML'), os.path.join('XML'))
        dir_util.copy_tree(os.path.join(self.unzipped_dest_path, 'XSL'), os.path.join('XSL'))
        shutil.rmtree(self.unzipped_dest_path)
        # ajustar las extensiones .XML --> .xml
        self._update_extensions()


    def update(self):
        """ Ejecuta la actualizacion de los XML """
        if not self.need_update():
            print 'Actualizacion no necesaria.'
            return
        
        print 'Descargando...'
        self.download()
        print 'Desempaquetando...'
        self.unzip()
        print 'Copiando archivos...'
        self.copy_files()
        print 'Actualizando archivo...'
        self._create_last_update_file()


    def _create_last_update_file(self, update_date=None):
        """ Crea el archivo de referencia con la ultima actualizacion realizada """
        if update_date is None:
            update_date = self.last_update

        root = etree.Element("root")
        root.set('last_update', update_date)

        f = open(self.lastupdate_xml_file, 'w+')
        f.write(etree.tostring(root, encoding='utf8', pretty_print=True))
        f.close()


    def _update_extensions(self):
        files = glob.glob(os.path.join('XML', '*.XML'))
        files += glob.glob(os.path.join('XSL', '*.XML'))
        for filepath in files:
            (root, ext) = os.path.splitext(filepath)
            os.rename(root + ext, root + ext.lower())
        


# tests
if __name__ == '__main__':
    updater = gDimmUpdater()
    updater.update()


    


