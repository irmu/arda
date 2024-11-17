
import json, sys, os
import shutil
import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
from resources.lib.plugin import Plugin
from resources.lib.plugin import run_hook
from ..DI import DI

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class epg(Plugin):
    name = "epgmad4"
    priority = 100

    def process_item(self, item):
        if "epgmad4" in item:
            link = item.get("epgmad4", "")
            thumbnail = item.get("thumbnail", "")
            fanart = item.get("fanart", "")
            icon = item.get("icon", "")
            if not isinstance(link, list):                
                if link == "epg_setup":
                    item["is_dir"] = False
                    item["link"] = "epgmad4/epg_setup"
                                
                list_item = xbmcgui.ListItem(item.get("title", item.get("name", "")), offscreen=True)
                list_item.setArt({"thumb": thumbnail, "fanart": fanart})
                item["list_item"] = list_item
                return item
                    
    def routes(self, plugin):        
        @plugin.route("/epgmad4/epg_setup")
        def epg_setup():                 
            try : 
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}')   
                xbmc.sleep(100)
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}')
            except :
                xbmcgui.Dialog().ok("Error", "[COLOR red][B]IPTV Simple Client is not installed.\n\n[COLOR red]Please install IPTV Simple Client and re-run this item[/COLOR][/B]")
                return
                        
            addon = xbmcaddon.Addon('pvr.iptvsimple')
            addon_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
            all_instance = [f for f in os.listdir(addon_path) if os.path.isfile(os.path.join(addon_path, f)) and "instance-settings" in f and not "disabled" in f] 
            instance_count = [x.replace(".xml","").split("-")[-1] for x in all_instance] 
            if not instance_count : instance_count=[0] 
            
            instance_count = sorted(instance_count) 
            next_instance = int(instance_count[-1])+1
            instance_file = f"instance-settings-{next_instance}.xml"
            base_instance = "instance-settings-1.xml"
            master_instance = "https://magnetic.website/MAD_TITAN_SPORTS/TOOLS/Pvr_Settings/epg-settings4.xml" 
            
            # xbmcgui.Dialog().ok("[COLOR white]INFORMATION[/COLOR]", f'Instances Found. \n{all_instance}\n{next_instance=}\n{instance_file=}')
                            
            if not xbmcgui.Dialog().yesno("[COLOR white]IPTV Simple Client Setup[/COLOR]", "[COLOR yellow][B]Update IPTV Simple Client settings to use EPG?[/COLOR][/B]"):
                return
            else:            
                pvr_data = DI.session.get(master_instance).text
                # pvr_data = "" 
                if not pvr_data:
                    xbmcgui.Dialog().ok("[COLOR red]WARNING[/COLOR]", "[B]There was a problem loading the EPG Settings Data\n[COLOR yellow]Please Report to Admin in TG Group[/COLOR][/B]")                                     
                    return
                else :
                    pvr_data = pvr_data.replace('EPG Config', f'EPG Config-{next_instance}')
                    with open(os.path.join(addon_path, instance_file), 'w') as f:
                        f.write(pvr_data)
                         
                if xbmcgui.Dialog().yesno("[COLOR white]IPTV Simple Client Setup[/COLOR]", "[COLOR yellow][B]Do you want to disable all existing PVR Guides ? [/COLOR][/B]") :  
                    for file in all_instance :                   
                        if os.path.isfile(os.path.join(addon_path, file)) :                    
                            src = os.path.join(addon_path, file)
                            dst = os.path.join(addon_path, f"disabled-{file}")
                            shutil.copyfile(src, dst)
                            xbmcvfs.delete(os.path.join(addon_path, file))                          
       
                if os.path.isfile(os.path.join(addon_path, "settings.xml")) :                        
                    xbmcvfs.delete(os.path.join(addon_path, "settings.xml"))     
                    
                xbmcgui.Dialog().ok("[COLOR white]Success[/COLOR]", "[COLOR yellow][B]EPG enabled. \n\n[COLOR red]KODI will now Force Close.[/COLOR][/B]")                                  
                xbmc.executebuiltin("Quit")
                # os._exit(1)
            


