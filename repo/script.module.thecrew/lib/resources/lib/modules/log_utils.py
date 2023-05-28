# -*- coding: utf-8 -*-

'''
 ***********************************************************
 * The Crew Add-on
 *
 *
 * @file log_utils.py
 * @package script.module.thecrew
 *
 * @copyright (c) 2023, The Crew
 * @license GNU General Public License, version 3 (GPL-3.0)
 *
 ********************************************************cm*
'''

import json
import os
import pstats
import time
from datetime import datetime
import xbmc

import six

from resources.lib.modules import control

LOGDEBUG = xbmc.LOGDEBUG
LOGERROR = xbmc.LOGERROR
LOGFATAL = xbmc.LOGFATAL
LOGINFO = xbmc.LOGINFO
LOGNONE = xbmc.LOGNONE
LOGNOTICE = xbmc.LOGINFO
LOGWARNING = xbmc.LOGWARNING

#addonName = control.addonInfo('name')
addonName = 'The Crew'
DEBUGPREFIX = '[COLOR red][' + addonName + ' - DEBUG ][/COLOR]' if control.setting('debug_in_color') == 'true' else '[ ' + addonName + ' ]'
LOGPATH = control.transPath('special://logpath/')
FILENAME = 'the_crew.log'
LOG_FILE = os.path.join(LOGPATH, FILENAME)
debug_enabled = control.setting('addon_debug')
debug_log = control.setting('debug.location')


def log(msg, level=LOGDEBUG):

    if not debug_enabled:
        return

    try:
        if isinstance(msg, str):
            msg = ('{}').format(str(msg))
        else:
            raise Exception('Logutils.log() msg not of type str!')

        if not debug_log == '0':
            if not os.path.exists(LOG_FILE):
                f = open(LOG_FILE, 'w')
                f.close()
            with open(LOG_FILE, 'a') as f:
                line = ('[{} {}] {}: {}').format(datetime.now().date(), str(datetime.now().time())[:8], DEBUGPREFIX, msg)
                f.write(line.rstrip('\r\n')+'\n\n')
    except Exception as e:
        try:
            xbmc.log('[ The Crew ] Logging Failure: ' + str(e), 2)
        except:
            pass

class Profiler(object):
    def __init__(self, file_path, sort_by='time', builtins=False):
        self._profiler = cProfile.Profile(builtins=builtins)
        self.file_path = file_path
        self.sort_by = sort_by


    def profile(self, f):
        def method_profile_on(*args, **kwargs):
            try:
                self._profiler.enable()
                result = self._profiler.runcall(f, *args, **kwargs)
                self._profiler.disable()
                return result
            except Exception as e:
                log('Profiler Error: %s' % (e), LOGWARNING)
                return f(*args, **kwargs)


        def method_profile_off(*args, **kwargs):
            return f(*args, **kwargs)
        if _is_debugging():
            return method_profile_on
        else:
            return method_profile_off


    def __del__(self):
        self.dump_stats()


    def dump_stats(self):
        if self._profiler is not None:
            s = six.BytesIO
            params = (self.sort_by,) if isinstance(self.sort_by, six.string_types) else self.sort_by
            ps = pstats.Stats(self._profiler, stream=s).sort_stats(*params)
            ps.print_stats()
            if self.file_path is not None:
                with open(self.file_path, 'w') as f:
                    f.write(s.getvalue())


def trace(method):
    def method_trace_on(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        log('{name!r} time: {time:2.4f}s args: |{args!r}| kwargs: |{kwargs!r}|'.format(
            name=method.__name__, time=end - start, args=args, kwargs=kwargs), LOGDEBUG)
        return result

    def method_trace_off(*args, **kwargs):
        return method(*args, **kwargs)

    if _is_debugging():
        return method_trace_on
    else:
        return method_trace_off


def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings',
               'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']

    return False


def execute_jsonrpc(command):
    if not isinstance(command, six.string_types):
        command = json.dumps(command)
    response = control.jsonrpc(command)
    return json.loads(response)