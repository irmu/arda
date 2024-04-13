from datetime import datetime

from ..models.Link import Link
from ..models.Game import Game
from ..models.Extractor import Extractor
from pyairtable import Table
current_date = datetime.now()

class Aust(Extractor):
    def __init__(self) -> None:
        self.name = "Aust"
        self.short_name = "Aust"

    def get_games(self):
        channels_table = Table("key", "app", "Australia")
        m3u8_table = Table("key", "app", "IPTVmine1")

        channels_records = channels_table.all(sort=["number"])
        m3u8_records = m3u8_table.all()

        m3u8s = {}
        for m3u8_record in m3u8_records:
            record_id = m3u8_record["id"]
            fields = m3u8_record["fields"]
            urls = []
            # if "url" in fields and "://" in fields["url"]: urls.append(unidecode(fields["url"]))
            if "SERVER2" in fields and "://" in fields["SERVER2"]: urls.append(Link(address=fields["SERVER2"]))
            # if "SERVER2" in fields and "://" in fields["SERVER2"]: urls.append("ffmpegdirect://" + fields["SERVER2"])
            if "SERVER" in fields and "://" in fields["SERVER"]: urls.append(Link(address=fields["SERVER"], is_ffmpegdirect=True))
            # if "test" in fields and "://" in fields["test"]: urls.append("PlayMedia(&quot;pvr://channels/tv/All%20channels/pvr.iptvsimple_" + unidecode(fields["test"]))
            # for i in range(1, 5):
            #     if "link" + str(i) in fields:
            #         url = fields["link" + str(i)]
            #         if "://" in url: urls.append(unidecode(url))
            m3u8s[record_id] = urls

        games = []
        for record in channels_records:
            fields = record["fields"]
            if "name" in fields:
                name = fields["name"]
                thumbnail = fields.get("icon", "")
                urls = []
                if "url" in fields and fields["url"] != "-": urls.append(Link(fields["url"].strip()))
                if "link1" in fields and fields["link1"] != "-": urls.append(Link(fields["link1"].strip()))
                if "IPTVmine1" in fields and fields["IPTVmine1"] != "-":
                    for record_id in fields["IPTVmine1"]: urls.extend(m3u8s[record_id])
                if "IPTVCAT" in fields and fields["IPTVCAT"] != "-":
                    for record_id in fields["IPTVCAT"]: urls.extend(m3u8s[record_id])    
                games.append(Game(title=name, links=urls, icon=thumbnail))
        
        return games