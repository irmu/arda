# -*- coding: utf-8 -*-
import re
import time

global global_var,stop_all#global
global_var=[]
stop_all=0
from  resources.modules.client import get_html
 
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
    if tv_movie=='movie':
     search_url=[('%s+%s'%(clean_name(original_title,1).replace(' ','+'),show_original_year)).lower()]
    else:
      if Addon.getSetting('debrid_select')=='0' :
        search_url=[('%s+s%se%s'%(clean_name(original_title,1).replace(' ','+'),season_n,episode_n)).lower(),('%s-s%s'%(clean_name(original_title,1).replace(' ','-'),season_n)).lower(),('%s-season-%s'%(clean_name(original_title,1).replace(' ','-'),season)).lower()]
      else:
        search_url=[('%s+s%se%s'%(clean_name(original_title,1).replace(' ','+'),season_n,episode_n)).lower()]
    
    regex='<tr>(.+?)</tr>'
    regex1=re.compile(regex,re.DOTALL)
    
    regex='tfiles.org/torrent/.+?/(.+?)\.torrent\?title=(.+?)\.torrent.+?<td class="nowrap-td">(.+?)<.+?<span class="text-success">(.+?)<.+?span class="text-danger">(.+?)<'
    regex2=re.compile(regex,re.DOTALL)
            
    for itt in search_url:
      for page in range(1,4):
        
        x=get_html('https://ext.to/search/%s/%s/'%(itt,str(page)),headers=base_header,timeout=10).content()
       
        regex='<tr>(.+?)</tr>'
        macth_pre=regex1.findall(x)
        
        for itm in macth_pre:
            
            regex='tfiles.org/torrent/.+?/(.+?)\.torrent\?title=(.+?)\.torrent.+?<td class="nowrap-td">(.+?)<.+?<span class="text-success">(.+?)<.+?span class="text-danger">(.+?)<'
            macth_pre2=regex2.findall(itm)
          
            for hash,title,size,peer,seed in macth_pre2:
                    
                     if stop_all==1:
                        break
                     lk='magnet:?xt=urn:btih:%s&dn=%s'%(hash,urllib.quote_plus(title))
                     if stop_all==1:
                        break
                    
                     if '4k' in title:
                              res='2160'
                     elif '2160' in title:
                          res='2160'
                     elif '1080' in title:
                          res='1080'
                     elif '720' in title:
                          res='720'
                     elif '480' in title:
                          res='480'
                     elif '360' in title:
                          res='360'
                     else:
                          res='HD'
                    
                    
                   
                     try:
                         o_size=size
                         size=float(o_size.replace('GB','').replace('MB','').replace(",",'').strip())
                         if 'MB' in o_size:
                           size=size/1000
                     except:
                        size=0
                     max_size=int(Addon.getSetting("size_limit"))
              
                     if size<max_size:
                  
                       all_links.append((title,lk,str(size),res))
                   
                       global_var=all_links
    return global_var
        
    