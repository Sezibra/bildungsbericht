"""Inhaltsverzeichnisse der Bildungsberichte auslesen.

Speichert alle Lesezeichen (Jahr, Ebene, Titel, Seite) in data/interim/toc.csv
und zeigt die Anzahl der Einträge pro Ebene sowie alle Einträge der Ebene 1.
"""

from pathlib import Path
import re

import pymupdf
import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
PDF_ORDNER = PROJEKT / "data" / "raw" / "berichte"
AUSGABE = PROJEKT / "data" / "interim" / "toc.csv"


def main():
    zeilen = []
    for pfad in sorted(PDF_ORDNER.glob("*.pdf")):
        jahr = int(re.search(r"(20[0-2]\d)", pfad.name).group(1))
        with pymupdf.open(pfad) as doc:
            for ebene, titel, seite in doc.get_toc():
                zeilen.append({"jahr": jahr, "ebene": ebene,
                               "titel": titel.strip(), "seite": seite})

    df = pd.DataFrame(zeilen)
    AUSGABE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(AUSGABE, index=False, encoding="utf-8-sig")

    print("Einträge pro Jahr und Ebene:")
    print(pd.crosstab(df["jahr"], df["ebene"]))
    print()
    for jahr, gruppe in df[df["ebene"] == 1].groupby("jahr"):
        print(f"--- {jahr} ---")
        for _, z in gruppe.iterrows():
            print(f"{z['seite']:>4}  {z['titel']}")
    print(f"\nGespeichert: {AUSGABE}")


if __name__ == "__main__":
    main()