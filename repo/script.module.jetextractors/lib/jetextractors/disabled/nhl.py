import requests, time
from datetime import datetime, timedelta
from unidecode import unidecode
current_date = datetime.now()
current_date_str = current_date.strftime("%Y-%m-%d")

domain = []

def get_games():
    games = []
    api = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=%s&endDate=%s&hydrate=broadcasts(all),game(content(media(epg)),seriesSummary)&site=en_nhl&teamId=&gameType=&timecode=' % (current_date_str, current_date_str)
    r_schedule = requests.get(api).json()
    events = r_schedule["dates"][0]["games"]
    for game in events:
        home_team = unidecode(game["teams"]["home"]["team"]["name"])
        visitor_team = unidecode(game["teams"]["away"]["team"]["name"])
        title = "%s vs %s" % (home_team, visitor_team)
        icon = "http://loodibee.com/wp-content/uploads/nhl-%s-logo.png" % (home_team.lower().replace(" ", "-"))
        utc_time = datetime(*(time.strptime(game["gameDate"], "%Y-%m-%dT%H:%M:%SZ")[:6]))
        game_id = game["gamePk"]
        hrefs = []
        for broadcast in game["content"]["media"]["epg"][0]["items"]:
            hrefs.append("https://sports24.icu/nhl/%s/%s.html" % (game_id, broadcast["mediaPlaybackId"]))
        games.append({
            "title": title,
            "league": "NHL",
            "icon": icon,
            "links": hrefs,
            "time": utc_time
        })
    
    return games

def get_scores_yahoo():
    scores = []
    r_scores = requests.get("https://api-secure.sports.yahoo.com/v1/editorial/s/scoreboard", params={"leagues": "nhl", "date": current_date_str}).json()
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
    return scores