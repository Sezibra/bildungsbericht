"""Kapitelebene der Inhaltsverzeichnisse bestimmen und Herausforderungen suchen.

Liest data/interim/toc.csv. Ebene 1 gilt als Kapitelebene, wenn sie mehrere
Einträge hat. Hat sie nur einen Eintrag (Titel des Berichts), gilt Ebene 2.
"""

from pathlib import Path

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
toc = pd.read_csv(PROJEKT / "data" / "interim" / "toc.csv")

# Steuerzeichen und doppelte Leerzeichen entfernen
toc["titel"] = toc["titel"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

anzahl_ebene1 = toc[toc["ebene"] == 1].groupby("jahr").size()
kapitel_ebene = (anzahl_ebene1 > 1).map({True: 1, False: 2})
toc["kapitel_ebene"] = toc["jahr"].map(kapitel_ebene)

print("Kapitelebene pro Jahr:")
print(kapitel_ebene.to_string())
print()

kapitel = toc[(toc["ebene"] == toc["kapitel_ebene"]) & (toc["kapitel_ebene"] == 2)]
for jahr, gruppe in kapitel.groupby("jahr"):
    print(f"--- {jahr} ---")
    for _, z in gruppe.iterrows():
        print(f"{z['seite']:>4}  {z['titel']}")
print()

treffer = toc[toc["titel"].str.contains("herausforderung", case=False)]
print("Einträge mit 'Herausforderung' (alle Ebenen):")
for _, z in treffer.iterrows():
    print(f"{z['jahr']}  Ebene {z['ebene']}  S. {z['seite']:>4}  {z['titel']}")