import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

def get_games():
    games = []
    scores = {}
    schedule = requests.get("https://statsapi.mlb.com/api/v1/schedule", params={"sportId": "1"}).json()["dates"][0]["games"]
    for game in schedule:
        name = "%s at %s" % (game["teams"]["away"]["team"]["name"], game["teams"]["home"]["team"]["name"])
        scores[name] = game
    
    r = requests.get("https://sports24.icu/mlb/").text
    soup = BeautifulSoup(r, "html.parser")
    for game in soup.select("div.card-body"):
        if len(game.select(".teamlogo")) == 0: continue
        game_name = game.select_one("h4.card-title").text
        hrefs = []
        for href in game.select("div.game-feeds > a"):
            link = href.get("href")
            if link.startswith("//"): continue
            elif link.startswith("/"):
                link = "https://sports24.icu" + link
            hrefs.append(link)
        game_scores = scores[game_name]
        if "score" in game_scores["teams"]["home"]: game_title = "[COLORorange]%s %s-%s[/COLOR]: %s vs %s" % (game_scores["status"]["detailedState"], game_scores["teams"]["home"]["score"], game_scores["teams"]["away"]["score"], game_scores["teams"]["home"]["team"]["name"], game_scores["teams"]["away"]["team"]["name"])
        else: game_title = "[COLORorange]%s[/COLOR]: %s vs %s" % (game_scores["status"]["detailedState"], game_scores["teams"]["home"]["team"]["name"], game_scores["teams"]["away"]["team"]["name"])
        game_icon = "https:" + game.select_one("img.teamlogo").get("src")
        game_time = datetime(*(time.strptime(game_scores["gameDate"], "%Y-%m-%dT%H:%M:%SZ")[:6]))
        games.append({
            "title": game_title,
            "league": "MLB",
            "icon": game_icon,
            "links": hrefs,
            "time": game_time
        })

    return games
