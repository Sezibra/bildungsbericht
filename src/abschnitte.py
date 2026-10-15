"""Abschnitt 'Zentrale Herausforderungen' ausschneiden.

Start: Lesezeichen mit diesem Titel, sonst erste Seite mit einer Zeile,
die genau dieser Überschrift entspricht (nur vor Kapitel A).
Ende: Seite vor dem Beginn von Kapitel A.
Extraktion über die Schriftinformation:
- Zeilen kleiner als der Fließtext entfallen (Seitenzahl, Kolumnentitel, Fußnote).
- Eine Folge fetter Zeilen gleicher Größe, größer als der Fließtext, gilt als
  Zwischenüberschrift und steht zwischen <<UE>> und <</UE>>. Ausnahme: Beginnt
  die nächste Zeile fett und geht in normalen Text über, ist die Folge ein
  Leitsatz und bleibt Text.
Text pro Jahr in data/interim/abschnitte/ speichern.
"""

from collections import Counter
from pathlib import Path
import re

import pymupdf
import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
PDF_ORDNER = PROJEKT / "data" / "raw" / "berichte"
TOC = PROJEKT / "data" / "interim" / "toc.csv"
AUSGABE = PROJEKT / "data" / "interim" / "abschnitte"
TITEL = "zentrale herausforderungen"
KAPITEL_A = r"^a\b|spannungsfeld"
UE_START = "<<UE>>"
UE_ENDE = "<</UE>>"
TOLERANZ = 0.3  # Punkt, für Abweichungen wie 9,6 statt 9,5


def normalisiere(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def kapitelebene(toc_jahr):
    return 1 if (toc_jahr["ebene"] == 1).sum() > 1 else 2


def kapitel_a_start(toc_jahr):
    kapitel = toc_jahr[toc_jahr["ebene"] == kapitelebene(toc_jahr)]
    titel = kapitel["titel"].map(normalisiere)
    treffer = kapitel[titel.str.contains(KAPITEL_A, regex=True) & (kapitel["seite"] > 0)]
    return int(treffer["seite"].min()) if len(treffer) else None


def lesezeichen_start(toc_jahr):
    treffer = toc_jahr[toc_jahr["titel"].map(normalisiere) == TITEL]
    return int(treffer["seite"].iloc[0]) if len(treffer) else None


def seiten_mit_ueberschrift(doc):
    seiten = []
    for nr, seite in enumerate(doc, start=1):
        zeilen = [normalisiere(z) for z in seite.get_text("text").splitlines()]
        if TITEL in zeilen:
            seiten.append(nr)
    return seiten


def ist_fett(span):
    return bool(span["flags"] & 16) or "bold" in span["font"].lower()


def bloecke_der_seite(seite):
    """Pro Textblock eine Liste von Zeilen als Dictionary."""
    bloecke = []
    for block in seite.get_text("dict")["blocks"]:
        zeilen = []
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            text = "".join(s["text"] for s in line["spans"]).strip()
            if not re.search(r"\w", text):
                continue
            zeilen.append({"text": text,
                           "groesse": round(max(s["size"] for s in spans), 1),
                           "fett": all(ist_fett(s) for s in spans),
                           "beginnt_fett": ist_fett(spans[0])})
        if zeilen:
            bloecke.append(zeilen)
    return bloecke


def fliesstextgroesse(doc, start, ende):
    gewicht = Counter()
    for p in range(start, ende + 1):
        for block in bloecke_der_seite(doc[p - 1]):
            for zeile in block:
                gewicht[zeile["groesse"]] += len(zeile["text"])
    return gewicht.most_common(1)[0][0]


def seite_als_text(seite, fliesstext):
    ausgabe, ueberschriften = [], 0
    for block in bloecke_der_seite(seite):
        block = [z for z in block if z["groesse"] >= fliesstext - TOLERANZ]
        i = 0
        while i < len(block):
            zeile = block[i]
            if not (zeile["fett"] and zeile["groesse"] > fliesstext + TOLERANZ):
                ausgabe.append(zeile["text"])
                i += 1
                continue
            # Folge fetter Zeilen gleicher Größe
            j = i
            while (j < len(block) and block[j]["fett"]
                   and block[j]["groesse"] == zeile["groesse"]):
                j += 1
            texte = [z["text"] for z in block[i:j]]
            leitsatz = j < len(block) and block[j]["beginnt_fett"]
            if not leitsatz and normalisiere(" ".join(texte)) != TITEL:
                ausgabe += [UE_START, *texte, UE_ENDE]
                ueberschriften += 1
            else:
                ausgabe += texte
            i = j
    return "\n".join(ausgabe), ueberschriften


def main():
    toc = pd.read_csv(TOC)
    AUSGABE.mkdir(parents=True, exist_ok=True)
    tabelle = []

    for pfad in sorted(PDF_ORDNER.glob("*.pdf")):
        jahr = int(re.search(r"(20[0-2]\d)", pfad.name).group(1))
        toc_jahr = toc[toc["jahr"] == jahr]
        with pymupdf.open(pfad) as doc:
            a_start = kapitel_a_start(toc_jahr)
            start = lesezeichen_start(toc_jahr)
            quelle = "lesezeichen"
            if start is None:
                vor_a = [s for s in seiten_mit_ueberschrift(doc) if a_start and s < a_start]
                start = min(vor_a) if vor_a else None
                quelle = "ueberschrift"
            if start is None or a_start is None:
                tabelle.append({"jahr": jahr, "start": "", "ende": "", "quelle": "",
                                "fliesstext": "", "ueberschriften": 0, "zeichen": 0})
                continue
            ende = a_start - 1
            fliesstext = fliesstextgroesse(doc, start, ende)
            teile, anzahl = [], 0
            for p in range(start, ende + 1):
                text, n = seite_als_text(doc[p - 1], fliesstext)
                teile.append(text)
                anzahl += n
            text = "\n".join(teile)
            (AUSGABE / f"zentrale_herausforderungen_{jahr}.txt").write_text(text, encoding="utf-8")
            tabelle.append({"jahr": jahr, "start": start, "ende": ende, "quelle": quelle,
                            "fliesstext": fliesstext, "ueberschriften": anzahl,
                            "zeichen": len(text)})

    print(pd.DataFrame(tabelle).to_string(index=False))
    print(f"\nGespeichert in: {AUSGABE}")


if __name__ == "__main__":
    main()