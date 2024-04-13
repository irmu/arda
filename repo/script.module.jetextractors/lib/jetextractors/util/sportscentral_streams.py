import requests, base64
from bs4 import BeautifulSoup
from ..config import get_config
from urllib.parse import urlparse

from ..models.Link import Link
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344"

def get_streams(match_id, match_sport, origin):
    # url = "https://sportscentral.io/streams-table/%s/%s?new-ui=1&origin=%s" % (match_id, match_sport, origin)
    url = f"https://scdn.dev/main-assets/{match_id}/{match_sport}?origin={origin}"
    links = get_streams_table(url)
    return links

def get_streams_table(url):
    links = []
    r_streams = requests.get(url, headers={"User-Agent": user_agent, "Referer": "https://nbabite.com"}).text
    soup = BeautifulSoup(r_streams, "html.parser")
    exclude = get_config().get("sportscentral_exclude", [])
    for stream in soup.select("table.m-0 > tbody > tr"):
        href = stream.get("data-stream-link")
        channel = stream.select_one("b").text.strip()
        name = stream.select_one("td").text.strip()
        site = urlparse(href).netloc
        if site in exclude:
            continue
        # quality = stream.select_one("span.label-purple").text.strip()
        links.append(Link(address=href, name="%s - %s" % (name, channel)))
    return links