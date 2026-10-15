"""Inventar der Bildungsberichte.

Prüft für jede PDF im Ordner data/raw/berichte:
Seitenzahl, Dateigröße, Anteil der Seiten mit Textebene,
Umfang des eingebetteten Inhaltsverzeichnisses und Passwortschutz.
Ergebnis: data/interim/inventar.csv und eine Tabelle in der Konsole.
"""

from pathlib import Path
import re

import fitz  # PyMuPDF
import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
PDF_ORDNER = PROJEKT / "data" / "raw" / "berichte"
AUSGABE = PROJEKT / "data" / "interim" / "inventar.csv"

# Seiten mit weniger Zeichen gelten als Seiten ohne Textebene (Bild, Leerseite)
MIN_ZEICHEN = 200


def jahr_aus_dateiname(name):
    treffer = re.search(r"(20[0-2]\d)", name)
    return int(treffer.group(1)) if treffer else None


def pruefe_pdf(pfad):
    zeile = {"datei": pfad.name, "jahr": jahr_aus_dateiname(pfad.name)}
    with fitz.open(pfad) as doc:
        if doc.needs_pass:
            zeile["hinweis"] = "passwortgeschuetzt"
            return zeile
        zeichen = [len(seite.get_text("text").strip()) for seite in doc]
        toc = doc.get_toc()
        zeile.update({
            "seiten": doc.page_count,
            "mb": round(pfad.stat().st_size / 1e6, 1),
            "anteil_textseiten": round(sum(z >= MIN_ZEICHEN for z in zeichen) / doc.page_count, 3),
            "zeichen_gesamt": sum(zeichen),
            "toc_eintraege": len(toc),
            "toc_ebenen": max((eintrag[0] for eintrag in toc), default=0),
        })
    return zeile


def main():
    pdfs = sorted(PDF_ORDNER.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"Keine PDFs gefunden in {PDF_ORDNER}")

    zeilen = []
    for pfad in pdfs:
        print(f"Pruefe {pfad.name} ...")
        try:
            zeilen.append(pruefe_pdf(pfad))
        except Exception as fehler:
            zeilen.append({"datei": pfad.name, "jahr": jahr_aus_dateiname(pfad.name),
                           "hinweis": f"Fehler: {fehler}"})

    df = pd.DataFrame(zeilen).sort_values("jahr")
    AUSGABE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(AUSGABE, index=False, encoding="utf-8-sig")
    print()
    print(df.to_string(index=False))
    print(f"\nGespeichert: {AUSGABE}")


if __name__ == "__main__":
    main()