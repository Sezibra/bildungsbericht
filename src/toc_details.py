"""Tiefere Lesezeichen für ausgewählte Seitenbereiche anzeigen."""

from pathlib import Path
import re

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
toc = pd.read_csv(PROJEKT / "data" / "interim" / "toc.csv")
toc["titel"] = toc["titel"].map(lambda t: re.sub(r"\s+", " ", str(t)).strip())


def zeige(jahr, von, bis, max_ebene):
    t = toc[(toc["jahr"] == jahr) & toc["seite"].between(von, bis) & (toc["ebene"] <= max_ebene)]
    print(f"--- {jahr}, Seiten {von} bis {bis}, bis Ebene {max_ebene} ---")
    for _, z in t.iterrows():
        einzug = "  " * (z["ebene"] - 1)
        print(f"  S.{z['seite']:>4}  E{z['ebene']}  {einzug}{z['titel'][:80]}")


zeige(2006, 185, 216, 3)
zeige(2018, 200, 262, 3)
zeige(2026, 1, 60, 4)