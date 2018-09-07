import requests
import pprint
import sys
import json

affixes = {}

dungeons = {}
dungeon_slugs = ["ataldazar", "the-underrot",
                 "kings-rest", "temple-of-sethraliss",
                 "the-motherlode",
                 "freehold",  "tol-dagor",
                 "waycrest-manor", "siege-of-boralus",
                 "shrine-of-the-storm",]
runs = []

regions = ["us", "eu", "kr", "tw"]

def parse_response(data):
    global runs
    for d in data["rankings"]:
       
        r = d["run"]
        level = r["mythic_level"]
        level = d["score"]

        if r["dungeon"]["name"] not in dungeons:
            dungeons[r["dungeon"]["name"]] = []
        dungeons[r["dungeon"]["name"]] += [level]

        current_run = [r["dungeon"]["name"], level]
        for c in r["roster"]:
            ch = c["character"]
            spec_class = ch["spec"]["name"] + " " + ch["class"]["name"]
            current_run += [spec_class]
        runs += [current_run]



for rg in regions:
    response = requests.get("https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en")
    data = response.json()
    affixes[rg] = data["title"]

    for ds in dungeon_slugs:
        if affixes[rg] != affixes["us"]:
            continue
        response = requests.get("https://raider.io/api/v1/mythic-plus/runs?season=season-bfa-1&region=" + rg + "&affixes=current&dungeon=" + ds)
        data = response.json()
        parse_response(data)

with open('affixes.json', 'w') as outfile:
    json.dump(affixes, outfile)

with open('dungeons.json', 'w') as outfile:
    json.dump(dungeons, outfile)

with open('runs.json', 'w') as outfile:
    json.dump(runs, outfile)
