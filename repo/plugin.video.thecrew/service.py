# -*- coding: utf-8 -*-

'''
 ***********************************************************
 * The Crew Add-on
 *
 *
 * @file service.py
 * @package plugin.video.thecrew
 *
 * @copyright (c) 2023, The Crew
 * @license GNU General Public License, version 3 (GPL-3.0)
 *
 ********************************************************cm*
'''



# CM - 06/07/2021
# cm - 06/20/2023
# cm - testfile VS without mocking (just useless)
# pylint: disable=import-error
# pylint: disable=no-name-in-module
import os
import re
import traceback
import glob

from shutil import rmtree
from resources.lib.modules import control

from resources.lib.modules.crewruntime import c

import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon




def conversion():
    if c.has_silent_boot:
        c.log('Checking Conversion')
    else:
        control.infoDialog('Checking Conversion', sound=False, icon='INFO')
    conversionFile = os.path.join(control.dataPath, 'conversion.v')
    bookmarkFile = control.bookmarksFile
    #curVersion = str(control.addon('script.module.thecrew').getAddonInfo('version'))
    curVersion = c.moduleversion
    version = c.pluginversion

    if os.path.exists(conversionFile):
        if c.has_silent_boot:
            c.log(f"You are fine, running module {curVersion} (video: {version}), Continuing...")
        else:
            control.infoDialog(f"You are fine, running module {curVersion} (video: {version}), Continuing...", sound=False)
    else:
        f_path = 'special://home/addons/script.thecrew.metadata'
        rmtree(f_path, ignore_errors=True)

        if os.path.isfile(bookmarkFile):
            os.remove(bookmarkFile)
            c.log('removing ' + str(bookmarkFile))

        if os.path.isfile(bookmarkFile):
            if c.has_silent_boot:
                c.log(f"Conversion failed on [os.path.isFile(bookmarkFile)]")
            else:
                control.infoDialog('Conversion failed')
        else:
            #write the conversion.v file
            with open(conversionFile, 'w') as fh:
                fh.write(curVersion)
            c.log('File written')
            if c.has_silent_boot:
                c.log(f"Conversion successful")
            else:
                control.infoDialog('Conversion succesful')


def readProviders(scraper_path_fill, msg1, catnr):
    addon_name = c.name
    addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
    addon_path = xbmcvfs.translatePath('special://home/addons/plugin.video.thecrew')
    module_path = xbmcvfs.translatePath('special://home/addons/script.module.thecrew')


    xbmc.log(f"[ plugin.video.thecrew ] service - checking {msg1} providers started")

    if c.has_silent_boot:
        c.log(f"Preparing {msg1} Providers")
    else:
        xbmcgui.Dialog().notification(addon_name, f"Preparing {msg1} Providers", addon_icon)

    settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
    scraper_path = os.path.join(module_path, 'lib/resources/lib/sources/' + scraper_path_fill)
    try:
        xml = openfile(settings_xml_path)
    except Exception as e:
        failure = str(traceback.format_exc())
        c.log(f"The Crew Service - Exception: \n {failure}")
        return

    new_settings = '\n'
    for file in glob.glob("%s/*.py" % (scraper_path)):
        file = os.path.basename(file)
        if not '__init__' in file:
            file = file.replace('.py', '')
            new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (file.lower(), file.upper())
        new_settings += '    '

    pattern = ('<category label="{}">').format(str(catnr)) + '([\s\S]*?)<\/category>'
    found = re.findall(pattern, xml, flags=re.DOTALL) # pyright: ignore [reportGeneralTypeIssues]

    xml = xml.replace(found[0], new_settings) #pyright: ignore
    savefile(settings_xml_path, xml)
    if c.has_silent_boot:
        c.log(f"{msg1} Providers Updated")
    else:
        xbmcgui.Dialog().notification(addon_name, f"{msg1} Providers Updated", addon_icon)


def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'r')
        contents = fh.read()
        fh.close()
        return contents
    except Exception as e:
        failure = str(traceback.format_exc())
        c.log(f"Service Open File Exception - {path_to_the_file} \n {failure}")
        return None


def savefile(path_to_the_file, content):
    try:
        fh = open(path_to_the_file, 'w')
        fh.write(content)
        fh.close()
    except Exception as e:
        failure = str(traceback.format_exc())
        c.log(f"Service Save File Exception - {path_to_the_file} \n {failure}")



def syncTraktLibrary():
    control.execute('RunPlugin(plugin://plugin.video.thecrew/?action=tvshowsToLibrarySilent&url=traktcollection')
    control.execute('RunPlugin(plugin://plugin.video.thecrew/?action=moviesToLibrarySilent&url=traktcollection')


def main():

    monitor = xbmc.Monitor()

    try:
        c.log_boot_option()
        hours = control.setting('schedTraktTime')
        _timeout = 3600 * int(hours)

        # cm -conversion check and fix from module v. 1.x to v. > 2.0.0
        c.initialize_all()
        conversion()

        # cm - waiting 30 secs for widgets to load
        monitor.waitForAbort(30)        
        control.startupMaintenance()

        #cm - checking the scrapers
        fum_ver = xbmcaddon.Addon('script.module.thecrew').getAddonInfo('version')
        updated = xbmcaddon.Addon('plugin.video.thecrew').getSetting('module_base')
        if not updated: 
            updated = '0'

        checks = ['en|Free|32345','en_de|Debrid|90004','en_tor|Torrent|90005']
        for check in checks:
            items = check.split('|')
            scraper_path_fill = items[0] ; msg1 = items[1] ; catnr = items[2]
            readProviders(scraper_path_fill, msg1, catnr)

        xbmcaddon.Addon('plugin.video.thecrew').setSetting('module_base', fum_ver)
        c.log('Providers done')

        if control.setting('autoTraktOnStart') == 'true':
            c.log('autoTraktOnStart Enabled: synctraktlib started')
            syncTraktLibrary()

        if int(control.setting('schedTraktTime')) > 0:
            c.log(f"Starting schedTrakTime with setting={hours} hrs")

            while not monitor.abortRequested():
                # Sleep/wait for abort for 10 seconds
                if monitor.waitForAbort(timeout=_timeout):
                    # Abort was requested while waiting. We should exit
                    break
                c.log('Starting trakt scheduling')
                c.log(f"Scheduled time frame: {hours} hours")
                syncTraktLibrary()
           
    except Exception as e:
        import traceback
        failure = traceback.format_exc()
        c.log('[CM Debug @ 204 in service.py]Traceback:: ' + str(failure))
        c.log('[CM Debug @ 205 in service.py]Exception raised. Error = ' + str(e))
        pass

    finally:
        c.log('monitor passing finally')
        del monitor



control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

if __name__ == '__main__':
    main()

