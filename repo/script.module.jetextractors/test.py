from typing import List
from lib.jetextractors import extractor
import colorama, calendar, requests, json
from datetime import datetime, timedelta
from lib.jetextractors.models.Extractor import Extractor
from lib.jetextractors.models.Link import Link

def format_time(date):
    return utc_to_local(date).strftime("%m/%d %I:%M %p") if date != None else ""

# https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib
def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def link_playable(link: Link) -> bool:
    if link.is_widevine:
        return True, None
    r = requests.get(link.address, headers=link.headers)
    if r.status_code == 403 and link.jetproxy:
        link.headers["User-Agent"] = link.headers["User-Agent"] + "1"
        r = requests.get(link.address, headers=link.headers)
    if "#EXTM3U" in r.text:
        return True, r
    else:
        return False, r

def test_link(link: Link, i: int = 0, length: int = 1):
    try:
        link_ext = extractor.find_extractor(link.address)
        if link_ext is not None and link_ext.shortener:
            link = link_ext.get_link(link.address)
            link_ext = extractor.find_extractor(link.address)
        if link.name is not None:
            print(f"\t\tLink {i + 1}/{length} ({link.name}): {link.address} (links: {link.is_links}, jetproxy: {link.jetproxy}, widevine: {link.is_widevine}, direct: {link.is_direct}, headers: {link.headers})")
        else:
            print(f"\t\tLink {i + 1}/{length}: {link.address} (links: {link.is_links}, jetproxy: {link.jetproxy}, widevine: {link.is_widevine}, direct: {link.is_direct}, headers: {link.headers})")
        if link.is_direct:
            playable = link_playable(link)
            if playable[0]:
                print(colorama.Fore.GREEN + f"\t\t\t✅ Link is playable" + colorama.Fore.WHITE)
            else:
                print(colorama.Fore.RED + f"\t\t\t❌ Link is not playable (status code {playable[1].status_code})" + colorama.Fore.WHITE)
            return
        if link_ext != None:
            print(f"\t\t\tUsing extractor: {link_ext.name} ({type(link_ext).__name__})")
            try:
                m3u8 = link_ext.get_link(link.address)
                if m3u8 == None:
                    print(colorama.Fore.RED + f"\t\t\t❌ Link is not playable (link is none)" + colorama.Fore.WHITE)
                    return
                print(colorama.Fore.CYAN + f"\t\t\tLink: {m3u8} (headers: {m3u8.headers}, jetproxy: {m3u8.jetproxy}, widevine: {m3u8.jetproxy})" + colorama.Fore.WHITE)
                playable = link_playable(m3u8)
                if playable[0]:
                    print(colorama.Fore.GREEN + f"\t\t\t✅ Link is playable" + colorama.Fore.WHITE)
                else:
                    print(colorama.Fore.RED + f"\t\t\t❌ Link is not playable (status code {playable[1].status_code})" + colorama.Fore.WHITE)
            except Exception as e:
                print(colorama.Fore.RED + f"\t\t\t❌ Error when getting link: {e}" + colorama.Fore.WHITE)
        else:
            print(colorama.Fore.YELLOW + "\t\t\tNo extractor found for link; trying iframe extractor" + colorama.Fore.WHITE)
            iframes = extractor.iframe_extractor(link.address)
            if len(iframes) == 0:
                print(colorama.Fore.RED + "\t\t\t❌ No links from iframe extractor" + colorama.Fore.WHITE)
                return
            print(f"\t\t\tiframe links:")
            for x, iframe in enumerate(iframes):
                print(colorama.Fore.CYAN + f"\t\t\t\tiframe {x + 1}/{len(iframes)}: {iframe.address} (headers: {iframe.headers})" + colorama.Fore.WHITE)
                playable = link_playable(iframe)
                iframe_ext = extractor.find_extractor(iframe.address)
                if not playable[0] and iframe_ext != None:
                    print(colorama.Fore.WHITE + f"\t\t\t\t\tUsing extractor: {iframe_ext.name} ({type(iframe_ext).__name__})" + colorama.Fore.WHITE)
                    try:
                        m3u8 = iframe_ext.get_link(iframe.address)
                        print(colorama.Fore.CYAN + f"\t\t\t\t\tLink: {m3u8} (headers: {m3u8.headers}, jetproxy: {m3u8.jetproxy}, widevine: {m3u8.jetproxy})" + colorama.Fore.WHITE)
                        playable = link_playable(m3u8)
                    except Exception as e:
                        print(colorama.Fore.RED + f"\t\t\t\t\t❌ Error when getting link: {e}" + colorama.Fore.WHITE)
                        continue
                if playable[0]:
                    print(colorama.Fore.GREEN + f"\t\t\t\t\t✅ Link is playable" + colorama.Fore.WHITE)
                else:
                    print(colorama.Fore.RED + f"\t\t\t\t\t❌ Link is not playable (status code {playable[1].status_code})" + colorama.Fore.WHITE)
    except Exception as e:
        print(colorama.Fore.RED + f"\t\t\t❌ Link is not playable (error: {e})" + colorama.Fore.WHITE)

def test_links(links: List[Link]):
    if links[0].is_links:
        print(f"\t\t\tGetting links...")
        links_ext = extractor.find_extractor(links[0].address)
        links = links_ext.get_links(links[0].address)
        if len(links) == 0:
            print(colorama.Fore.YELLOW + f"\t\t\tNo links; skipping..." + colorama.Fore.WHITE)
            return
    for i, link in enumerate(links):
        test_link(link, i, len(links))

def test_extractor(ext: Extractor):
    ext_name = f"{ext.name} ({type(ext).__name__})"
    print(colorama.Style.BRIGHT + colorama.Fore.BLUE + f"{ext_name}: Starting tests...")
    try:
        games = ext.get_games()
        if len(games) == 0:
            print(colorama.Fore.YELLOW + f"{ext_name}: Zero games; skipping...")
            return
        print(colorama.Style.BRIGHT + colorama.Fore.WHITE + f"{ext_name}: Games:")
        for g, game in enumerate(games):
            print(f"\tGame {g + 1}/{len(games)} {format_time(game.starttime)} ({game.league}): {game.title}")
            if len(game.links) == 0:
                print(colorama.Fore.YELLOW + f"\t\tNo links; skipping...")
                continue
            test_links(game.links)
    except Exception as e:
        print(colorama.Fore.RED + f"{ext_name}: Error when getting games: {e}" + colorama.Fore.WHITE)

if __name__ == "__main__":
    extractors = list(sorted(extractor.get_extractors(), key=lambda x: type(x).__name__))
    colorama.init()

    print("[1] Test all extractors")
    print("[2] Test one extractor")
    print("[3] Test link")
    inp = input("Make a selection: ")
    if inp == "1":
        for ext in extractors:
            test_extractor(ext)
            print(colorama.Style.RESET_ALL)
    elif inp == "2":
        print("Choose extractor:")
        for i, ext in enumerate(extractors):
            ext_name = f"{ext.name} ({type(ext).__name__})"
            print(f"[{i}] {ext_name}")
        inp = input("Make a selection: ")
        test_extractor(extractors[int(inp)])
    elif inp == "3":
        inp = input("Enter a link: ")
        headers = input("Headers (as json): [{}] ")
        if not headers:
            headers = {}
        else:
            headers = json.loads(headers)
        test_link(Link(inp, headers=headers))
    else:
        print("Invalid input; quitting...")