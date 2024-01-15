import os
import json
import requests

config={
        "title":"UNotes (v0.2.0)",
        "version": "0.2.0",
        "theme": "Light",
        "font": "Lucida Console",
        "font-size": 12,
        "font-size-index": 2,
        "icons": {
        	"save":	"./icons/save.png",
        	"open":	"./icons/open.png",
        	"new":	"./icons/new.png",
        	"exit":	"./icons/exit.png",
            "icon": "./icons/icon.png",
            "preferences": "./icons/preferences.png"
        }
    }

def initConfig():
    if os.path.exists("./config.json"):
        d = json.loads(open("./config.json").read())
        for i in d: config[i] = d[i]
        with open("./config.json", "w") as jsonfile:
            json.dump(config, jsonfile, indent='\t')
    else:
        openfile=open("./config.json","w")
        d = {}
        for i in d: config[i] = d[i]
        openfile.write(json.dumps(config, indent='\t'))
        openfile.close()


def initIcons(config):
    icons = [
        "https://codewars-dm.web.app/assets/save.png", 
        "https://codewars-dm.web.app/assets/open.png", 
        "https://codewars-dm.web.app/assets/new.png", 
        "https://codewars-dm.web.app/assets/preferences.png",
        "https://codewars-dm.web.app/assets/icon.png",
        "https://codewars-dm.web.app/assets/exit.png"
    ]

    if not os.path.exists("./icons"):
        os.mkdir("./icons")
    
    for i in config["icons"]:
        i += ".png"
        if os.path.exists("./icons/"+i) == False:
            for j in icons:
                if i == j.split('/')[-1]:
                    missing = j
            r = requests.get(missing, allow_redirects=True)
            open("./icons/"+i, "wb").write(r.content)