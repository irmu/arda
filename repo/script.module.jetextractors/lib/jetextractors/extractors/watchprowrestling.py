import sys
import json
import re
from urllib.parse import urlparse, parse_qsl, quote_plus, unquote_plus
from html import unescape
from base64 import b64decode
from typing import List
import xbmc
import xbmcgui
import requests
from bs4 import BeautifulSoup as bs
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack


BASE_URL = 'https://watchprowrestling.co'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
HEADERS = {"User-Agent": USER_AGENT, 'Accept': '*/*', 'Referer': BASE_URL}
SEARCH_URL = f'{BASE_URL}/?s='
DEBRID = ['1fichier.com', 'uptobox.com', 'drop.download']
FILTERS = ['guccihide.com', 'streamplay.to', 'www.m2list.com', 'vptip.com', 'https://issuessolution.site', 'www.sawlive.net', 'player.restream.io']
PROGRESS = xbmcgui.DialogProgress()
OK = xbmcgui.Dialog().ok


class WatchProWrestling(Extractor):
    domains = ["watchprowrestling.co"]
    name = "WatchProWrestling"

    def get_games(self) -> List[Game]:
        response = requests.get(BASE_URL, headers=HEADERS)
        soup = bs(response.text, 'html.parser')
        vids = soup.find_all(class_='post-card')
        if not vids:
            OK('No Items Found', 'No items were found.')
            sys.exit()
        games = [Game('Search', page='SEARCH')]
        for vid in vids:
            title = vid.a.img['alt'].replace('Watch ', '')
            link = vid.a['href']
            thumbnail = vid.a.img['src']
            games.append(Game(title=title, links=[Link(link, is_links=True)], icon=thumbnail))
        pagination = soup.find(class_='next page-numbers')
        if pagination:
            next_page = pagination['href']
            games.append(Game("[COLORyellow]Next Page[/COLOR]", page=next_page))
        return games
    
    def get_games_page(self, page) -> List[Game]:
        games = []
        items = {}
        if 'SEARCH' in page:
            query = from_keyboard()
            if not query:
                quit()
            url = SEARCH_URL + quote_plus(query)
        else:
            url = page
        response = requests.get(url, headers=HEADERS)
        soup = bs(response.text, 'html.parser')
        vids = soup.find_all(class_='post-card')
        if not vids:
            OK('No Items Found', 'No items were found.')
            quit()
        for vid in vids:
            title = vid.a.img['alt'].replace('Watch ', '')
            link = vid.a['href']
            thumbnail = vid.a.img['src']
            items[title] = {
                'link': link,
                'thumbnail': thumbnail
            }
            games.append(Game(title=title, links=[Link(link, is_links=True)], icon=thumbnail))
        pagination = soup.find(class_='next page-numbers')
        if pagination:
            next_page = pagination['href']
            games.append(Game("[COLORyellow]Next Page[/COLOR]", page=next_page))
        return games
    
    def get_links(self, url: str) -> List[Link]:
        xbmc.log('WPW Started', xbmc.LOGINFO)
        links = []
        items = []
        non_working = []
        debrid = []
        non_debrid = []
        link = ''
        r = requests.get(url, headers=HEADERS).text
        soup = bs(r, 'html.parser')
        matches = soup.find_all(class_='custom-button color-blue shape-square size-small align-left')
        for match in matches:
            title = match.text
            link = match['href']
            if 'NetU' in title:
                continue
            splitted = link.split('/')
            if len(splitted) > 2 and splitted[2] in DEBRID:
                title = f'{title} [COLOR green]***Debrid***[/COLOR]'
            links.append([title, link])
        if not links:
            OK('WPW Scraper', 'No Links Available')
        if not 'Live Stream' in links[0][0]:
            links.reverse()
        selection = self.get_multilink(links)
        if not selection:
            sys.exit()
        title, link = selection
        #xbmc.log(f'selection= {selection}', xbmc.LOGINFO)
        link = resolve(link)
        if not link:
            sys.exit()
        if link.startswith('hls|'):
            link = link.replace('hls|', '')
            items.append(Link(link, name=title, is_resolveurl=False, is_hls=True))
        elif link.startswith('ffmpeg|'):
            link = link.replace('ffmpeg|', '')
            items.append(Link(link, name=title, is_resolveurl=False, is_ffmpegdirect=True))
        else:
            items.append(Link(link, name=title, is_resolveurl=True))
        if not items:
            OK('WPW Scraper', 'No Links Available')
            sys.exit()
        return items
    
    def get_multilink(self, lists):
        labels = [i[0] for i in lists]
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Choose a Link', labels)
        if ret == -1:
           return ''
        return lists[ret]


