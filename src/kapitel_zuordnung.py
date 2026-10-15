"""Einheitliche Kapitelcodes pro Bericht.

Codes: EIN (Einleitung), UEB (Überblicksteil), A bis I (Kapitel).
Ableitung:
1. Buchstabe am Titelanfang.
2. Ohne Buchstaben: Abgleich mit Standardtiteln (2018).
3. Einträge ohne Code gehören zum vorherigen Kapitel
   (2006: 'Zusammenfassung und Perspektiven' ist Teil von H).
Sonderfälle:
- 2018: 'Wirkungen und Erträge von Bildung' ist das Schwerpunktkapitel H,
  ein Kapitel I fehlt.
- 2026: Einleitung umfasst Seiten 21 bis 24, der Überblicksteil 25 bis 56
  (Zentrale Befunde, Trends und Problemlagen, Zentrale Herausforderungen).
Ergebnis: data/interim/kapitel_zuordnung.csv
"""

from pathlib import Path
import re

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
EINGABE = PROJEKT / "data" / "interim" / "kapitel.csv"
AUSGABE = PROJEKT / "data" / "interim" / "kapitel_zuordnung.csv"

CODES = ["EIN", "UEB", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
STANDARDTITEL = [
    ("spannungsfeld", "A"),
    ("grundinformationen", "B"),
    ("frühkindliche|frühe bildung", "C"),
    ("allgemein ?bildende schule", "D"),
    ("berufliche ausbildung", "E"),
    ("hochschule", "F"),
    ("weiterbildung", "G"),
]
SONDERFAELLE = {(2018, "wirkungen und erträge von bildung"): "H"}
TEILUNGEN = {
    2026: [("EIN", "Einleitung", 21, 24),
           ("UEB", "Zentrale Befunde, Trends und Problemlagen, Zentrale Herausforderungen", 25, 56)],
}


def normalisiere(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def kapitelcode(jahr, titel):
    n = normalisiere(titel)
    if n.startswith("einleitung"):
        return "EIN"
    if "wichtige ergebnisse" in n or n == "zusammenfassung":
        return "UEB"
    treffer = re.match(r"^([a-i])\b", n)
    if treffer:
        return treffer.group(1).upper()
    if (jahr, n) in SONDERFAELLE:
        return SONDERFAELLE[(jahr, n)]
    for muster, buchstabe in STANDARDTITEL:
        if re.search(muster, n):
            return buchstabe
    return None


def main():
    kapitel = pd.read_csv(EINGABE)
    zeilen = []
    for jahr, k in kapitel.groupby("jahr"):
        eintraege = []
        for _, z in k.sort_values("von").iterrows():
            code = kapitelcode(jahr, z["kapitel"])
            if code is None and eintraege:
                eintraege[-1]["bis"] = z["bis"]  # gehört zum vorherigen Kapitel
                continue
            eintraege.append({"jahr": jahr, "code": code, "titel": z["kapitel"],
                              "von": z["von"], "bis": z["bis"]})
        if jahr in TEILUNGEN:
            teile = TEILUNGEN[jahr]
            bereiche = [(von, bis) for _, _, von, bis in teile]
            eintraege = [e for e in eintraege
                         if not any(von <= e["von"] <= bis for von, bis in bereiche)]
            eintraege += [{"jahr": jahr, "code": c, "titel": t, "von": von, "bis": bis}
                          for c, t, von, bis in teile]
        zeilen += sorted(eintraege, key=lambda e: e["von"])

    df = pd.DataFrame(zeilen)
    df["seiten"] = df["bis"] - df["von"] + 1
    df.to_csv(AUSGABE, index=False, encoding="utf-8-sig")

    print("Seiten pro Kapitelcode und Jahr:")
    tabelle = df.pivot_table(index="jahr", columns="code", values="seiten", aggfunc="sum")
    print(tabelle.reindex(columns=CODES).fillna(0).astype(int).to_string())
    print()
    print("Schwerpunktkapitel H:")
    for _, z in df[df["code"] == "H"].iterrows():
        print(f"  {z['jahr']}  {z['titel'][:80]}")
    fehlend = df[df["code"].isna()]
    if len(fehlend):
        print("\nOhne Code:")
        print(fehlend.to_string(index=False))
    print(f"\nGespeichert: {AUSGABE}")


if __name__ == "__main__":
    main()