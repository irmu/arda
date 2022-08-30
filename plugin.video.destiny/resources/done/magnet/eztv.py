from bs4 import BeautifulSoup
from resources.lib.common import tools
from resources.lib.common import source_utils
from resources.lib.common. source_utils import serenRequests


class sources:

    def __init__(self):
        self.domain = "eztv.ag"
        self.base_link = 'https://eztv.ag'
        self.search_link = '/search/%s'

    def episode(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])
            season = simpleInfo['season_number'].zfill(2)
            episode = simpleInfo['episode_number'].zfill(2)

            url = self.base_link + self.search_link % tools.quote_plus('%s s%se%s' % (showTitle, season, episode))
            response = serenRequests().get(url)
            results = BeautifulSoup(response.text, 'html.parser').find_all('tr', {'class': 'forum_header_border'})

            torrent_list = []

            for i in results:
                try:
                    torrent = {}
                    torrent['package'] = 'single'
                    torrent['release_title'] = i.find('a', {'class': 'epinfo'}).text
                    if not source_utils.filterSingleEpisode(simpleInfo, torrent['release_title']):
                        continue

                    torrent['magnet'] = i.find('a', {'class': 'magnet'})['href']
                    size = i.find_all('td')[3].text
                    size = source_utils.de_string_size(size)
                    torrent['size'] = size
                    torrent['seeds'] = 0
                    torrent_list.append(torrent)
                except:
                    continue

            return torrent_list
        except:
            import traceback
            traceback.print_exc()
            pass
