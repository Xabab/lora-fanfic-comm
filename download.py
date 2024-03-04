import requests
from bs4 import BeautifulSoup as bs
import time
import json
from parse_favorites_list import *
from pathlib import Path
import re

def download(favorites):
    s = requests.Session()

    s.cookies.update({
        "style_cookie"                        : "null",
        "has_js"                              : "1",
        "phpbb3_rl7a3_k"                      : "",
        "phpbb3_rl7a3_u"                      : "00000",
        "phpbb3_rl7a3_sid"                    : "00000",
        "SESS00000"                           : "00000"})
    
    download_url = "https://[redacted]/data.php?id="
    
    i = 0

    for fav in favorites:
        i+=1
        
        print(f"Downloading item {i} out of {len(favorites)}")
        
        print(fav.__dict__)

        try:
            r = requests.get(download_url + fav.item_id)
            filename = r.headers['content-disposition']
            filename = re.findall("filename=(.+)", filename)[0]
            
            path = Path('./rp files/' + fav.item_id)
            path.mkdir(parents=True, exist_ok=True)
            
            open("./rp files/"  + fav.item_id + '/' +  filename.replace("\"", "").replace("\\\\", "\\"), "wb").write(r.content)
        except KeyError:
            print("KeyError", fav.item_id)
        except FileNotFoundError:
            print("FileNotFoundError", fav.item_id)
        finally:
            time.sleep(0.3)
        
    


if __name__ == "__main__":
    download(load_favorites("RPLogs.json"))