class Search(WatchProWrestling):
    domains = ["watchprowrestling.co"]
    name = "WatchProWrestlingSearch"

    def get_games(self) -> List[Game]:
        response = requests.get(BASE_URL, headers=HEADERS)
        soup = bs(response.text, 'html.parser')
        vids = soup.find_all(class_='post-card')
        if not vids:
            OK('No Items Found', 'No items were found.')
            sys.exit()
        games = []
        for vid in vids:
            title = vid.a.img['alt'].replace('Watch ', '')
            link = vid.a['href']
            thumbnail = vid.a.img['src']
            games.append(Game(title=title, links=[Link(link, is_links=True)], icon=thumbnail))
        return games


def from_keyboard(default_text='', header='Search'):
    kb = xbmc.Keyboard(default_text, header, False)
    kb.doModal()
    if (kb.isConfirmed()):
        return kb.getText()
    return

def unpack(url:str, referer: str):
    HEADERS['Referer'] = referer
    r = requests.get(url, headers=HEADERS).text
    return jsunpack.unpack(r)

def resolve_hdfree(url: str, referer: str):
    unpacked = unpack(url, referer=referer)
    url2 = re.compile("startframe2='(.+?)'").findall(unpacked)[0]
    return url2

def resolve_educ_top(url: str, referer: str):
    HEADERS['Referer'] = referer
    unpacked = unpack(url, referer=referer)
    url2 = re.compile('iframe src="(.+?)line=').findall(unpacked)[0]
    return url2

def resolve_sawlive(url: str):
    HEADERS['Referer'] = 'https://vptip.com/'
    r = requests.get(url, headers = HEADERS).text
    code = re.compile(r'var maincode="(.+?)"').findall(r)[0]
    line = re.compile(r'var subcode="(.+?)"').findall(r)[0]
    HEADERS ['Referer'] = 'https://www.hdfree.info/'
    r = requests.get(f'https://www.hdfree.info/finalpage/{code}.php?line={line}', headers=HEADERS).text
    try:
        labels = b64decode(re.compile("var labels=atob\('(.+?)'").findall(r)[0]).decode('utf-8')
        substyles = b64decode(re.compile("var substyles=atob\('(.+?)'").findall(r)[0]).decode('utf-8')
        _id = re.compile("var preloadcaptions = '(.+?)_").findall(r)[0]
        return 'https:' + labels.split('src="')[1] + _id
    except IndexError:
        HEADERS['Referer'] = 'https://vptip.com/'
        r = requests.get(url, headers = HEADERS).text
        line = re.compile(r'var subcode="(.+?)"').findall(r)[0]
        referer = f'https://android-database2.firebase-api.com/group2/secure2/?line={line}'
        link = f'https://android-database2.firebase-api.com/AccessLog2/{line}/apache.m3u8'
        return f'{link}|Referer={referer}'
    return
    
def resolve_ntuplay(url: str, referer: str=''):
    if referer:
        HEADERS['Referer'] = referer
    else:
        HEADERS['Referer'] = 'https://vptip.com/'
    r = requests.get(url, headers=HEADERS).text
    link = re.compile("source:'(.+?)'").findall(r)
    if link:
        link = link[0]
        if 'webuit.' in link:
            return resolve_webuit(link, referer=url)
        return f'hls|{link}|Referer={url}'
    return

def resolve_webuit(url: str, referer: str):
    HEADERS['Referer'] = referer
    r = requests.get(url, headers=HEADERS).text
    lines = r.splitlines()
    if lines:
        track = lines[-1]
        url2 = url.replace('webuit', 'wiki').replace('/lb/', '/wiki/').replace('index.m3u8', track)
        return f'hls|{url2}|Referer={referer}'
    return

