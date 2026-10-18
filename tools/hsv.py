import requests

BASE = "https://api.openligadb.de"
SAISON = 2026
HSV_ID = 100


def hole_daten(pfad):
    antwort = requests.get(f"{BASE}/{pfad}", timeout=10)
    antwort.raise_for_status()
    return antwort.json()


def endergebnis(spiel):
    for ergebnis in spiel["matchResults"]:
        if ergebnis["resultTypeID"] == 2:
            return ergebnis["pointsTeam1"], ergebnis["pointsTeam2"]
    return None


# --- 1. Alle Spiele holen und HSV-Spiele herausfiltern ---
spiele = hole_daten(f"getmatchdata/bl1/{SAISON}")

hsv_spiele = []
for spiel in spiele:
    if spiel["team1"]["teamId"] == HSV_ID or spiel["team2"]["teamId"] == HSV_ID:
        hsv_spiele.append(spiel)

hsv_spiele = sorted(hsv_spiele, key=lambda s: s["matchDateTimeUTC"])
print(f"HSV-Spiele in der Saison: {len(hsv_spiele)}")

# --- 2. In gespielt und offen aufteilen ---
gespielt = [s for s in hsv_spiele if s["matchIsFinished"]]
offen = [s for s in hsv_spiele if not s["matchIsFinished"]]

# --- 3. Ergebnisse aus HSV-Sicht ---
print("\n=== Bisherige Ergebnisse ===")
form = []
for spiel in gespielt:
    tore1, tore2 = endergebnis(spiel)
    hsv_ist_heim = spiel["team1"]["teamId"] == HSV_ID

    if hsv_ist_heim:
        hsv_tore, gegner_tore = tore1, tore2
        gegner = spiel["team2"]["teamName"]
    else:
        hsv_tore, gegner_tore = tore2, tore1
        gegner = spiel["team1"]["teamName"]

    if hsv_tore > gegner_tore:
        ergebnis = "S"
    elif hsv_tore == gegner_tore:
        ergebnis = "U"
    else:
        ergebnis = "N"
    form.append(ergebnis)

    ort = "H" if hsv_ist_heim else "A"
    spieltag = spiel["group"]["groupName"]
    print(f"{spieltag:<13} ({ort})  {gegner:<28} {hsv_tore}:{gegner_tore}  {ergebnis}")

print(f"\nForm (letzte 5): {' '.join(form[-5:])}")

# --- 4. Nächstes Spiel ---
if offen:
    naechstes = offen[0]
    heim = naechstes["team1"]["teamName"]
    gast = naechstes["team2"]["teamName"]
    print(f"\nNächstes Spiel: {heim} – {gast} ({naechstes['matchDateTime']})")

# --- 5. HSV in der Tabelle ---
tabelle = hole_daten(f"getbltable/bl1/{SAISON}")
for platz, team in enumerate(tabelle, start=1):
    if team["teamInfoId"] == HSV_ID:
        print(f"Tabelle: Platz {platz}, {team['points']} Punkte, "
              f"Tore {team['goals']}:{team['opponentGoals']}")