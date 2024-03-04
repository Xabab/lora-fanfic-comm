import requests
from bs4 import BeautifulSoup as bs
import time
import json


class Favorite:
    def __init__(self, item_id, autor, title, media_type, tags = None, favorites = None, views = None, comments = None) -> None:
        self.item_id    = item_id
        self.autor      = autor
        self.title      = title
        self.media_type = media_type
        self.tags       = tags
        self.favorites  = favorites
        self.views      = views
        self.comments   = comments
        


def parse_faworites_list():
    s = requests.Session()

    s.cookies.update({
        "style_cookie"                        : "null",
        "has_js"                              : "1",
        "phpbb3_rl7a3_k"                      : "",
        "phpbb3_rl7a3_u"                      : "00000",
        "phpbb3_rl7a3_sid"                    : "00000",
        "SESS00000"                           : "00000"})


    url = "https://[redacted]/favorites/username?p="

    i = 1
    
    favorites = []
    
    print("Parsing list of favorites:")

    while(True):
        print(f"Parsing page # {i}")
        
        p = s.get(url + str(i))
        b = bs(p.content, "html.parser")
        items = b.find_all("li", class_="gallery-item")

        if (len(items)==0 or i > 1000): break

        for item in items:
            item_id = item.attrs["id"]
            autor = item.find(class_="user-link").text
            title = item.find(class_="item-title").text
            media_type = item.find(class_="biicon11").attrs["class"][1].split('-')[1]

            favorites.append(Favorite(item_iaryion.com/g4d, autor, title, media_type))
            
        i+=1
            
        time.sleep(0.3)
        
    with open("RPLogs.json", "w+") as f:
        json_string = json.dumps([ob.__dict__ for ob in favorites], indent=4)
        f.write(json_string)
        
    return favorites
        
        
def parse_writings(favorites):
    s = requests.Session()

    s.cookies.update({
        "style_cookie"                        : "null",
        "has_js"                              : "1",
        "phpbb3_rl7a3_k"                      : "",
        "phpbb3_rl7a3_u"                      : "00000",
        "phpbb3_rl7a3_sid"                    : "00000",
        "SESS00000"                           : "00000"})
    
    url_fav = "https://[redacted]/view/"
        
    i = 0
    
    print("Parsing \"Writing\" items:")
        
    for fav in favorites:
        i+=1
        
        print(f"Parsing item {i} out of {len(favorites)}")
        
        print(fav.__dict__)
        
        if fav.media_type != "Writing": continue
        
        p = s.get(url_fav + fav.item_id)
        b = bs(p.content, "html.parser")
        
        tags = []
        
        try:
            taglist = list(b.find("span", class_="taglist").children)
        except AttributeError:
            taglist = None


        if taglist:
            for tag in taglist:
                if tag.text == " ": continue
                tags.append(tag.text.lower())

        try: 
            fav.tags       = tags
            fav.favorites  = int(b.find("b", string="Favorites").parent.text.split()[1].replace(",", ""))
            fav.views      = int(b.find("b", string="Views").parent.text.split()[1].replace(",", ""))
            fav.comments   = int(b.find("b", string="Comments").parent.text.split()[1].replace(",", ""))
        except AttributeError:
            fav.tags       = []
            fav.favorites  = 0
            fav.views      = 0
            fav.comments   = 0

        print(fav.__dict__)
        
        time.sleep(0.3)
    
    
    with open("RPLogs.json", "w+") as f:
        json_string = json.dumps([ob.__dict__ for ob in favorites], indent=4)
        f.write(json_string)
        
    favorites_writing = [fav for fav in favorites if fav.media_type == "Writing"]
    
    with open("RPLogs_writing.json", "w+") as f:
        json_string = json.dumps([ob.__dict__ for ob in favorites_writing], indent=4)
        f.write(json_string)
        
    return favorites_writing


def load_favorites(filepath):
    favs = None
    
    with open(filepath, "r") as f:
        favs = json.loads(f.read())
        
    favs_objects = []
        
    for fav in favs:
        fav_object = Favorite(**fav)
        favs_objects.append(fav_object)
        
    return favs_objects
        
    
if __name__ == "__main__":
    favorites = load_favorites("RPLogs.json")
    
    parse_writings(favorites)
    