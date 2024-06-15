import requests, re
from bs4 import BeautifulSoup as bs
from typing import List
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link


class SportsVideo(Extractor):
    domains = ["nfl-video.com", "nhlvideo.net","mlblive.net","rugby24.net", "fullfightreplays.com","basketball-video.com"]
    name = "SportsVideo"

    def get_games(self) -> List[Game]:
        games = []
        games.append(Game(title="NFL", page="0"))
        games.append(Game(title="NHL", page="1"))
        games.append(Game(title="MLB", page="2"))
        games.append(Game(title="Rugby", page="3"))
        games.append(Game(title="MMA", page="4"))
        games.append(Game(title="NBA", page="5"))
        return games
    def get_nba_games(self) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[5]}"  # Assuming NBA URL is at index 5 in domains list
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(base_url, headers=headers, verify=False).text
        soup = bs(r, 'html.parser')
        matches = soup.find_all(class_='short_item block_elem')
        for match in matches:
            name = match.h3.a.text.replace('Full Game Replay ', '').rstrip(' NHL')  # Update to NBA
            link = f"{base_url}{match.a['href']}"
            icon = f"{base_url}{match.a.img['src']}"
            games.append(Game(name, links=[Link(link, is_links=True)], icon=icon))
        games.append(Game("[COLORyellow]Page 2[/COLOR]", page=2))  # Adjust page number if necessary
        return games
    
    def get_games_page(self, page) -> List[Game]:
        games = []
        split = page.split(",") # sport[0,1,2,3],path[str]
        domain = self.domains[int(split[0])]
        base_url = f"https://{domain}"

        if len(split) == 1:
            r = requests.get(base_url, verify="basketball" not in domain).text
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
            r = requests.get(url, headers=headers, verify="basketball" not in domain).text
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
                # nba_games = self.get_nba_games()  # Assume you have a function to get NBA games
                # games += nba_games
        return games
    
    def get_links(self, url: str) -> List[Link]:
        links = []
        title = ''
        link = ''
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers, verify="basketball" not in url).text
        if "basketball" not in url:
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
        else:
            soup = bs(r, 'html.parser')
            iframes = soup.find_all(class_='su-button')
            for iframe in iframes:
                link = iframe['href']
                if link.startswith('//'):
                    link = f'https:{link}'
                response = requests.get(link, headers=headers, verify=False).text
                soup = bs(response, 'html.parser')
                iframe_ = soup.find('iframe')
                if not iframe_: continue
                link = iframe_['src']
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