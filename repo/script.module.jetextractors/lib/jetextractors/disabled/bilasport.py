import requests, re, base64, time
try: from urlparse import urlparse
except: from urllib.parse import urlparse
from bs4 import BeautifulSoup
from . import yoursports
from datetime import datetime
from unidecode import unidecode
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
domain = ["bilasport.net"]
site_name = "Bilasport"
short_id = "BS"

def get_regex_yoursports(text):
    if "rbnhd" in text:
        return r"var rbnhd = '(.+?)'"
    else:
        return r'var mustave = atob\((.+?)\)'

def get_yoursports(url):
    stream = requests.get(url).text
    try:
        link = re.compile(get_regex_yoursports(stream)).findall(stream)[0]
    except:
        link = re.compile('<iframe frameborder=0 height=100% width=100% src="(.+?php)"', re.DOTALL).findall(stream)[0]
        link = requests.get(link).text
        link = re.compile(get_regex_yoursports(link)).findall(link)[0]

    if not link.startswith("http") and not link.startswith("/"):
        link = base64.b64decode(link).decode("ascii")
        if link.startswith('/'):
            link = 'http://yoursports.stream' + link

    link = '%s|Referer=%s&User-Agent=%s' % (link, url, user_agent)
    return link

def get_m3u8_iframe(href):
    m3u8 = ""
    r_stream = requests.get(href, "html.parser", headers={"User-Agent": user_agent}).text
    if href.startswith("http://yoursports.stream"):
        m3u8 = get_yoursports(href)
    elif len(re.compile(r'var sou.?.?=.?.?"(.+?)"').findall(r_stream)) > 0:
        m3u8 = re.compile(r'var sou.?.?=.?.?"(.+?)"').findall(r_stream)[0] + "|Referer=%s&User-Agent=%s" % (href, user_agent)
    elif len(re.compile(r"source: '(.+?)'").findall(r_stream)) > 0:
        m3u8 = re.compile(r"source: '(.+?)'").findall(r_stream)[0] + "|Referer=%s&User-Agent=%s" % (href, user_agent)
    elif "https://href.li/" in r_stream:
        re_hrefli = re.compile(r'iframe.+?src="(.+?)"').findall(r_stream)[0].replace("https://href.li/?", "")
        m3u8 = get_m3u8_iframe(re_hrefli)

    if m3u8 != "" and not m3u8.startswith("http"):
        domain = urlparse(href).netloc
        m3u8 = "http://%s/" % domain + m3u8

    return m3u8

def get_m3u8(url, extra=False):
    base_url = "https://" + urlparse(url).netloc
    r_href = requests.get(url, headers={"User-Agent": user_agent}).text
    re_iframe = re.compile(r'document\.getElementById\(\'iframegame\'\)\.src = "(.+?)";').findall(r_href)[0]
    r_iframe = requests.get(re_iframe, headers={"User-Agent": user_agent}).text
    soup_iframe = BeautifulSoup(r_iframe, "html.parser")
    m3u8 = ""
    iframe_src = soup_iframe.find("iframe").get("src")
    if iframe_src.startswith("http://bilasport.net/nfl"):
        iframe_src = "http://givemenbastreams.com/nflstream.php?g=" + iframe_src.replace("http://bilasport.net/nfl/", "").replace(".php", "")
    elif iframe_src.startswith("https://href.li/?"):
        iframe_src = iframe_src.replace("https://href.li/?", "")
    elif iframe_src.startswith("/"):
        iframe_src = base_url + iframe_src

    m3u8 = get_m3u8_iframe(iframe_src)
    if m3u8 == "":
        raise "no link found"
    else:
        return m3u8

def _get_games(index="schedule.html"):
    games = []
    base_url = "http://bilasport.net/"
    r_home = requests.get(base_url + index, headers={"User-Agent": user_agent}).text
    soup = BeautifulSoup(r_home, "html.parser")
    for game in soup.select("tr.tbltr1"):
        try:
            href = base_url + game.get("data-erlnk")
            title = game.find_all("div", class_="clb_name2")[0].getText().strip() + " vs. " + game.find_all("div", class_="clb_name2")[1].getText().strip()
            icon = base_url + game.find_all("img")[0].get("src")
            
            league = game.find_all("div", class_="tms_vs2_inf_dt1")[2].find("div").getText()
            time_str = game.find("div", class_="given_date").get("data-gamestart")
            utc_time = ""
            if time_str != "":
                utc_time = datetime(*(time.strptime(time_str, "%Y-%m-%d %H:%M")[:6]))

            end_time = game.find("div", class_="given_date").get("data-gameends")
            utc_end_time = ""
            if end_time != "":
                utc_end_time = datetime(*(time.strptime(end_time, "%Y-%m-%d %H:%M")[:6]))
            # TODO: Implement this
            # href2 = "-"
            # if "g_t_inf_chlst" in data[href]:
            #     try:
            #         r_extra = BeautifulSoup(data[href], "html.parser")
            #         href2 = r_extra.find("div", {"class": "g_t_inf_chlst"}).parent.get("href")
            #     except Exception as e:
            #         pass
            games.append({
                "title": unidecode(title),
                "links": [
                    href
                ],
                "icon": icon,
                "league": league,
                "time": utc_time,
            })
        except Exception as e:
            continue
    return games

def get_games():
    return _get_games() + _get_games("tomorrow.html")