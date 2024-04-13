import requests, json, time
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
current_date = datetime.now()

valid_channels = ["tsn", "sn", "msg", "abc"]

def filter_month(schedule):
    return schedule["mscd"]["mon"] == current_date.strftime("%B")

def filter_day(schedule):
    return schedule["gdte"] == current_date.strftime("%Y-%m-%d")

def get_games():
    games = []
    schedule_url = "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json"
    r_schedule = requests.get(schedule_url).json()
    month_schedule = list(filter(filter_month, r_schedule["lscd"]))[0]["mscd"]["g"]
    day_schedule = list(filter(filter_day, month_schedule))
    for game in day_schedule:
        home_team = "%s %s" % (game["h"]["tc"], game["h"]["tn"])
        visitor_team = "%s %s" % (game["v"]["tc"], game["v"]["tn"])
        title = "%s vs %s" % (home_team, visitor_team)
        utc_time = datetime(*(time.strptime(game["gdtutc"] + "T" + game["utctm"] + ":00", "%Y-%m-%dT%H:%M:%S")[:6]))
        icon = "http://loodibee.com/wp-content/uploads/nba-%s-logo.png" % (home_team.lower().replace(" ", "-"))
        hrefs = []
        for provider in game["bd"]["b"]:
            if provider["type"] == "tv" and provider["disp"].lower() in valid_channels:
                hrefs.append("https://sports24.icu/nba/%s/%s/%s.html" % (game["gid"], game["gdte"].replace("-", ""), provider["disp"].lower().replace(" ", "")))
            elif provider["disp"] == "ESPN":
                hrefs.append("https://gma2.blab.email/fs2.m3u8")
                hrefs.append("https://ustvgo.tv/espn-live/")
            elif provider["disp"] == "TNT OT":
                hrefs.append("plugin://plugin.video.live.streamspro/?url=plugin%3A%2F%2Fplugin.video.f4mTester%2F%3Fstreamtype%3DHLSRETRY%26amp%3Burl%3Dhttp://us1-external-sources.iptvserver.tv:80/live/kkkrkDp2a9KNwAwGzpb/QT94uK5NNQw4r4Qs/660.m3u8%7Cuser-agent%3DiPad&mode=12")    
                hrefs.append("https://ustvgo.tv/tnt/")
            elif provider["disp"] == "TNT":
                hrefs.append("plugin://plugin.video.live.streamspro/?url=plugin%3A%2F%2Fplugin.video.f4mTester%2F%3Fstreamtype%3DHLSRETRY%26amp%3Burl%3Dhttp://us1-external-sources.iptvserver.tv:80/live/kkkrkDp2a9KNwAwGzpb/QT94uK5NNQw4r4Qs/660.m3u8%7Cuser-agent%3DiPad&mode=12")    
                hrefs.append("https://ustvgo.tv/tnt/")
            elif provider["disp"] == "NBA TV":
                hrefs.append("plugin://plugin.video.live.streamspro/?url=plugin%3A%2F%2Fplugin.video.f4mTester%2F%3Fstreamtype%3DHLSRETRY%26amp%3Burl%3Dhttp://us1-external-sources.iptvserver.tv:80/live/kkkrkDp2a9KNwAwGzpb/QT94uK5NNQw4r4Qs/660.m3u8%7Cuser-agent%3DiPad&mode=12")    
                hrefs.append("https://ustvgo.tv/nba-tv/")
        hrefs.append("https://sports24.icu/nba/%s/%s/%s.html" % (game["gid"], game["gdte"].replace("-", ""), game["h"]["tn"].lower())) # Home
        hrefs.append("https://sports24.icu/nba/%s/%s/%s.html" % (game["gid"], game["gdte"].replace("-", ""), game["v"]["tn"].lower())) # Visitor
        games.append({
            "title": title,
            "icon": icon,
            "links": hrefs,
            "time": utc_time,
            "league": "NBA"
        })
    
    return games

def get_scores_yahoo():
    scores = []
    try:
        r_scores = requests.get("https://api-secure.sports.yahoo.com/v1/editorial/s/scoreboard", params={"leagues": "nba", "date": current_date.strftime("%Y-%m-%d")}).json()
        scoreboard = r_scores["service"]["scoreboard"]
        teams = scoreboard["teams"]
        for game in scoreboard["games"].values():
            home_team_name = teams[game["home_team_id"]]["full_name"]
            away_team_name = teams[game["away_team_id"]]["full_name"]
            home_score = 0
            away_score = 0
            for period in game["game_periods"]:
                home_score += int(period["home_points"])
                away_score += int(period["away_points"])
            status = game["status_display_name"]
            scores.append({
                "home_team": home_team_name,
                "home_score": home_score,
                "away_team": away_team_name,
                "away_score": away_score,
                "status": status
            })
    except:
        pass
    return scores