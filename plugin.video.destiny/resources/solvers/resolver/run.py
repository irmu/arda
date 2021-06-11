# -*- coding: utf-8 -*-
import os,sys,urllib2
import mediaurl,urlparse
import  threading
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
dir_path = os.path.dirname(os.path.realpath(__file__))
mypath=os.path.join(dir_path,'..')
sys.path.append(mypath)
mypath=os.path.join(dir_path,'..\..\done')
sys.path.append(mypath)
class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)
import requests,re,sys,logging,urllib,json,time,cache
from general import domain_s,cloudflare_request,base_header
try:
  import xbmcgui,xbmc
  local=False
except:
  local=True
global tv_mode
###############################streamango##############################





def resolve_magnet(url):
    import Addon
    allow_rd=Addon.getSetting("rdsource")
    if allow_rd=='true':
        return url
    from kodipopcorntime.torrent import TorrentPlayer
    from kodipopcorntime import settings
    mediaSettings = getattr(settings, 'movies')
    item={'info': {'rating': 0.0, 'plotoutline': 'Elastigirl springs into action to save the day, while Mr. Incredible faces his greatest challenge yet \xe2\x80\x93 taking care of the problems of his three children.', 'code': 'tt3606756', 'director': '', 'studio': '', 'year': 2018, 'genre': 'animation / family / action / adventure / superhero', 'plot': 'Elastigirl springs into action to save the day, while Mr. Incredible faces his greatest challenge yet \xe2\x80\x93 taking care of the problems of his three children.', 'votes': 0.0, 'castandrole': [], 'title': 'Playing', 'tagline': '1080p: 18930 seeds; 720p: 14301 seeds; ', 'writer': '', 'originaltitle': 'Incredibles 2'}, 'thumbnail': 'http://image.tmdb.org/t/p/w500/x1txcDXkcM65gl7w20PwYSxAYah.jpg', 'stream_info': {'subtitle': {'language': ''}, 'audio': {'channels': 2, 'codec': 'aac', 'language': 'en'}, 'video': {'width': 1920, 'codec': 'h264', 'height': 720}}, 'label': 'Incredibles 2', 'properties': {'fanart_image': 'http://image.tmdb.org/t/p/w500/mabuNsGJgRuCTuGqjFkWe1xdu19.jpg'}, 'icon': 'http://image.tmdb.org/t/p/w500/x1txcDXkcM65gl7w20PwYSxAYah.jpg'}
    return TorrentPlayer().playTorrentFile(mediaSettings, url, item, None)
def resolve_lime(url):
    import Addon
    headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    x=requests.get(url,headers=headers).content
    regex='"magnet:(.+?)"'
    url='magnet:'+re.compile(regex).findall(x)[0]
    allow_rd=Addon.getSetting("rdsource")
    if allow_rd=='true':
        return url
    from kodipopcorntime.torrent import TorrentPlayer
    from kodipopcorntime import settings
    mediaSettings = getattr(settings, 'movies')
    item={'info': {'rating': 0.0, 'plotoutline': 'Elastigirl springs into action to save the day, while Mr. Incredible faces his greatest challenge yet \xe2\x80\x93 taking care of the problems of his three children.', 'code': 'tt3606756', 'director': '', 'studio': '', 'year': 2018, 'genre': 'animation / family / action / adventure / superhero', 'plot': 'Elastigirl springs into action to save the day, while Mr. Incredible faces his greatest challenge yet \xe2\x80\x93 taking care of the problems of his three children.', 'votes': 0.0, 'castandrole': [], 'title': 'Playing', 'tagline': '1080p: 18930 seeds; 720p: 14301 seeds; ', 'writer': '', 'originaltitle': 'Incredibles 2'}, 'thumbnail': 'http://image.tmdb.org/t/p/w500/x1txcDXkcM65gl7w20PwYSxAYah.jpg', 'stream_info': {'subtitle': {'language': ''}, 'audio': {'channels': 2, 'codec': 'aac', 'language': 'en'}, 'video': {'width': 1920, 'codec': 'h264', 'height': 720}}, 'label': 'Incredibles 2', 'properties': {'fanart_image': 'http://image.tmdb.org/t/p/w500/mabuNsGJgRuCTuGqjFkWe1xdu19.jpg'}, 'icon': 'http://image.tmdb.org/t/p/w500/x1txcDXkcM65gl7w20PwYSxAYah.jpg'}
    return TorrentPlayer().playTorrentFile(mediaSettings, url, item, None)



    
def resolve_rd(url):
    import resolveurl,xbmc
    #host = url.split('//')[1].replace('www.','')
    
    #debrid = host.split('/')[0].lower()
    
    debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()]
    all_resolve=[]
    for key in debrid_resolvers:
      all_resolve.append(key.name)
    
    #if 'Real-Debrid' not in all_resolve and 'MegaDebrid' not in all_resolve:
       
    #   xbmc.executebuiltin("RunPlugin(plugin://script.module.resolveurl/?mode=auth_rd)")
   
    if len(debrid_resolvers) == 0:

        debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True,include_universal=False) if 'rapidgator.net' in resolver.domains]

    debrid_resolver = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()][0]
 
    debrid_resolver.login()
    _host, _media_id = debrid_resolver.get_host_and_id(url)

    stream_url = debrid_resolver.get_media_url(_host, _media_id)

    return stream_url
    
def direct_resolve(name_check):
       logging.warning('Direct Resolve')
       logging.warning(name_check)
       name_check=name_check.replace('oload.stream','openload.co')
       
       if 'docs.googleusercontent.com' in name_check:
            return name_check
       
       import resolveurl
       if 'google' in name_check and 'view' not in name_check:
            return name_check
       if 'magnet:' in name_check:
            resolvable=False
       else:
            resolvable=resolveurl.HostedMediaFile(name_check).valid_url()
         
       if resolvable:
           link =resolveurl.resolve(name_check)
           
       else:
           link=name_check
       if link==False:
         return name_check
       if link==None:
                link=name_check
       if 'ftp://' in link:
     
          link=urllib.unquote(link)
       return link
       
def get_links(url,tv_m=False):
   import Addon
   global tv_mode
   
   if tv_m:
     tv_mode=True
   else:
     tv_mode=False
   url=url.strip().replace('\n','').replace('\t','').replace('\r','')
   rd_sources=Addon.getSetting("rdsource")
  
   
   if rd_sources=='true' and 'youtube' not in url :
        import resolveurl
        if 'magnet:' in url:
            resolvable_rd=False
        else:
            resolvable_rd=resolveurl.HostedMediaFile(url, include_disabled=True,include_universal=True).valid_url()
        logging.warning('resolvable_rd')
        logging.warning(resolvable_rd)
        
        if resolvable_rd and 'google' not in url:
           try:
             logging.warning('RD resolve: '+url)
             return resolve_rd(url)
           except Exception as e:
             logging.warning('Error Resolveing RD: '+str(e))
             return direct_resolve(url)
        else:
           return direct_resolve(url)
   else:
      
      return direct_resolve(url)
  
   

      
