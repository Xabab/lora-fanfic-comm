from pathlib import Path
import shutil
from parse_favorites_list import *
from os import listdir

if __name__ == "__main__":
    favs = load_favorites("RPLogs_writing.json")
    local_files = {}
    
    for f in listdir('./txt/pool/'):
        local_files[f.split('_')[0]] = './txt/pool/' + f
    

    favs = [ fav for fav in favs if fav.item_id in local_files.keys()]
    
    favs.sort(key=lambda x: x.favorites, reverse=True)
    
    for f in favs:
        print(f.favorites)

    pool = [ fav for fav in favs if fav.favorites > 20]
    
    print(len(pool))
    
    path = Path('./txt/pool selected/')
    if path.exists(): shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)

    for fav in pool:
        shutil.copyfile(local_files[fav.item_id], "./txt/pool selected/" + local_files[fav.item_id].split('/')[-1])