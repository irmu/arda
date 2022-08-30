import json, time,logging

from resources.lib.common import tools
from resources.lib.common import source_utils
from resources.lib.common.source_utils import serenRequests



class sources:

    def __init__(self):
        self.domain = "torrentapi.org"
        self.base_link = 'https://torrentapi.org/pubapi_v2.php?app_id=%s' % tools.addonName
        self.search_string = '&mode=search&search_string=%s&token=%s&limit=100&format=json_extended'
        self.threads = []
        self.threadResults = []
        self.token = ''

    def get_token(self):

        url = self.base_link + '&get_token=get_token'
        response = serenRequests().get(url)
        self.token = json.loads(response.text)['token']

    def movie(self, title, year):

        torrent_list = []
        self.get_token()
        title = source_utils.cleanTitle(title)
        url = self.base_link + self.search_string % (tools.quote('%s %s' % (title, year)), self.token)
        response = json.loads(serenRequests().get(url).text)
        if 'error_code' in response:
            pass
        else:
            for i in response['torrent_results']:
                try:
                    torrent = {}
                    torrent['package'] = 'single'
                    torrent['release_title'] = i['title']
                    if not source_utils.filterMovieTitle(torrent['release_title'], title, year):
                        continue
                    torrent['magnet'] = i['download']
                    torrent['seeds'] = i['seeders']
                    torrent['size'] = int((i['size'] / 1024) / 1024)
                    torrent_list.append(torrent)
                except:
                    import traceback
                    traceback.print_exc()
                    continue

        return torrent_list

    def episode(self, simpleInfo, allInfo):
        logging.warning('1')
        torrent_list = []
        self.get_token()
        show_title = simpleInfo['show_title'].replace('.', '')
        show_title = source_utils.cleanTitle(show_title)
        season = simpleInfo['season_number'].zfill(2)
        episode = simpleInfo['episode_number'].zfill(2)
        season_pack_query = '%s s%s' % (show_title, season)
        single_episode_query = '%s s%se%s' % (show_title, season, episode)

        url = self.base_link + self.search_string % (tools.quote(season_pack_query), self.token)
        tools.log(url)
        response = json.loads(serenRequests().get(url).text)
        for i in response:
            tools.log(i)
        if 'error_code' in response:
            tools.log(str(response))
            pass
        else:
            for i in response['torrent_results']:
                try:
                    torrent = {}
                    torrent['package'] = 'season'
                    torrent['release_title'] = i['title']
                    if not source_utils.filterSeasonPack(simpleInfo, torrent['release_title']):
                        continue
                    torrent['magnet'] = i['download']
                    torrent['seeds'] = i['seeders']
                    torrent['size'] = int((i['size'] / 1024) / 1024)
                    torrent_list.append(torrent)
                except  Exception as e:
                    logging.warning(e)
                    #import traceback
                    #traceback.print_exc()
                    continue

        time.sleep(2)

        url = self.base_link + self.search_string % (tools.quote(single_episode_query), self.token)
        response = json.loads(serenRequests().get(url).text)

        if 'error_code' in response:
            pass
        else:
            for i in response['torrent_results']:
                try:
                    torrent = {}
                    torrent['package'] = 'single'
                    torrent['release_title'] = i['title']
                    if not source_utils.filterSingleEpisode(simpleInfo, torrent['release_title']):
                        continue
                    torrent['magnet'] = i['download']
                    torrent['seeds'] = i['seeders']
                    torrent['size'] = int((i['size'] / 1024) / 1024)
                    torrent_list.append(torrent)
                except Exception as e:
                    logging.warning(e)
                    #import traceback
                    #traceback.print_exc()
                    continue
        for i in torrent_list:
            tools.log(i)
        return torrent_list
