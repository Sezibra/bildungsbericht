"""Schriftinformation in den Abschnitten 'Zentrale Herausforderungen' prüfen.

Pro Jahrgang: Fließtextgröße (Größe mit den meisten Zeichen) und alle Zeilen,
die davon abweichen oder vollständig fett sind. Grundlage für die Regel zur
Erkennung von Zwischenüberschriften.
"""

from collections import Counter
from pathlib import Path

import pymupdf

PROJEKT = Path(__file__).resolve().parents[1]
PDF_ORDNER = PROJEKT / "data" / "raw" / "berichte"
# Seitenbereiche aus abschnitte.py
BEREICHE = {2010: (27, 28), 2012: (26, 28), 2014: (25, 26), 2016: (29, 32),
            2018: (34, 38), 2020: (44, 46), 2022: (50, 54), 2024: (58, 60),
            2026: (50, 56)}
MAX_ZEILEN = 25


def ist_fett(span):
    return bool(span["flags"] & 16) or "bold" in span["font"].lower()


for jahr, (start, ende) in BEREICHE.items():
    zeilen = []
    with pymupdf.open(PDF_ORDNER / f"{jahr}.pdf") as doc:
        for p in range(start, ende + 1):
            for block in doc[p - 1].get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    spans = [s for s in line["spans"] if s["text"].strip()]
                    if not spans:
                        continue
                    text = "".join(s["text"] for s in spans).strip()
                    groesse = round(max(s["size"] for s in spans), 1)
                    fett = all(ist_fett(s) for s in spans)
                    zeilen.append((p, groesse, fett, spans[0]["font"], text))

    gewicht = Counter()
    for _, groesse, _, _, text in zeilen:
        gewicht[groesse] += len(text)
    fliesstext = gewicht.most_common(1)[0][0]

    print(f"--- {jahr} --- Fließtextgröße {fliesstext}, "
          f"Zeichen pro Größe: {dict(gewicht.most_common(5))}")
    kandidaten = [z for z in zeilen if z[1] != fliesstext or z[2]]
    for p, groesse, fett, schrift, text in kandidaten[:MAX_ZEILEN]:
        print(f"  S.{p:<3} {groesse:>5} {'fett' if fett else '    '} "
              f"{schrift[:22]:<22} {text[:60]}")
    if len(kandidaten) > MAX_ZEILEN:
        print(f"  ... {len(kandidaten) - MAX_ZEILEN} weitere")