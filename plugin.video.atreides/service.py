# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Welcome to House Atreides.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.module.atreides
# Addon Provider: House Atreides

import glob
import os
import re
import traceback

import xbmc
import xbmcgui
import xbmcaddon

from xbmc import (LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO,
                  LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING)

addon_name = 'Atreides'
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
addon_path = xbmc.translatePath(('special://home/addons/plugin.video.atreides')).decode('utf-8')
module_path = xbmc.translatePath(('special://home/addons/script.module.atreides')).decode('utf-8')


def main():
    fum_ver = xbmcaddon.Addon(id='script.module.atreides').getAddonInfo('version')
    updated = xbmcaddon.Addon(id='plugin.video.atreides').getSetting('module_base')
    if updated == '' or updated is None:
        updated = '0'

    if str(fum_ver) == str(updated):
        return

    xbmcgui.Dialog().notification(addon_name, 'Gathering scraper details', addon_icon)
    defaults_xml_path = os.path.join(addon_path, 'resources/defaults.xml')
    settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
    try:
        xml = openfile(defaults_xml_path)
    except Exception:
        failure = traceback.format_exc()
        log('Atreides Service - Exception: \n %s' % (str(failure)), LOGINFO)
        return

    '''
    First let's check for WWW scrapers
    '''
    scraper_path = os.path.join(module_path, 'lib/resources/lib/sources/www')
    log('Atreides Scraper Path: %s' % (str(scraper_path)), LOGINFO)

    new_settings = []
    new_settings = '<category label="32345">\n'
    new_settings += '        <setting type="lsep" label="32643" />\n'
    for file in glob.glob("%s/*.py" % (scraper_path)):
        file = os.path.basename(file)
        if '__init__' not in file:
            file = file.replace('.py', '')
            new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (
                file.lower(), file.upper())

    '''
    Now we check for the Open Directory scrapers
    '''
    scraper_path = os.path.join(module_path, 'lib/resources/lib/sources/openlist')
    log('Atreides Scraper Path: %s' % (str(scraper_path)), LOGINFO)

    new_settings += '        <setting type="lsep" label="32645" />\n'
    for file in glob.glob("%s/*.py" % (scraper_path)):
        file = os.path.basename(file)
        if '__init__' not in file:
            file = file.replace('.py', '')
            new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (
                file.lower(), file.upper())

    '''
    Now we check for the Torrent scrapers
    '''
    scraper_path = os.path.join(module_path, 'lib/resources/lib/sources/magnet')
    log('Atreides Scraper Path: %s' % (str(scraper_path)), LOGINFO)

    new_settings += '        <setting type="lsep" label="32644" />\n'
    for file in glob.glob("%s/*.py" % (scraper_path)):
        file = os.path.basename(file)
        if '__init__' not in file:
            file = file.replace('.py', '')
            new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (
                file.lower(), file.upper())

    '''
    Done, SET THE PUPPIES FREE!
    '''
    new_settings += '    </category>'

    xml = xml.replace('<category label="32345"></category>', str(new_settings))
    savefile(settings_xml_path, xml)

    xbmcaddon.Addon(id='plugin.video.atreides').setSetting('module_base', fum_ver)
    xbmcgui.Dialog().notification(addon_name, 'Scraper settings updated', addon_icon)


def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'rb')
        contents = fh.read()
        fh.close()
        return contents
    except Exception:
        failure = traceback.format_exc()
        print('Service Open File Exception - %s \n %s' % (path_to_the_file, str(failure)))
        return None


def savefile(path_to_the_file, content):
    try:
        fh = open(path_to_the_file, 'wb')
        fh.write(content)
        fh.close()
    except Exception:
        failure = traceback.format_exc()
        print('Service Save File Exception - %s \n %s' % (path_to_the_file, str(failure)))


DEBUGPREFIX = '[COLOR red][ ATREIDES DEBUG ][/COLOR]'


def log(msg, level=LOGNOTICE):

    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))
        print('%s: %s' % (DEBUGPREFIX, msg))
    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), level)
        except Exception:
            pass


if __name__ == '__main__':
    main()
