import requests, re
from bs4 import BeautifulSoup as bs
from typing import List
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link


class SportsVideo(Extractor):
    domains = ["nfl-video.com", "nhlvideo.net","mlblive.net","rugby24.net", "fullfightreplays.com"]
    name = "SportsVideo"

    def get_games(self) -> List[Game]:
        games = []
        games.append(Game(title="NFL", page="0"))
        games.append(Game(title="NHL", page="1"))
        games.append(Game(title="MLB", page="2"))
        games.append(Game(title="Rugby", page="3"))
        games.append(Game(title="MMA", page="4"))
        return games
    
    def get_games_page(self, page) -> List[Game]:
        games = []
        split = page.split(",") # sport[0,1,2,3],path[str]
        domain = self.domains[int(split[0])]
        base_url = f"https://{domain}"

        if len(split) == 1:
            r = requests.get(base_url).text
            soup = bs(r, "html.parser")
            for li in soup.select_one("ul#list_cat").select("li"):
                if li.get("class") != None:
                    continue
                cat_name = li.text.strip()
                cat_a = li.next
                if cat_a.get("rel") != None:
                    continue
                cat_href = cat_a.get("href")
                if cat_href == None:
                    continue
                href = "/" + "/".join(cat_href.split("/")[3:])
                games.append(Game(title=cat_name, page=f"{split[0]},{href}"))
        else:
            url = base_url + split[1]
            headers = {"User-Agent": self.user_agent, "Referer": base_url}
            r = requests.get(url, headers=headers).text
            soup = (bs(r, 'html.parser'))
            matches = soup.find_all(class_='short_item block_elem')
            for match in matches:
                name = match.h3.a.text.replace('Full Game Replay ', '').rstrip(' NHL')
                link = f"{base_url}{match.a['href']}"
                icon = f"{base_url}{match.a.img['src']}"
                games.append(Game(name, links=[Link(link, is_links=True)], icon=icon))
            next_page_btn = soup.select("a.swchItem")
            if len(next_page_btn) > 0 and next_page_btn[-1].text == "»":
                href = next_page_btn[-1].get('href')
                if not href.startswith("/"):
                    href = split[1] + href
                page = int(re.findall(r"spages\('(.+?)'", next_page_btn[-1].get('onclick'))[0])
                games.append(Game(f"[COLORyellow]Page {page}[/COLOR]", page=f"{split[0]},{href}"))
        return games
    
    def get_links(self, url: str) -> List[Link]:
        links = []
        title = ''
        link = ''
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers).text
        soup = bs(r, 'html.parser')
        alt_links = soup.find_all(class_='su-button su-button-style-default')
        if alt_links:
            for alt_link in alt_links:
                link = alt_link.get('href')
                if link:
                    title = link.split('/')[2]
                    links.append(Link(link, name=title, is_resolveurl=True))
        iframes = soup.find_all('iframe')
        for iframe in iframes:
            link = iframe['src']
            if link.startswith('//'):
                link = f'https:{link}'
            if 'youtube' in link:
                yt_id = link.split('/')[-1]
                link = f'plugin://plugin.video.youtube/play/?video_id={yt_id}'
                title = 'Highlights'
            else:
                title = link.split('/')[2]
            links.append(Link(link, name=title, is_resolveurl=True))
        return links