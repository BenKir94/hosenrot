import requests
import json

BASE = "https://api.openligadb.de"
SAISON = 2026      # OpenLigaDB zählt die Saison 2026/27 als 2026
HSV_ID = 100

# 1) Tabelle holen
tabelle = requests.get(f"{BASE}/getbltable/bl1/{SAISON}").json()
print(type(tabelle), len(tabelle))
print(json.dumps(tabelle[0], indent=2, ensure_ascii=False))

# 2) Alle Spiele der Saison holen
spiele = requests.get(f"{BASE}/getmatchdata/bl1/{SAISON}").json()
print(len(spiele))
print(json.dumps(spiele[0], indent=2, ensure_ascii=False))