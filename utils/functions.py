import requests
import sqlite3
import json
import shutil

lang = json.load(open('JSON/lang.json', 'r', encoding='UTF-8'))

# Function to download images from a URL
def dl_img(url, name):
    r = requests.get(url, stream=True)
    if r.status_code is 200:
        with open(name, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def getTranslation(guildID, key1, key2):
    """ Get translation keys for different settings """
    db = sqlite3.connect('SQL/settings.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT guild_id, lang FROM serversettings WHERE guild_id = '{guildID}'")
    res = cursor.fetchone() 
    if res is not None:
        return lang[res[1]][key1][key2]
    else:
        return lang['en'][key1][key2]
