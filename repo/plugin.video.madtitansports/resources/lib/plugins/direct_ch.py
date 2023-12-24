from ..external.airtable.airtable import Airtable
from resources.lib.plugin import Plugin
from resources.lib.plugin import run_hook
import xbmcgui
from jetextractors.models.Link import Link

class DirectCH(Plugin):
    name = "jet_direct_ch"
    priority = 100

    def process_item(self, item):
        if self.name in item:
            link = item.get(self.name, "")
            thumbnail = item.get("thumbnail", "")
            fanart = item.get("fanart", "")
            item["link"] = f"jet_direct_ch/{link}"
            item["is_dir"] = True
            list_item = xbmcgui.ListItem(item.get("title", item.get("name", "")), offscreen=True)
            list_item.setArt({"thumb": thumbnail, "fanart": fanart})
            item["list_item"] = list_item
            return item
    
    def routes(self, plugin):
        @plugin.route(f"/{self.name}/channels")
        def channels():
            channels_table = Airtable("apphTihiHBetdFgK8", "DIRECT_CHANNELS", api_key="keyvWT1TdSyCaibez")
            m3u8_table = Airtable("apphTihiHBetdFgK8", "IPTVmine1", api_key="keyvWT1TdSyCaibez")

            channels_records = channels_table.get_all(sort=["number"])
            m3u8_records = m3u8_table.get_all()

            m3u8s = {}
            for m3u8_record in m3u8_records:
                record_id = m3u8_record["id"]
                fields = m3u8_record["fields"]
                urls = []
                # if "url" in fields and "://" in fields["url"]: urls.append(unidecode(fields["url"]))
                if "SERVER2" in fields and "://" in fields["SERVER2"]: urls.append(Link(address=fields["SERVER2"]))
                # if "inks" in fields and "://" in fields["inks"]: urls.append("ffmpegdirect://" + unidecode(fields["inks"]))
                # if "test" in fields and "://" in fields["test"]: urls.append("PlayMedia(&quot;pvr://channels/tv/All%20channels/pvr.iptvsimple_" + unidecode(fields["test"]))
                # for i in range(1, 5):
                #     if "link" + str(i) in fields:
                #         url = fields["link" + str(i)]
                #         if "://" in url: urls.append(unidecode(url))
                m3u8s[record_id] = urls

            jen_list = []
            for record in channels_records:
                fields = record["fields"]
                if "name" in fields:
                    name = fields["name"]
                    thumbnail = fields.get("icon", "")
                    urls = []
                    if "url" in fields and fields["url"] != "-": urls.append(Link(address=fields["url"].strip()))
                if "link1" in fields and fields["link1"] != "-": urls.append(Link(address=fields["link1"].strip()))
                if "IPTVmine1" in fields and fields["IPTVmine1"] != "-":
                    for record_id in fields["IPTVmine1"]: urls.extend(m3u8s[record_id])
                    # if "IPTVCAT" in fields and fields["IPTVCAT"] != "-":
                        # for record_id in fields["IPTVCAT"]: urls.extend(m3u8s[record_id])
                    jen_list.append({
                        "title": name,
                        "thumbnail": thumbnail,
                        "fanart": thumbnail,
                        "sportjetextractors": [l.to_dict() for l in urls],
                        "type": "item"
                    })

            jen_list = [run_hook("process_item", item) for item in jen_list]
            jen_list = [run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list]
            run_hook("display_list", jen_list)
