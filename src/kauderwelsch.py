"""Absätze mit defekter Zeichenkodierung finden.

Merkmal: 'ß' direkt vor Großbuchstabe oder Sonderzeichen, mindestens 3 Mal.
"""

from collections import Counter
from pathlib import Path
import re

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
KORPUS = PROJEKT / "data" / "processed" / "korpus_absaetze.csv"
MUSTER = re.compile(r"ß[A-Z%&\"#$'()*+,\-./0-9]")
SCHWELLE = 3

korpus = pd.read_csv(KORPUS)
korpus["verdacht"] = korpus["text"].str.count(MUSTER)
betroffen = korpus[korpus["verdacht"] >= SCHWELLE]

print(f"Betroffene Einheiten gesamt: {len(betroffen)} von {len(korpus)}")
if len(betroffen):
    uebersicht = betroffen.groupby("jahr").agg(
        einheiten=("text", "size"),
        zeichen=("zeichen", "sum"),
        kapitel=("kapitel", lambda s: ", ".join(sorted(set(s)))),
        seiten=("seite", lambda s: ", ".join(map(str, sorted(set(s))))),
    )
    print(uebersicht.to_string())

    print("\nBeispiele:")
    for _, z in betroffen.sample(min(4, len(betroffen)), random_state=1).iterrows():
        print(f"  {z['jahr']} {z['kapitel']} S.{z['seite']} ({z['typ']}): {z['text'][:200]}")

    zeichen = Counter("".join(betroffen["text"]))
    print("\nZeichen in betroffenen Texten (Zeichen, Anzahl):")
    print("  " + "  ".join(f"{c!r}:{n}" for c, n in sorted(zeichen.items())))