def resolve_m2list(url:str):
    HEADERS['Referer'] = url
    _id, main_id = re.compile('mirror=(.+?)&mainid=(.+?$)').findall(url)[0]
    url2 = f'https://www.m2list.com/2023update/db/{main_id}_cache.php'
    r = requests.get(url2, headers=HEADERS).text
    x = re.compile('json="(.+?)"').findall(r)
    if not x:
        return
    try:
        x = b64decode(x[0]).decode('utf-8')
        x = json.loads(x)
    except:
        return
    
    video_id = ''
    link = ''
    try:
        video_id = x[_id.replace('tdmrep', 'dmrep')]
    except KeyError:
        return
    if not video_id:
        return
    
    embed_DmRep_type1 = f'https://www.dailymotion.com/embed/video/{video_id}'
    embed_FSCFull = f'https://developer1-vioef.android-devs.top/f/{video_id}.db|Referer=https://developer1-vioef.android-devs.top/'
    embed_FSCRep = f'https://developer1-vioef.android-devs.top/f/{video_id}.db|Referer=https://developer1-vioef.android-devs.top/'
    embed_pvphd = f'hls|https://player2.pvpstage.com/f/{video_id}.480|Referer=https://player2.pvpstage.com/'
    embed_pvphd = f'https://android-database1.firebase-api.com/dvr1/{video_id}.m3u8|Referer=https://www.linux-developers.top/'
    embed_Host4Full = f"https://sanji12.affliate.net/10th_March_2023/embed/mod/pvphd.php?source={video_id}" # Needs Prefix?
    emdbed2 = 'https://android-database1.firebase-api.com/dvr1/TNA_iMPACT_2024_07_11_720p_SD_1.m3u8'
    
    types = {
        'fscfull': embed_FSCFull,
        'tubehdfull': embed_pvphd,
        'h3full': embed_pvphd,
        'h4full': embed_Host4Full,
        'host3lp': embed_pvphd,
        'tuberep': embed_pvphd,
        'dmlp': embed_DmRep_type1,
        'tubelp': embed_pvphd,
        'fscrep': [
            embed_FSCRep,
            embed_pvphd
        ],
        'dmrep': embed_DmRep_type1
    }
    _id_splitted = _id.split('_')
    code = _id_splitted[0]
    if len(_id_splitted) > 1:
        chack_id = f'{code}_count{_id_splitted[1]}'
    else:
        chack_id = chack_id = f'{code}_count'
    link = types.get(code, '')
    if not link:
        return
    if type(link) == list:
        chack = x.get(chack_id, '')
        if chack == '1':
            link = link[0]
        else:
            link = link[1]
    return link

def resolve_vptip(url: str):
    #xbmc.log(f'vptip_url= {url}', xbmc.LOGINFO)
    HEADERS['Referer'] = BASE_URL
    r = requests.get(url, headers=HEADERS)
    soup = bs(r.text, 'html.parser')
    iframe = soup.find('iframe')
    #xbmc.log(f'iframe= {iframe}', xbmc.LOGINFO)
    if iframe:
        link = iframe['src']
        if link.startswith('//'):
            link = 'https:' + link
        return link
    return url

def resolve_wikisport(url: str):
    HEADERS['Referer'] = 'https://vptip.com/'
    r = requests.get(url, headers=HEADERS).text
    soup = bs(r, 'html.parser')
    iframe = soup.find('iframe')
    url2 = iframe['src']
    if 'ntuplay' in url2:
        return resolve_ntuplay(url2, referer=url)
    return url2

def resolve_embedstream(url:str):
    from .embedstream import Embedstream
    es = Embedstream()
    link = es.get_link(url)
    return f'{link}|Referer=https://www.nolive.me/'

def resolve_guccihide(url:str):
    HEADERS['Referer'] = 'https://vptip.com/'
    r = requests.get(url, headers=HEADERS).text
    try:
        r = jsunpack.unpack(r)
    except:
        return 
    link = re.compile('file:"(.+?)"').findall(r)
    if not link:
        return
    link = link[0]
    return f'hls|{link}|Referer={url}'

def resolve_healthvault(url):
    url_parsed = urlparse(url)
    url = dict(parse_qsl(url_parsed.query)).get('id')
    r = requests.get(url, headers=HEADERS)
    soup = bs(r.text, 'html.parser')
    meta = soup.find('meta')
    if meta:
        content = meta.get('content')
        if content:
            content = unescape(content)
            url2 = dict(parse_qsl(content)).get('id')
            return url2
    small = soup.find('small')
    if small:
        query = urlparse(unquote_plus(small.a['href'])).query
        return dict(parse_qsl(query))['id']
    return False

def resolve(url: str):
    url1 = ''
    if 'fast.store' in url:
            return f'{url}|Referer={BASE_URL}/'
    if 'vptip' in url:
        url1 = resolve_vptip(url)
    elif 'healthvault.online' in url:
        url1 = resolve_healthvault(url)
    if url1:
        if 'sawlive' in url1:
            return resolve_sawlive(url1)
        elif 'wikisport.click' in url1:
            return resolve_wikisport(url1)
        elif 'ntuplay' in url1:
            return resolve_ntuplay(url1)
        elif 'm2list' in url1:
            return resolve_m2list(url1)
        elif 'embedstream.me' in url1:
            return resolve_embedstream(url1)
        elif 'guccihide' in url1:
            return resolve_guccihide(url1)
        else:
            return url1 
    return url