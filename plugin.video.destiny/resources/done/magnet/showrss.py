from bs4 import BeautifulSoup

from resources.lib.common import tools
from resources.lib.common import source_utils
from resources.lib.common. source_utils import serenRequests
import re,logging

class sources:

    def __init__(self):
        self.domain = "showrss.info"
        self.base_link = 'https://showrss.info'
        self.search_link = '/browse'
        self.feed_url = '/show/%s.rss'

    def episode(self, simpleInfo, allInfo):
        logging.warning(simpleInfo)
        torrent_list = []
        show_title = source_utils.cleanTitle(simpleInfo['show_title'])
        year = simpleInfo['year']
        country = simpleInfo['country']
        show_string_list = [
            show_title,
            '%s %s' % (show_title, year),
            '%s %s' % (show_title, country)
        ]
        response = serenRequests().get(self.base_link + self.search_link)
        show_list = BeautifulSoup(response.text, 'html.parser').find_all('option')
        show_id = None
        for show in show_list:
            if source_utils.cleanTitle(show.text.lower()) in [i.lower() for i in show_string_list]:
                show_id = show['value']

        if show_id is None: return

        response = serenRequests().get(self.base_link + self.feed_url % show_id)
        torrents = BeautifulSoup(response.text, 'html.parser').find_all('item')
        for item in torrents:
            try:
                if '%sx%s' % (simpleInfo['season_number'], simpleInfo['episode_number'].zfill(2)) in item.find(
                        'title').text:
                    torrent = {}
                    torrent['package'] = 'single'
                    torrent['release_title'] = re.findall(r'<tv:raw_title>(.*?)</tv:raw_title>', str(item))[0]
                    torrent['magnet'] = re.findall(r'<link/>(.*?)<guid', str(item))[0]
                    torrent['seeds'] = 0
                    torrent_list.append(torrent)
            except:
                pass

        return torrent_list

