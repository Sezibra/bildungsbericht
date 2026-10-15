"""Korpus: alle Berichte als Absätze mit Metadaten.

Grundlage: data/interim/kapitel_zuordnung.csv (Seitenbereiche und Kapitelcodes).
Regeln:
- Position relativ zur Seitenbreite: Blöcke in der Registerleiste entfallen,
  Blöcke in der Randspalte erhalten den Typ 'randnotiz' (links auf geraden,
  rechts auf ungeraden Seiten).
- Zeilen kleiner als der Fließtext entfallen (Fußnote, Beschriftung,
  Seitenzahl, Kolumnentitel).
- Folgen fetter Zeilen gleicher Größe, größer als der Fließtext, sind
  Überschriften, außer bei Leitsätzen (nächste Zeile beginnt fett).
- Ein Textblock ist ein Absatz. Endet der letzte Textabsatz ohne Satzzeichen,
  gehört der nächste Textblock dazu. Ausnahmen: voriger Teil unter 40 Zeichen,
  Überschrift dazwischen, neues Kapitel. Randnotizen unterbrechen nicht.
- Fußnotenziffern direkt nach Buchstabe und Satzzeichen entfallen.
- Typ 'tabelle_abbildung': beginnt mit 'Abb.' oder 'Tab.', Nummer, Doppelpunkt.
- Typ 'fragment': Text unter 40 Zeichen ohne Satzzeichen am Ende,
  Überschrift mit höchstens 3 Zeichen.
- Nach Ziffern bleibt der Bindestrich erhalten ('6-jährigen').
Analyse nutzt nur die Typen 'text' und 'ueberschrift'.
Ergebnis: data/processed/korpus_absaetze.csv
"""

from collections import Counter
from pathlib import Path
import re

import pymupdf
import pandas as pd

from abschnitte import TOLERANZ, ist_fett
from bereinigung import glaette, loese_trennung_auf, repariere_zeichen, segmente

PROJEKT = Path(__file__).resolve().parents[1]
PDF_ORDNER = PROJEKT / "data" / "raw" / "berichte"
ZUORDNUNG = PROJEKT / "data" / "interim" / "kapitel_zuordnung.csv"
AUSGABE = PROJEKT / "data" / "processed" / "korpus_absaetze.csv"

SCHWERPUNKT = {
    2006: "Migration",
    2008: "Übergänge: Schule, Berufsausbildung, Hochschule, Arbeitsmarkt",
    2010: "Perspektiven des Bildungswesens im demografischen Wandel",
    2012: "Kulturelle/musisch-ästhetische Bildung im Lebenslauf",
    2014: "Menschen mit Behinderungen im Bildungssystem",
    2016: "Bildung und Migration",
    2018: "Wirkungen und Erträge von Bildung",
    2020: "Bildung in einer digitalisierten Welt",
    2022: "Bildungspersonal: Struktur, Entwicklung, Qualität und Professionalisierung",
    2024: "Berufliche Bildung",
    2026: "Bildungsungleichheiten nach sozialer Herkunft",
}
REITER = 0.055  # Registerleiste: äußerste 5,5 Prozent der Seitenbreite
RAND = 0.27     # Randspalte: Block endet vor 27 Prozent oder beginnt nach 73 Prozent
SATZENDE = tuple('.!?:;"“”)')
TAB_ABB = re.compile(r"^(abb|tab)\.\s*[a-i]\d+[-–]\d+\w*\s*:", re.IGNORECASE)
FUSSNOTE = re.compile(r"(?<=[^\W\d][.!?;:)])\d{1,3}(?=\s|$)")
WEICH_MITTEN = re.compile(r"\w\u00ad[a-zäöüß]")
ZIFFERNREICH = 0.25
FRAGMENT_ZEICHEN = 40
UEBERSCHRIFT_MIN = 4


def bloecke_mit_position(seite):
    breite = seite.rect.width
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
            bloecke.append({"x0": block["bbox"][0] / breite,
                            "x1": block["bbox"][2] / breite,
                            "zeilen": zeilen})
    return bloecke


def einheiten_der_seite(bloecke, fliesstext):
    """Liste von (typ, rohtext, seite_der_randspalte)."""
    ergebnis = []
    for block in bloecke:
        if block["x1"] < REITER or block["x0"] > 1 - REITER:
            continue  # Registerleiste
        zeilen = [z for z in block["zeilen"] if z["groesse"] >= fliesstext - TOLERANZ]
        if not zeilen:
            continue
        if block["x1"] < RAND or block["x0"] > 1 - RAND:
            rand = "links" if block["x1"] < RAND else "rechts"
            ergebnis.append(("randnotiz", "\n".join(z["text"] for z in zeilen), rand))
            continue
        textzeilen, i = [], 0
        while i < len(zeilen):
            zeile = zeilen[i]
            if zeile["fett"] and zeile["groesse"] > fliesstext + TOLERANZ:
                j = i
                while (j < len(zeilen) and zeilen[j]["fett"]
                       and zeilen[j]["groesse"] == zeile["groesse"]):
                    j += 1
                folge = [z["text"] for z in zeilen[i:j]]
                if j < len(zeilen) and zeilen[j]["beginnt_fett"]:
                    textzeilen += folge  # Leitsatz gehört zum Absatz
                else:
                    if textzeilen:
                        ergebnis.append(("text", "\n".join(textzeilen), ""))
                        textzeilen = []
                    ergebnis.append(("ueberschrift", "\n".join(folge), ""))
                i = j
            else:
                textzeilen.append(zeile["text"])
                i += 1
        if textzeilen:
            ergebnis.append(("text", "\n".join(textzeilen), ""))
    return ergebnis


