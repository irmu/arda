import threading, requests

from bs4 import BeautifulSoup
from resources.lib.common import tools
from resources.lib.common import source_utils

class sources:

    def __init__(self):
        self.domain = "bitlordsearch.com"
        self.base_link = 'https://bitlordsearch.com/'
        self.search_link = 'search?q=%s'
        self.threads = []
        self.threadResults = []

    def getList(self, url):
        torrent_list = []
        try:
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
            response = requests.get(url, headers=headers)
            results = BeautifulSoup(response.text, 'html.parser')
            results = results.find_all('tr', {'class': 'bls-row'})

            for i in results:
                torrent = {}
                torrent['magnet'] = i.find_all('a', {'magnet-button'})[0]['href']
                torrent['release_title'] = i.find_all('span', {'class': 'title'})[0].text
                torrent['seeds'] = int(i.find_all('td', {'class': 'seeds'})[0].text)
                torrent['size'] = int(i.find_all('td', {'class': 'size'})[0].text)
                torrent_list.append(torrent)
            return torrent_list
        except:
            import traceback
            traceback.print_exc()
            pass

        return torrent_list

    def movie(self, title, year):
        title = source_utils.cleanTitle(title)

        url = self.base_link + self.search_link % tools.quote('%s %s' % (title, year))
        results = self.getList(url)

        torrent_list = []
        for i in results:
            try:
                if source_utils.filterMovieTitle(i['release_title'], title, year):
                    i['package'] = 'single'
                    torrent_list.append(i)
                else:
                    continue
            except:
                import traceback
                traceback.print_exc()
                continue
        return torrent_list

    def episode(self, simpleInfo, allInfo):
        self.threads.append(threading.Thread(target=self.seasonPack, args=(simpleInfo, allInfo)))
        self.threads.append(threading.Thread(target=self.singleEpisode, args=(simpleInfo, allInfo)))
        self.threads.append(threading.Thread(target=self.showPack, args=(simpleInfo, allInfo)))

        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        return self.threadResults

    def showPack(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])

            url = self.base_link + self.search_link % tools.quote('%s season 1-%s' % (showTitle, simpleInfo['no_seasons']))
            results = self.getList(url)

            url = self.base_link + self.search_link % tools.quote('%s complete' % showTitle)
            results += self.getList(url)

            torrent_list = []

            for i in results:
                try:
                    if not source_utils.filterShowPack(simpleInfo, i['release_title']):
                        continue
                    else:
                        i['package'] = 'show'
                        torrent_list.append(i)
                except:
                    continue

            self.threadResults += torrent_list

        except:
            import traceback
            traceback.print_exc()
            pass


    def seasonPack(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])

            url = self.base_link + self.search_link % tools.quote('%s season %s' % (showTitle, simpleInfo['season_number']))
            results = self.getList(url)
            torrent_list = []

            for torrent in results:
                try:
                    torrent = {}

                    if not source_utils.filterSeasonPack(simpleInfo, torrent['release_title']):
                        continue
                    else:
                        torrent['package'] = 'season'
                        torrent_list.append(torrent)
                except:
                    continue

            self.threadResults += torrent_list

        except:
            import traceback
            traceback.print_exc()
            pass

    def singleEpisode(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])
            season = simpleInfo['season_number'].zfill(2)
            episode = simpleInfo['episode_number'].zfill(2)

            url = self.base_link + self.search_link % tools.quote('%s s%se%s' % (showTitle, season, episode))
            results = self.getList(url)

            torrent_list = []

            for torrent in results:
                try:
                    if not source_utils.filterSingleEpisode(simpleInfo, torrent['release_title']):
                        continue
                    else:
                        torrent['package'] = 'single'
                        torrent_list.append(torrent)
                except:
                    continue

            self.threadResults += torrent_list
        except:
            import traceback
            traceback.print_exc()
            pass