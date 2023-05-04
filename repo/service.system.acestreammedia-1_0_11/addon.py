import os
import subprocess
import sys
import xbmc
import xbmcaddon
import xbmcgui

def get_disks():
   disks=[]
   acestream_engine = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'acestream.engine')
   script_ismount = os.path.join(acestream_engine,'mount_disk.sh')
   storage = os.path.join(acestream_engine, 'androidfs', 'storage')
   if os.path.exists(script_ismount):
      p = subprocess.Popen([script_ismount, '1'], stdout=subprocess.PIPE)
      names=p.stdout.readline().strip().split()
      for name in names:
         i=names.index(name)
         if (i%2 == 1):
            if name != storage:
               disks.append('{0} ({1})'.format(names[i-1],name))
   else:
      disks.append('default /storage')
   return disks   

def addon():   
   STRINGS  = xbmcaddon.Addon().getLocalizedString
   if sys.argv[1] == 'select_disk':
      dialog  = xbmcgui.Dialog()
      while True:
         names=get_disks()
         index = dialog.select(STRINGS(32126), names)
         if index == -1:
            break
         disk_cache = names[index]
         xbmcaddon.Addon().setSetting('disk_cache', disk_cache)
         break

if __name__ == '__main__':
   addon()
