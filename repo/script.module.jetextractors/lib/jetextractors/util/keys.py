import requests, base64

class Keys():
    mlb = ""
    nhl = ""
    sling = ""
    

    def get_key(key):
        key = base64.b64decode(key).decode('utf-8')
        if key.startswith("http"):
            if key.endswith(".json"):
                key = requests.get(key).json()
            else:
                key = requests.get(key).text
        if type(key) == str:
            key = key.strip()
        return key