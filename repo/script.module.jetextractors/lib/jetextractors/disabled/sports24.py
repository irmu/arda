import requests, re, base64
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from . import sling, nhl, nba, mlb

class Sports24(Extractor):
    def __init__(self) -> None:
        self.domains = ["sports24.icu", "vip.sports24.icu"]
        self.name = "Sports24"
        self.short_name = "S24"

    def get_link(self, url):
        headers = {
            'user-agent': self.user_agent,
            'referer': "https://vip.sports24.icu/",
            'cookie': "visited=1"
        }
        if url.endswith("abc.html"):
            url = "https://sports24.icu/tv/v?id=abc"
        r = requests.get(url, headers=headers).text
        if "/mlb/player" in r:
            url_b64 = re.compile(r"\/mlb\/player\?src=(.+?)&").findall(r)[0]
            m3u8 = base64.b64decode(url_b64).decode("ascii")
            return m3u8
        elif "sl.php?ch=" in r:
            channel_id = re.compile(r'sl\.php\?ch=(.+?)"').findall(r)[0]
            channel_info = sling.get_channel_info(channel_id)
            playback_info = channel_info["qvt"]
            mpd_url, license_url, _, start_time = sling.get_playlist(playback_info)
            return "inputstream://%s===%s===%s" % (mpd_url, license_url, str(start_time))
        elif "/bm/play.php?id=" in r:
            re_url = "https://vip.sports24.icu" + re.compile(r'src="(\/bm\/play\.php\?id=.+?)"').findall(r)[0]
            r_embed = requests.get(re_url, headers={"User-Agent": self.user_agent, "Referer": url}).text
            mpd_url = re.compile(r'var src = "(.+?)"').findall(r_embed)[0]
            widevine_url = re.compile(r'var myWV = "(.+?)"').findall(r_embed)[0]
            license_url = widevine_url + "|Referer=https://sports24.icu/&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36|R{SSM}|"
            if license_url.startswith("//"):
                license_url = "https:" + license_url
            return "inputstream://%s===%s" % (mpd_url + "|User-Agent=" + self.user_agent, license_url)
        elif "/nhl/player?src=" in r:
            re_url = re.compile(r'"\/nhl\/player\?src=(.+?)&a=.+?"').findall(r)[0]
            m3u8 = base64.b64decode(re_url).decode("ascii")
            return m3u8
        elif "/bm/tsn.php?id=" in r:
            re_url = "https://sports24.icu/bm/tsn.php?id=" + re.compile(r'src="\/bm\/tsn\.php\?id=(.+?)"').findall(r)[0]
            r_embed = requests.get(re_url, headers=headers).text
            re_src = re.compile(r'var src = "(.+?)"').findall(r_embed)[0]
            src = base64.b64decode(re_src)
            if type(src) == bytes: src = src.decode("ascii")
            license_url = "https://license.9c9media.ca/widevine|Referer=https://sports24.icu/&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36|R{SSM}|"
            return "inputstream://%s===%s" % (src + "|User-Agent=" + self.user_agent, license_url)
        elif "v.php?id=" in r:
            re_url = "https://sports24.icu/frames/v.php?id=" + re.compile(r'v\.php\?id=(.+?)"').findall(r)[0]
            r_embed = requests.get(re_url, headers=headers).text
            re_m3u8 = re.compile(r'source: "(.+?)"').findall(r_embed)[0]
            return re_m3u8
        elif "ck.php?id=" in r:
            re_url = "https://sports24.icu/bm/ck.php?id=" + re.compile(r'ck\.php\?id=(.+?)"').findall(r)[0]
            r_embed = requests.get(re_url, headers=headers).text
            re_src = re.compile(r'var src = "(.+?)"').findall(r_embed)[0]
            return "inputstream://%s===" % (re_src + "|User-Agent=" + self.user_agent)
        else: return ""

    def get_games():
        nhl_games = nhl.get_games()
        nba_games = nba.get_games()
        mlb_games = mlb.get_games()
        nba_scores = nba.get_scores_yahoo()
        nhl_scores = nhl.get_scores_yahoo()
        for score in nba_scores:
            title = score["home_team"] + " vs " + score["away_team"]
            for game in nba_games:
                if game["title"].lower() == title.lower() or game["title"].lower().replace("la", "los angeles") == title.lower():
                    game["title"] = "[COLORorange]%s %s-%s[/COLOR]: %s" % (score["status"], str(score["home_score"]), str(score["away_score"]), game["title"])
                    break
        for score in nhl_scores:
            title = score["home_team"] + " vs " + score["away_team"]
            for game in nhl_games:
                if game["title"].lower() == title.lower() or game["title"].lower().replace("la", "los angeles") == title.lower():
                    game["title"] = "[COLORorange]%s %s-%s[/COLOR]: %s" % (score["status"], str(score["home_score"]), str(score["away_score"]), game["title"])
                    break
        games = nba_games + nhl_games + mlb_games
        return games