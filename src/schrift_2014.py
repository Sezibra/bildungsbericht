"""Defekte Schrift im Bericht 2014 identifizieren."""

from collections import defaultdict
from pathlib import Path
import re

import pymupdf

PROJEKT = Path(__file__).resolve().parents[1]
PDF = PROJEKT / "data" / "raw" / "berichte" / "2014.pdf"
SEITEN = [15, 16, 18, 19, 23, 25, 174, 176, 181, 189, 190, 197, 200, 202,
          203, 204, 205, 212, 213, 215, 216]
KORPUS_SEITEN = range(15, 229)
MUSTER = re.compile(r"ß[A-Z%&\"#$'()*+,\-./0-9]")


def spans(seite):
    for block in seite.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if span["text"].strip():
                    yield span


statistik = defaultdict(lambda: {"stuecke": 0, "zeichen": 0, "treffer": 0})
beispiele = defaultdict(list)
with pymupdf.open(PDF) as doc:
    for p in SEITEN:
        for span in spans(doc[p - 1]):
            eintrag = statistik[span["font"]]
            eintrag["stuecke"] += 1
            eintrag["zeichen"] += len(span["text"])
            eintrag["treffer"] += len(MUSTER.findall(span["text"]))
            if len(beispiele[span["font"]]) < 3 and len(span["text"]) > 20:
                beispiele[span["font"]].append((p, span["text"][:70]))

    print("Schriften auf den 21 Seiten:")
    for schrift, e in sorted(statistik.items(), key=lambda x: -x[1]["zeichen"]):
        print(f"  {schrift:<35} Stücke {e['stuecke']:>5}  Zeichen {e['zeichen']:>6}  "
              f"Treffer {e['treffer']:>4}")

    verdaechtig = [s for s, e in statistik.items() if e["treffer"] > 0]
    print("\nBeispiele verdächtiger Schriften:")
    for schrift in verdaechtig:
        print(f"  {schrift}")
        for p, text in beispiele[schrift]:
            print(f"    S.{p}: {text}")

    print("\nVorkommen verdächtiger Schriften im ganzen Korpus 2014:")
    for schrift in verdaechtig:
        seiten, zeichen = set(), 0
        for p in KORPUS_SEITEN:
            for span in spans(doc[p - 1]):
                if span["font"] == schrift:
                    seiten.add(p)
                    zeichen += len(span["text"])
        print(f"  {schrift}: {zeichen} Zeichen auf {len(seiten)} Seiten: "
              f"{', '.join(map(str, sorted(seiten)))}")