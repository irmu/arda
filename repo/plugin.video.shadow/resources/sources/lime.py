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
    if tv_movie=='movie':
     search_url=[('%s %s'%(clean_name(original_title,1),show_original_year)).lower()]
     search_type='movies'
    else:
     if Addon.getSetting('debrid_select')=='0' :
        search_url=[('%s s%se%s'%(clean_name(original_title,1),season_n,episode_n)).lower(),('%s s%s'%(clean_name(original_title,1),season_n)).lower(),('%s season %s'%(clean_name(original_title,1),season)).lower()]
     else:
        search_url=[('%s s%se%s'%(clean_name(original_title,1),season_n,episode_n)).lower()]
     search_type='tv'
    
    regex='<tr bgcolor="(.+?)</tr>'
    regex1=re.compile(regex,re.DOTALL)
    
    regex='a href="(.+?)".+?<td class="tdnormal">(.+?)<.+?<td class="tdseed">(.+?)<.+?<td class="tdleech">(.+?)<'
    regex2=re.compile(regex,re.DOTALL)
    
    regex3=re.compile('&dn=(.+?)&')
    
    for itt in search_url:
      for page in range(0,4):
        
        
                      
        x = get_html('https://limetorrents.at/search/%s/category/%s/%s/'%(itt,search_type,str(page)),headers=base_header).content()

        regex='<tr bgcolor="(.+?)</tr>'
        m=regex1.findall(x)
        
        for items in m:
            regex='a href="(.+?)".+?<td class="tdnormal">(.+?)<.+?<td class="tdseed">(.+?)<.+?<td class="tdleech">(.+?)<'
            m2=regex2.findall(items)
        
        
       
            for link,size,seed,peer in m2:
               
                if stop_all==1:
                    break
                try:
                     o_size=size.decode('utf8','ignore')
                     size=float(o_size.replace('GB','').replace('MB','').replace(",",'').strip())
                     if 'MB' in o_size:
                       size=size/1000
                except Exception as e:
                   
                    size=0
                title=regex3.findall(link)
                if len(title)>0:
                    title=urllib.unquote_plus(title[0])
                else:
                    title=original_title
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
                
                
               
                 
                max_size=int(Addon.getSetting("size_limit"))
          
                if size<max_size:
                  
                   all_links.append((title,link,str(size),res))
               
                   global_var=all_links
    return global_var
        
    