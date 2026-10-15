"""Layout prüfen: Blockpositionen, erkannte Überschriften, weiche Trennzeichen."""

from pathlib import Path
import re

import pandas as pd
import pymupdf

from abschnitte import ist_fett

PROJEKT = Path(__file__).resolve().parents[1]
PDF_ORDNER = PROJEKT / "data" / "raw" / "berichte"
KORPUS = PROJEKT / "data" / "processed" / "korpus_absaetze.csv"
ZUORDNUNG = PROJEKT / "data" / "interim" / "kapitel_zuordnung.csv"
SEITEN = [(2014, 96), (2024, 180), (2012, 92)]
MUSTER = re.compile(r"\w+\u00ad[a-zäöüß]\w*")

print("A) Textblöcke mit Position")
for jahr, p in SEITEN:
    with pymupdf.open(PDF_ORDNER / f"{jahr}.pdf") as doc:
        seite = doc[p - 1]
        print(f"--- {jahr} S.{p}, Seitenbreite {seite.rect.width:.0f} ---")
        for block in seite.get_text("dict")["blocks"]:
            spans = [s for l in block.get("lines", []) for s in l["spans"] if s["text"].strip()]
            if not spans:
                continue
            x0, y0, x1, _ = block["bbox"]
            text = " ".join(s["text"] for s in spans).replace("\u00ad", "|")
            groesse = max(s["size"] for s in spans)
            fett = "F" if all(ist_fett(s) for s in spans) else " "
            print(f"  x {x0:4.0f}-{x1:4.0f} b {x1 - x0:4.0f} y {y0:4.0f} "
                  f"{groesse:4.1f} {fett} {len(text):4}  {text[:55]}")

print("\nB) Zufällige erkannte Überschriften")
korpus = pd.read_csv(KORPUS)
for jahr in (2006, 2024):
    ue = korpus[(korpus["jahr"] == jahr) & (korpus["typ"] == "ueberschrift")]
    print(f"--- {jahr} ---")
    for _, z in ue.sample(15, random_state=4).iterrows():
        print(f"  {z['kapitel']} S.{z['seite']}: {z['text'][:90]}")

print("\nC) Weiches Trennzeichen mitten in der Zeile vor Kleinbuchstaben")
zuordnung = pd.read_csv(ZUORDNUNG)
for jahr in (2020, 2022):
    k = zuordnung[zuordnung["jahr"] == jahr]
    von, bis = int(k["von"].min()), int(k["bis"].max())
    treffer = []
    with pymupdf.open(PDF_ORDNER / f"{jahr}.pdf") as doc:
        for p in range(von, bis + 1):
            for zeile in doc[p - 1].get_text("text").splitlines():
                treffer += MUSTER.findall(zeile)
    print(f"--- {jahr}: {len(treffer)} Treffer ---")
    print("  " + ", ".join(t.replace("\u00ad", "|") for t in treffer[:25]))