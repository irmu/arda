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
type=['movie','non_rd']

import urllib2,urllib,logging,base64,json


import urllib2,urllib,logging,base64,json


color=all_colors[112]
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    if tv_movie=='tv':
        return []
    headers={'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.0.1; samsung Build/AXXXXXXX)',

            'Connection': 'Keep-Alive'}
    c_name=clean_name(original_title,1).lower()
    url='https://movie2020.club/newmovie2020/movie2020.php?fines=%s&javac=AA:AA:AA:AA:AA:AA&javemu=false&cz02=com.hot.movies.online.free'%clean_name(original_title,1)
 
    x=get_html(url,headers=headers).json()
 
    from resources.modules.google_solve import googledrive_resolve
    for items in x['kalbe']:
        if c_name in items['unmee'].lower() and show_original_year in items['unmee']:
            url='https://movie2020.club/newmovie2020/movie2020.php?jindanjun=%s&javac=AA:AA:AA:AA:AA:AA&javemu=false&cz02=com.hot.movies.online.free'%items['unid']
            y=get_html(url,headers=headers).json()
            
            for itt in y['kalbe'][0]['drecturl']:
                  id_lk=itt['link']
                  link='https://drive.google.com/file/d/'+id_lk+'/view'
                  try:
                    link2,qualities=googledrive_resolve(link)
                  except:
                    continue
                  
                  link2=link2.split('|')
                  qualities.sort(reverse = True) 
                  if len(qualities)>0:
                    res=qualities[0]
                  
                  
                  cookies={'DRIVE_STREAM':link2[2].split('Cookie=DRIVE_STREAM%3D')[1]}
                 
                 
                 
                  try_head = get_html(link2[0].replace('\\',''),headers=base_header,cookies=cookies, stream=True,verify=False,timeout=15)
                  size=0
                 
                  if 'Content-Length' in try_head.headers():
  
                    if int(try_head.headers()['Content-Length'])>(1024*1024):
                        size=float(try_head.headers()['Content-Length'])/(1024*1024*1024)
                
                        
                  all_links.append((clean_name(original_title,1),'Direct_link$$$'+link,str(size),str(res)))

                  global_var=all_links
    return global_var