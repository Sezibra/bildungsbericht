"""Korpusgrenzen und Kapitel pro Bericht bestimmen.

Start: erstes Lesezeichen 'Einleitung' (alle Ebenen).
Ende: Seite vor dem ersten Anhangselement auf Kapitelebene
      (Literaturverzeichnis, Tabellenanhang oder 'L').
Kapitel: Einträge der Kapitelebene sowie Einleitung, Wichtige Ergebnisse
         und Zusammenfassung auf allen Ebenen.
Ergebnis: data/interim/kapitel.csv
"""

from pathlib import Path
import re

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
TOC = PROJEKT / "data" / "interim" / "toc.csv"
AUSGABE = PROJEKT / "data" / "interim" / "kapitel.csv"

ANFANG = r"^einleitung"
SCHLUSS = r"literaturverzeichnis|tabellenanhang|^l$|^l\b"
RAHMENTEILE = r"^einleitung|wichtige ergebnisse|^zusammenfassung"


def normalisiere(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def main():
    toc = pd.read_csv(TOC)
    toc["titel"] = toc["titel"].map(lambda t: re.sub(r"\s+", " ", str(t)).strip())
    toc["norm"] = toc["titel"].map(normalisiere)
    alle_kapitel = []

    for jahr, t in toc.groupby("jahr"):
        kapitelebene = 1 if (t["ebene"] == 1).sum() > 1 else 2
        t = t[t["seite"] > 0]

        einleitung = t[t["norm"].str.contains(ANFANG, regex=True)]
        start = int(einleitung["seite"].min())
        schluss = t[(t["ebene"] == kapitelebene)
                    & t["norm"].str.contains(SCHLUSS, regex=True)
                    & (t["seite"] > start)]
        ende = int(schluss["seite"].min()) - 1

        kandidaten = t[(t["ebene"] == kapitelebene)
                       | t["norm"].str.contains(RAHMENTEILE, regex=True)]
        kandidaten = kandidaten[(kandidaten["seite"] >= start) & (kandidaten["seite"] <= ende)]
        kandidaten = kandidaten.sort_values("seite").drop_duplicates("seite", keep="first")

        starts = kandidaten["seite"].tolist()
        enden = [s - 1 for s in starts[1:]] + [ende]
        print(f"--- {jahr}: Seiten {start} bis {ende} ({ende - start + 1} Seiten) ---")
        for (_, k), von, bis in zip(kandidaten.iterrows(), starts, enden):
            print(f"  {von:>4} bis {bis:>4}  {k['titel'][:70]}")
            alle_kapitel.append({"jahr": jahr, "kapitel": k["titel"],
                                 "von": von, "bis": bis})

    pd.DataFrame(alle_kapitel).to_csv(AUSGABE, index=False, encoding="utf-8-sig")
    print(f"\nGespeichert: {AUSGABE}")


if __name__ == "__main__":
    main()