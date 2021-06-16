################################################################################
#      This file is part of LibreELEC - https://libreelec.tv
#      Copyright (C) 2016 Team LibreELEC
#
#  LibreELEC is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  LibreELEC is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with LibreELEC.  If not, see <http://www.gnu.org/licenses/>.
################################################################################


import subprocess
import xbmc
import xbmcaddon
import xbmcgui
import pickle
import os
import addon


class Monitor(xbmc.Monitor):

   def __init__(self, *args, **kwargs):
      xbmc.Monitor.__init__(self)
      self.id = xbmcaddon.Addon().getAddonInfo('id')
      self.path = xbmcaddon.Addon().getAddonInfo('path')
      self.acestream_engine = os.path.join(self.path, 'acestream.engine','androidfs','acestream.engine')
      self.addonname = xbmcaddon.Addon().getAddonInfo('name')
      self.update()

   def onSettingsChanged(self):
      self.update()
      subprocess.call(['systemctl', 'restart', self.id])

   def update(self):
      try:
         disk_cache = xbmcaddon.Addon().getSetting('disk_cache')
         disks = addon.get_disks()
         f = disk_cache in disks
         if f == 0:
            line1 = "Drive \"" + disk_cache + "\" is not in the system! The default disc will be automatically installed!"
            xbmcgui.Dialog().ok(self.addonname, line1)
            xbmcaddon.Addon().setSetting('disk_cache', 'default (/storage)')
      except OSError:
         pass
      self.createAcestreamConf()
      self.createPlayerConfPickle()

   def createPlayerConfPickle(self):
      pickle_data = {'ad_storage_limit':1073741824, \
      'download_dir':'/storage/.ACEStream/.acestream_cache', \
      'live_cache_type':self.param('live_cache_type'), \
      'vod_cache_type':self.param('vod_cache_type'), \
      'max_connects':int(self.param('max_connects')), \
      'total_max_upload_rate':int(self.param('total_max_upload_rate')), \
      'total_max_download_rate':int(self.param('total_max_download_rate')), \
      'disk_cache_limit':1024*1024*1024*int(self.param('disk_cache_limit')), \
      'playlist_output_format_vod':self.param('playlist_output_format_vod'), \
      'playlist_output_format_live':self.param('playlist_output_format_live'), \
      'max_peers':int(self.param('max_peers')), \
      'memory_cache_limit':1024*1024*int(self.param('memory_cache_limit')), \
      'live_buffer_time':int(self.param('live_buffer_time')), \
      'player_buffer_time':int(self.param('player_buffer_time')), \
      'transcode_audio':0 if self.param('transcode_audio') == 'false' else 1, \
      'transcode_ac3':0 if self.param('transcode_ac3') == 'false' else 1, \
      'transcode_mp3':0 if self.param('transcode_mp3') == 'false' else 1, \
      'auto_sync':0 if self.param('auto_sync') == 'false' else 1, \
      'preferred_video_quality':self.param('preferred_video_quality'), \
      'preferred_video_bitrate':self.param('preferred_video_bitrate')}
      ACEStream = os.path.join(self.acestream_engine,'.ACEStream')
      if not os.path.exists(ACEStream):
         os.makedirs(ACEStream)
      file = open(os.path.join(ACEStream,'playerconf.pickle'), 'wt')
      file.write(pickle.dumps(pickle_data,0))
      file.close()
   
   def createAcestreamConf(self):
      arg = \
      '--client-console' + '\n' + \
      '--login' + '\n' + self.param('login') + '\n' + \
      '--password' + '\n' + self.param('password') + '\n' + \
      '--bind-all' + '\n' + \
      '--access-token' + '\n' + self.param('access_token') + '\n' + \
      '--cache-dir' + '\n' + '/storage/.ACEStream' + '\n' + \
      '--vod-drop-max-age' + '\n' + '120' + '\n' + \
      '--max-file-size' + '\n' + '2147483648' + '\n' + \
      '--max-peers-limit' + '\n' + '50' + '\n' + \
      '--max-upload-slots' + '\n' + '30' + '\n' + \
      '--stats-report-interval' + '\n' + '1' + '\n' + \
      '--slots-manager-use-cpu-limit' + '\n' + '1' + '\n' + \
      '--core-dlr-periodic-check-interval' + '\n' + '3' + '\n' + \
      '--check-live-pos-interval' + '\n' + '3' + '\n' + \
      '--refill-buffer-interval' + '\n' + '2' + '\n' + \
      '--core-skip-have-before-playback-pos' + '\n' + '1' + '\n' + \
      '--webrtc-allow-outgoing-connections' + '\n' + '1' + '\n' + \
      '--allow-user-config' + '\n'
      if self.param('is_debug') == 'true':
         arg += '--log-debug\n1\n--log-modules\nroot:D\n--debug-profile\n'
      else:
         arg += '--log-debug\n0'
      file = open(os.path.join(self.acestream_engine,'acestream.conf'), 'wt')
      file.write(arg)
      file.close()

   def param(self, param):
      return xbmcaddon.Addon().getSetting(param)

if __name__ == "__main__":
   Monitor().waitForAbort()
