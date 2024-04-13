import re, math
from base64 import b64decode
import requests
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class TheTVApp(Extractor):
    def __init__(self) -> None:
        self.domains = ["thetvapp.to"]
        self.name = "TheTVApp"

    def get_games(self):
        games = [
            Game("Live TV", page="tv"),
            Game("NBA", page="nba"),
            Game("MLB", page="mlb"),
            Game("NHL", page="nhl"),
            Game("NFL", page="nfl"),
        ]
        return games
    
    def get_games_page(self, page):
        games = []
        
        r = requests.get(f"https://{self.domains[0]}/{page}").text
        soup = BeautifulSoup(r, "html.parser")
        for link in soup.select("a.list-group-item"):
            href = f"https://{self.domains[0]}" + link.get("href")
            name = link.text
            games.append(Game(name, [Link(href)]))

        return games

    def get_link(self, url):
        link = ''
        s = requests.Session()
        r = s.get(url, headers={"User-Agent": self.user_agent, "Referer": f"https://{self.domains[0]}/"}).text
        encrypted = re.findall("encrypted = '(.+?)'", r)
        if encrypted:
            app_js_url = re.findall(r'type="module".+(build\/assets\/app-.+?\.js)', r)
            if app_js_url:
                app_js = s.get(f"https://{self.domains[0]}/{app_js_url[0]}").text
            else:
                soup = BeautifulSoup(r, 'html.parser')
                app_js_url = soup.find('script', attrs={'type': 'module'}).get('src')
                app_js = s.get(app_js_url).text
            key = self.get_key(app_js)
            link = self.deobfuscate_simplified(encrypted[0], key)
        return Link(link, headers={"Referer": f"https://{self.domains[0]}/", "User-Agent": self.user_agent}, is_hls=True)
    
    def get_key(self, file: str):
        deobfus_func_name = re.findall(r"{file:(.+?)\(encrypted\)", file)[0]
        deob_func = re.search(f"function {deobfus_func_name}\(.+?,.+?=(.+?)\)", file)
        key = deob_func.group(1)
        if key.startswith("'") or key.startswith('"'):
            key = eval(key)
            return key
        array_get_func_name = key[:key.index("(")]
        array_get_func_setter = re.search(f"const {array_get_func_name}=(.+?);", file)
        array_get_func_name = array_get_func_setter.group(1)
        backslash = "\\"
        array_get_func = re.search(f"return {backslash if array_get_func_name.startswith('$') else ''}{array_get_func_name}=function.+?" + "{", file)
        array_get_offset = int(file[file.index("-", array_get_func.end()) + 1:file.index(",", array_get_func.end())])
        for m in re.finditer(r"\.shift\(\)\)}}\)\((.+?),([0-9]+)\)", file):
            if m.start() > array_get_func_setter.start():
                array_func_match = m
                break
        array_func_name = array_func_match.group(1)
        array_shift_num = int(array_func_match.group(2))
        array_shift_func_body = file[file.rfind("(function", 0, array_func_match.start()):array_func_match.end()]
        array_func = re.search(f"function {array_func_name}\(\)", file)
        array = eval(file[file.index("[", array_func.start()):file.index("];", array_func.start()) + 1])
        expression = compile(re.findall(r"if\((.+?)===", array_shift_func_body)[0], "expression", "eval")

        def x(index) -> str:
            return array[index - array_get_offset]
        
        t = x
        
        def parseInt(s: str) -> int:
            m = re.match(r"([0-9]+)", s)
            if m == None:
                return math.nan
            else:
                return int(m.group(1))
        
        while (eval(expression) != array_shift_num):
            array.append(array.pop(0))
        
        key = x(int(key[key.index("(") + 1:]))
        return key
    
    def deobfuscate_simplified(self, s, key):
        ret = ''
        b64 = b64decode(s)
        for i, byte in enumerate(b64):
            ret += chr(byte ^ (ord(key[i % len(key)])))
        return ret
        