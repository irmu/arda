# -*- coding: utf-8 -*-
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info), PlatformCode y Core del Grupo Balandro (https://linktr.ee/balandro)

import os, sys, urllib, re, shutil, zipfile, base64
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import locale, time, random, plugintools
import resolvers

if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.error as urllib2

from core import httptools
from core.item import Item
from platformcode.config import WebErrorException

actualiza  = xbmc.translatePath(os.path.join(base64.b64decode("c3BlY2lhbDovL2hvbWUvYWRkb25zL3BsdWdpbi52aWRlby5GdXRib2xUcmVhbS9taV9kZWZhdWx0LnB5".encode('utf-8')).decode('utf-8')))
pyo  = xbmc.translatePath(os.path.join(base64.b64decode("c3BlY2lhbDovL2hvbWUvYWRkb25zL3BsdWdpbi52aWRlby5GdXRib2xUcmVhbS9taV9kZWZhdWx0LnB5bw==".encode('utf-8')).decode('utf-8')))

if sys.version_info[0] < 3:
    v = open( actualiza, "r" )
else:
    v = open( actualiza, "r", encoding='utf-8' )

cod_Local = v.read()
v.close()

datosConf = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0FjZVRvcnIvZnV0dHJlYW0vbWFpbi9EYXRvc0NvbmY=".encode('utf-8')).decode('utf-8')).data

if not "<FutbolTream2>" in datosConf:
    datosConf = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yZW50cnkuY28veHM2YmYvcmF3".encode('utf-8')).decode('utf-8')).data

comparaVersion = plugintools.find_single_match(cod_Local,'comparaVersion="(.*?)"')
versionActual = plugintools.find_single_match(datosConf,'VersionFutbolTream>(.*?)<Fin')

if versionActual > comparaVersion:
    try:
        cod1 = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0FjZVRvcnIvZnV0dHJlYW0vbWFpbi9taURlZmF1bHQ=".encode('utf-8')).decode('utf-8')).data
    except:
        cod1 = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yZW50cnkuY28vZGdoOXkvcmF3".encode('utf-8')).decode('utf-8')).data

    codigo = cod1.replace("\r\n" , "\n").replace("œ" , "")

    if os.path.isfile(pyo): os.remove(pyo)

    if sys.version_info[0] < 3:
        fichero = open(actualiza, "wb")
    else:
        fichero = open(actualiza, "w", encoding='utf-8') #En Python 3 da error abrir con "wb", así q lo hago con w y con codificación utf-8
    fichero.write(codigo)
    fichero.close()





from mi_default import *

	

# Punto de Entrada
def run():
	plugintools.log('[%s %s] Running %s... ' % (addonName, addonVersion, addonName))

	# Obteniendo parámetros...
	params = plugintools.get_params()
    
	
	if params.get("action") is None:
		main_list(params)
	else:
		action = params.get("action")
		exec(action+"(params)")
        

	plugintools.close_item_list()            



# Principal
def main_list(params):
    
    miDefault(params)
	



	


	


		
run()

		




	

