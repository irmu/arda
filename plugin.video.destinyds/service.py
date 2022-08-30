# -*- coding: utf-8 -*-
import xbmc,time,xbmcaddon,os,requests,xbmcgui,re,logging,threading,urllib,json,datetime



Addon = xbmcaddon.Addon()


from resources.scrapers.globals import *

from resources.done import cache
global current_list_item,list_index
list_index=999
current_list_item=''
from default import nextup,show_sources,done_nextup
class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)
        
def post_trakt(path,data=None, with_auth=True):
    import urllib
    API_ENDPOINT = "https://api-v2launch.trakt.tv"
    CLIENT_ID = "8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6"
    SETTING_TRAKT_ACCESS_TOKEN = "trakt_access_token"
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': CLIENT_ID
    }


    
    if with_auth:
           
            token =unicode( Addon.getSetting(SETTING_TRAKT_ACCESS_TOKEN))
            headers.update({'Authorization': 'Bearer %s' % token})
            
        
            return requests.post("{0}/{1}".format(API_ENDPOINT, path), json=(data), headers=headers).content
def similar(w1, w2):
    from difflib import SequenceMatcher
    
    s = SequenceMatcher(None, w1, w2)
    return int(round(s.ratio()*100))
def check_pre(saved_name,all_subs):
       release_names=['bluray','hdtv','dvdrip','bdrip','web-dl']
       array_original=list(saved_name)
       array_original=[line.strip().lower() for line in array_original]
       array_original=[(x) for x in array_original if x != '']
       highest=0
       for items in all_subs:
           array_subs=list(items)
          
           array_subs=[line.strip().lower() for line in array_subs]
           array_subs=[str(x).lower() for x in array_subs if x != '']
           
     
           for item_2 in release_names:
           
            if item_2 in array_original and item_2 in array_subs:
              array_original.append(item_2)
              array_original.append(item_2)
              array_original.append(item_2)
              array_subs.append(item_2)
              array_subs.append(item_2)
              array_subs.append(item_2)
    
     
           precent=similar(array_original,array_subs)
           
           if precent>=highest:
             highest=precent
       return highest
def fix_q(quality):
    f_q=100
    if '2160' in quality:
      f_q=1
    if '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=5
    elif '360' in quality or 'sd' in quality.lower():
      f_q=6
    elif '240' in quality:
      f_q=7
    return f_q




logging.warning('Nextup Service Started')

done_p=0
marked_trk=0
counter_no_play=0
START=True
def SetTimer(delta):
    return datetime.datetime.now() + datetime.timedelta(seconds=delta)
    


while not xbmc.abortRequested:
   
    START=False
    if xbmc.Player().isPlaying():
        counter_no_play=0
        try:
            time_to_window=int(Addon.getSetting("window"))
        except:
            time_to_window=30
        current_list_item_pre=(xbmc.getInfoLabel("VideoPlayer.Plot"))
        
        if len(current_list_item_pre)>0:
            current_list_item=current_list_item_pre
            
     
        
        if '_from_Destiny_' in current_list_item and '-KIDSSECTION-' not in current_list_item and '__aceplay__' not in current_list_item:
           try:
            
            time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
            if xbmc.Player().getTotalTime()>600:
                avg=(xbmc.Player().getTime()*100)/xbmc.Player().getTotalTime()
                time_to_save_trk=int(Addon.getSetting("time_to_save"))
                if Addon.getSetting("use_trak")=='true' and avg>time_to_save_trk and marked_trk==0:
                     dbcur.execute("SELECT * FROM sources")

                     match = dbcur.fetchone()
                     name,url,icon,image,plot,year,season,episode,original_title,heb_name,show_original_year,eng_name,isr,id=match
                    
                     if len(id)>1 and id!='%20':
                         if season!=None and season!="%20":
                           '''
                           logging.warning('tv')
                           logging.warning(imdb_id)
                           url_pre='http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s&language=en'%imdb_id.replace('tt','')
                           html2=requests.get(url_pre).content
                           pre_tvdb = str(html2).split('<seriesid>')
                           if len(pre_tvdb) > 1:
                                tvdb = str(pre_tvdb[1]).split('</seriesid>')
                           logging.warning(tvdb)
                           '''
                           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
                           
                           i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
                         else:
                           
                           i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
                     marked_trk=1
            
            
            if time_left<time_to_window and time_left>0  and xbmc.Player().getTotalTime()>600:#only if longer then 10min
                if 'channel' not in current_list_item:
                    result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": { "properties": [ "showlink", "showtitle", "season", "title", "artist" ], "playlistid": 1}, "id": 1}')

                    j_list=json.loads(result)
                    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                    playlist.clear()
                        
                    if 'items' in (j_list['result']):
                        
                        result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": { "playlistid": 0 }, "id": 1}')
                        logging.warning('clearing playlist')
                if Addon.getSetting('nextup')=='true' and done_nextup==0:
                 
                 
                 nextup()
                
                 done_nextup=1
                 xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            if  done_p==0:
            
                if xbmc.getCondVisibility("Player.Paused")==True :
                     done_p=1
                     xbmc.sleep(1000)
                     windoid=xbmcgui.getCurrentWindowDialogId()
                    
                     
                     if Addon.getSetting('show_p2')=='true' and windoid!=10101 and windoid!=10153:
                       
                         show_sources()
                     
                     
            if xbmc.getCondVisibility("Player.Paused")==False :
                   done_p=0
           
           except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)

            logging.warning('ERROR IN NEXTUP:'+str(lineno))
            logging.warning('inline:'+line)
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno))).encode('utf-8'))
            done_nextup=1
            marked_trk=1
            
            pass
           
        
    else:
       if counter_no_play<10:
            counter_no_play+=1
      
       if counter_no_play==5:
        
       
        if 'channel' not in current_list_item and '_from_Destiny_' in current_list_item:
            result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": { "properties": [ "showlink", "showtitle", "season", "title", "artist" ], "playlistid": 1}, "id": 1}')

            j_list=json.loads(result)
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            if 'items' in (j_list['result']):
                
                result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": { "playlistid": 0 }, "id": 1}')
        current_list_item=''
       done_nextup=0
       marked_trk=0
       
       
    xbmc.sleep(1000)

               
                             