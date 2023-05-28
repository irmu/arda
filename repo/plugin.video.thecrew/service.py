# -*- coding: utf-8 -*-

'''
 ***********************************************************
 * The Crew Add-on
 *
 *
 * @file tvshows.py
 * @package script.module.thecrew
 *
 * @copyright (c) 2023, The Crew
 * @license GNU General Public License, version 3 (GPL-3.0)
 *
 ********************************************************cm*
'''

import shutil
import xbmc
import threading
import os

from resources.lib.modules import control
from resources.lib.modules import log_utils


def conversion():
    control.infoDialog('Checking Conversion', sound=False, icon='INFO')
    conversionFile = os.path.join(control.dataPath, 'conversion.v')
    bookmarkFile = control.bookmarksFile
    curVersion = control.addon('script.module.thecrew').getAddonInfo('version')

    if os.path.exists(conversionFile):
        control.infoDialog('You are fine, running version ' + str(curVersion) + ' Continuing...', sound=False, icon='INFO')
    else:
        f_path = 'special://home/addons/script.thecrew.metadata'
        shutil.rmtree(f_path, ignore_errors=True)

        if os.path.isfile(bookmarkFile):
            os.remove(bookmarkFile)
            log_utils.log('removing ' + str(bookmarkFile))

        if os.path.isfile(bookmarkFile):
            log_utils.log('Conversion Failed')
            control.infoDialog('Conversion failed')
        else:
            #write the conversion.v file
            log_utils.log('Conversion Done')
            with open(conversionFile, 'w') as fh: 
                fh.write(curVersion)
            log_utils.log('File written')
            control.infoDialog('Conversion done')
            log_utils.log('Conversion Done')



def syncTraktLibrary():
    control.execute('RunPlugin(plugin://plugin.video.thecrew/?action=tvshowsToLibrarySilent&url=traktcollection')
    control.execute('RunPlugin(plugin://plugin.video.thecrew/?action=moviesToLibrarySilent&url=traktcollection')

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

monitor = control.monitor

control.startupMaintenance()

try:
    conversion()
    monitor.waitForAbort(30)
    if control.setting('autoTraktOnStart') == 'true':
        syncTraktLibrary()

    if int(control.setting('schedTraktTime')) > 0:
        
        timeout = 3600 * int(control.setting('schedTraktTime'))
        monitor.waitForAbort(timeout)  # sleeps for time set in timeout or returns early if kodi aborts
        log_utils.log('---------------------------------------------------------------')
        log_utils.log('-------------------- Starting trakt scheduling ----------------')
        log_utils.log('-------------------- Scheduled time frame: ' + hours + ' hours ------------')
        log_utils.log('---------------------------------------------------------------')
        syncTraktLibrary()

        if monitor.abortRequested():
            # abort was requested to Kodi (e.g. shutdown), do your cleanup logic
            #log_utils.log('[CM DEBUG @ 135 in service] monitor abort requested')
            del monitor

except Exception as e:
    import traceback
    failure = traceback.format_exc()
    log_utils.log('[CM Debug @ 89 in service.py]Traceback:: ' + str(failure))
    log_utils.log('[CM Debug @ 90 in service.py]Exception raised. Error = ' + str(e))
    log_utils.log('[CM DEBUG @ 91 in service] exception raised')
    pass

finally:
    log_utils.log('[ plugin.video.thecrew ] monitor stopped gracefully.')
    del monitor