def endet_mit_satz(text):
    return FUSSNOTE.sub("", text.rstrip()).endswith(SATZENDE)


def bindestrich_nach_ziffer(text):
    text = re.sub(r"(?<=\d)[-\u00ad][ \t]*\n\s*(?=[a-zäöüß])", "-", text)
    return re.sub(r"(?<=\d)\u00ad(?=[a-zäöüß])", "-", text)


def verarbeite_bericht(jahr, kapitel):
    with pymupdf.open(PDF_ORDNER / f"{jahr}.pdf") as doc:
        seiten = {}
        for _, k in kapitel.iterrows():
            for p in range(int(k["von"]), int(k["bis"]) + 1):
                seiten[p] = (k["code"], bloecke_mit_position(doc[p - 1]))

    gewicht = Counter()
    for _, bloecke in seiten.values():
        for block in bloecke:
            for zeile in block["zeilen"]:
                gewicht[zeile["groesse"]] += len(zeile["text"])
    fliesstext = gewicht.most_common(1)[0][0]

    roh, letzter_text = [], None
    for p in sorted(seiten):
        code, bloecke = seiten[p]
        for typ, text, rand in einheiten_der_seite(bloecke, fliesstext):
            if typ == "randnotiz":
                roh.append({"typ": typ, "roh": text, "seite": p, "kapitel": code, "rand": rand})
                continue
            if typ == "ueberschrift":
                roh.append({"typ": typ, "roh": text, "seite": p, "kapitel": code, "rand": ""})
                letzter_text = None
                continue
            if (letzter_text is not None and letzter_text["kapitel"] == code
                    and len(letzter_text["roh"]) >= FRAGMENT_ZEICHEN
                    and not endet_mit_satz(letzter_text["roh"])):
                letzter_text["roh"] += "\n" + text
            else:
                letzter_text = {"typ": typ, "roh": text, "seite": p, "kapitel": code, "rand": ""}
                roh.append(letzter_text)

    zeilen, weich_mitten = [], 0
    for einheit in roh:
        weich_mitten += len(WEICH_MITTEN.findall(einheit["roh"]))
        text = bindestrich_nach_ziffer(repariere_zeichen(einheit["roh"]))
        text = loese_trennung_auf(text, jahr)
        if einheit["typ"] in ("ueberschrift", "randnotiz"):
            teile = [(einheit["typ"], re.sub(r"\s*\n\s*", " ", text))]
        else:
            teile = segmente(text)
        for typ, teil in teile:
            teil = FUSSNOTE.sub("", glaette(teil))
            if not teil:
                continue
            if TAB_ABB.match(teil):
                typ = "tabelle_abbildung"
            elif typ == "text" and len(teil) < FRAGMENT_ZEICHEN and not teil.endswith(SATZENDE):
                typ = "fragment"
            elif typ == "ueberschrift" and len(teil) < UEBERSCHRIFT_MIN:
                typ = "fragment"
            zeilen.append({
                "jahr": jahr,
                "kapitel": einheit["kapitel"],
                "schwerpunkt": SCHWERPUNKT[jahr],
                "seite": einheit["seite"],
                "typ": typ,
                "rand": einheit["rand"],
                "text": teil,
                "zeichen": len(teil),
                "ziffernanteil": round(sum(c.isdigit() for c in teil) / len(teil), 3),
            })
    return zeilen, fliesstext, weich_mitten


def beispiele(df, titel, anzahl, seed):
    print(f"\n{titel}:")
    for _, z in df.sample(min(anzahl, len(df)), random_state=seed).iterrows():
        print(f"  {z['jahr']} {z['kapitel']} S.{z['seite']}: {z['text'][:120]}")


def main():
    zuordnung = pd.read_csv(ZUORDNUNG)
    alle, uebersicht = [], []
    for jahr, kapitel in zuordnung.groupby("jahr"):
        print(f"Verarbeite {jahr} ...")
        zeilen, fliesstext, weich_mitten = verarbeite_bericht(jahr, kapitel)
        df = pd.DataFrame(zeilen)
        text = df[df["typ"] == "text"]
        uebersicht.append({
            "jahr": jahr,
            "text": len(text),
            "ueberschr": (df["typ"] == "ueberschrift").sum(),
            "rand_links": ((df["typ"] == "randnotiz") & (df["rand"] == "links")).sum(),
            "rand_rechts": ((df["typ"] == "randnotiz") & (df["rand"] == "rechts")).sum(),
            "fragment": (df["typ"] == "fragment").sum(),
            "tab_abb": (df["typ"] == "tabelle_abbildung").sum(),
            "zeichen_text": text["zeichen"].sum(),
            "median": int(text["zeichen"].median()),
            "ziffernreich": round((text["ziffernanteil"] > ZIFFERNREICH).mean(), 3),
        })
        alle += zeilen

    korpus = pd.DataFrame(alle)
    AUSGABE.parent.mkdir(parents=True, exist_ok=True)
    korpus.to_csv(AUSGABE, index=False, encoding="utf-8-sig")

    print()
    print(pd.DataFrame(uebersicht).to_string(index=False))
    beispiele(korpus[korpus["typ"] == "fragment"], "Fragmente", 6, 6)
    beispiele(korpus[korpus["typ"] == "text"], "Zufällige Absätze", 5, 2)
    print(f"\nGespeichert: {AUSGABE}")


if __name__ == "__main__":
    main()