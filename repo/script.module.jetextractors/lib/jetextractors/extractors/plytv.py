import requests, re, base64
from bs4 import BeautifulSoup
from pyjsparser import parse

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..util.hunter import hunter

class PlyTv(Extractor):
    def __init__(self) -> None:
        self.domains = ["cuervotv.me"]
        self.user_agent = "Mozilla/5.0 ((Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15"

    def getAuthUrl(self, embed):
        auth_url = base64.b64decode(re.findall(r"const authCallUrl = '(.+?)'", embed)[0]).decode("utf-8")
        scode = re.findall(r"const sCode = '(.+?)'", embed)[0]
        ts = re.findall(r"const expireTs = (.+?);", embed)[0]
        unique_id = re.findall(r"const unqiueId = '(.+?)'", embed)[0]
        return f"{auth_url}/?stream={unique_id}&scode={scode}&expires={ts}"

    def __plytv_sdembed(self, base_url, origin):
        if not base_url.startswith("http"):
            base_url = f"https://{self.domains[0]}/sd0embed?v=" + base_url
        r = requests.post(base_url, headers={"Origin": origin, "Referer": origin, "User-Agent": self.user_agent}).text
        soup = BeautifulSoup(r, "html.parser")
        script = next(s for s in soup.select("script") if s.attrs == {})
        p = parse(script.string)
        for c, cmd in enumerate(p["body"]):
            if cmd["type"] == "VariableDeclaration":
                for declaration in cmd["declarations"]:
                    var_name = declaration['id']['name']
                    if 'name' in declaration['init']:
                        var_declare = declaration['init']['name']
                    else:
                        if declaration['init']['value'] != '':
                            var_declare = f"'{declaration['init']['value']}'"
                        else:
                            var_declare = "''"
                    exec(f"{var_name} = {var_declare}")
            elif cmd["type"] == "ExpressionStatement" and cmd["expression"]["type"] != "CallExpression":
                if cmd["expression"]["type"] == "AssignmentExpression":
                    exps = [cmd["expression"]]
                else:
                    exps = cmd["expression"]["expressions"]
                for exp in exps:
                    exec(f"{exp['left']['name']} = {exp['right']['left']['name']} {exp['right']['operator']} {exp['right']['right']['name']}")
        result = eval(p["body"][-2]["expression"]["arguments"][0]["name"])
        re_hunter = re.compile(r'decodeURIComponent\(escape\(r\)\)}\("(.+?)",(.+?),"(.+?)",(.+?),(.+?),(.+?)\)').findall(result)[0]
        deobfus = hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
        re_m3u8 = base64.b64decode(re.findall(r"const playUrl = '(.+?)';", deobfus)[0]).decode("utf-8")
        auth_url = self.getAuthUrl(deobfus)
        auth = requests.get(auth_url, headers={"Referer": base_url, "User-Agent": self.user_agent, "Origin": f"https://{self.domains[0]}"})
        return Link(address=re_m3u8, headers={"Referer": f"https://{self.domains[0]}/sd0embed", "User-Agent": self.user_agent, "Origin": f"https://www.{self.domains[0]}"}, is_widevine=True, manifest_type="hls", license_url="h")


    def ___plytv_sdembed(self, base_url, origin):
        if not base_url.startswith("http"):
            base_url = f"https://www.{self.domains[0]}/sd0embed?v=" + base_url
        r_embed = requests.post(base_url, headers={"Origin": origin, "Referer": origin, "User-Agent": self.user_agent}).text
        re_hunter = re.compile(r'}\(\"(.+?)\", (.+?), \"(.+?)\", (.+?), (.+?), (.+?)\)').findall(r_embed)
        re_b64 = re.compile(r"const (?:strmUrl|soureUrl) = '(.+?)';").findall(r_embed)
        if len(re_hunter) > 0:
            re_hunter = re_hunter[0]
            deobfus = hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
            re_b64 = re.findall(r"const vdoUrl = '(.+?)';", deobfus)[0]
            url = base64.b64decode(re_b64).decode("UTF-8")
            try:
                auth_url = self.getAuthUrl(deobfus)
                auth = requests.get(auth_url, headers={"Referer": base_url, "User-Agent": self.user_agent, "Origin": "https://www.plylive.me"}).text
            except:
                pass
        elif len(re_b64) > 0:
            url = base64.b64decode(re_b64[0]).decode("UTF-8")
            try:
                auth_url = self.getAuthUrl(r_embed)
                requests.get(auth_url, headers={"Referer": base_url, "User-Agent": self.user_agent}).text
            except:
                pass
        return Link(address=url, headers={"Referer": f"https://{self.domains[0]}/sd0embed", "User-Agent": self.user_agent, "Origin": f"https://{self.domains[0]}"}, license_url=f"|Referer=https://{self.domains[0]}/sd0embed")
    
    def plytv_sdembed(self, endpoint, vid, origin):
        base_url = f"https://{self.domains[0]}/sd0embed/{endpoint}"
        r_embed = requests.post(base_url, headers={"Origin": origin, "Referer": origin, "User-Agent": self.user_agent}, data={"v": vid}).text
        re_hunter = re.compile(r'decodeURIComponent\(escape\(.+\)\)}\(\"(.+?)\",(.+?),\"(.+?)\",(.+?),(.+?),(.+?)\)').findall(r_embed)[0]
        deobfus = hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
        re_b64 = re.findall(r"const vidHlsUrl = '(.+?)';", deobfus)[0]
        url = base64.b64decode(re_b64).decode("UTF-8")
        auth_url = self.getAuthUrl(deobfus)
        r = requests.get(auth_url, headers={"Referer": base_url, "User-Agent": self.user_agent}).text
        return Link(address=url, headers={"Referer": base_url, "User-Agent": self.user_agent, "Origin": f"https://{self.domains[0]}"}, license_url="|User-Agent=iPad")

    def get_link(self, url):
        if "&origin=" not in url:
            return ""
        else:
            origin = url[url.index("&origin=") + 8:]
            return self.plytv_sdembed(url, origin)
