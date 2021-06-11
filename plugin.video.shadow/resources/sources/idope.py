# -*- coding: utf-8 -*-
import re
import time
from  resources.modules.client import get_html
global global_var,stop_all#global
global_var=[]
stop_all=0

 
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon
except:
  import Addon
type=['movie','tv','torrent']

import urllib2,urllib,logging,base64,json

def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    if tv_movie=='tv':
        cat='3'
    elif tv_movie=='movie':
        cat='1'
    else:
        cat='1'
    if tv_movie=='movie':
     search_url=[('%s+%s'%(clean_name(original_title,1).replace(' ','+'),show_original_year)).lower()]
    elif tv_movie=='tv':
     if Addon.getSetting('debrid_select')=='0' :
        search_url=[('%s s%se%s'%(clean_name(original_title,1).replace(' ','%20'),season_n,episode_n)).lower(),('%s s%s'%(clean_name(original_title,1).replace(' ','%20'),season_n)).lower(),('%s season+%s'%(clean_name(original_title,1).replace(' ','%20'),season)).lower()]
     else:
        search_url=[('%s s%se%s'%(clean_name(original_title,1).replace(' ','%20'),season_n,episode_n)).lower()]
    regex_pre='<div class="resultdivtop">(.+?)<div class="magnetictext'
    regex1=re.compile(regex_pre,re.DOTALL)
    
    
    regex='<div class="resultdivbottonlength">(.+?)<.+?class="hideinfohash">(.+?)<.+?class="hideinfohash">(.+?)<'
    regex2=re.compile(regex,re.DOTALL)
            
    for page in range(1,4):
      for itt in search_url:
        x=get_html('https://idope.se/torrent-list/%s/?p=%s&c=%s'%(itt,page,cat),headers=base_header,timeout=10).content()
        
        regex_pre='<div class="resultdivtop">(.+?)<div class="magnetictext'
        m_pre=regex1.findall(x)
        for items in m_pre:
            if stop_all==1:
                    break
            regex='<div class="resultdivbottonlength">(.+?)<.+?class="hideinfohash">(.+?)<.+?class="hideinfohash">(.+?)<'
            match=regex2.findall(items)
           
            for size,hash,nam in match:
     
                if stop_all==1:
                    break
                
                try:
                     o_size=size.replace('GiB','').replace('MiB','').replace('GB','').replace('MB','').replace(",",'').replace("\n",'').replace("\t",'').replace(" ",'').replace("\r",'').strip()
     
                     size=float(o_size)
              
                     if 'MB' in o_size or 'MiB' in o_size:
                       size=size/1000
                except:
                    size=0
                lk='magnet:?xt=urn:btih:%s&dn=%s'%(hash,urllib.quote_plus(nam))
                max_size=int(Addon.getSetting("size_limit"))
                if '.TS.' in nam:
                    continue
                if int(size)<max_size:
                   if '4k' in nam:
                          res='2160'
                   elif '2160' in nam:
                          res='2160'
                   elif '1080' in nam:
                          res='1080'
                   elif '720' in nam:
                          res='720'
                   elif '480' in nam:
                          res='480'
                   elif '360' in nam:
                          res='360'
                   else:
                          res='HD'
                   
                   all_links.append((nam,lk,str(size),res))
               
                   global_var=all_links
    return global_var
        
    