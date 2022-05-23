# -*- coding: UTF-8 -*-


#######################################################################
#
# autoexec cristalazul
# ----------------------------------------------------------------------------
# Modificación eliminar indigo del sistema. Proveedor: CTA
# ----------------------------------------------------------------------------
#######################################################################

import shutil
import six
from kodi_six import xbmc,xbmcvfs
TRANSLATEPATH = xbmc.translatePath if six.PY2 else xbmcvfs.translatePath

try:
    addon_path2 = TRANSLATEPATH(('special://home/addons/plugin.video.blackghost'))
    addon_path2 = six.ensure_str(addon_path2)
    shutil.rmtree(addon_path2, ignore_errors=True)
except:
    pass
	
instalado = xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)')
if instalado==0:
    xbmc.executebuiltin('InstallAddon(script.module.resolveurl)')