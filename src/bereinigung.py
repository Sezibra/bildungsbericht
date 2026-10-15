"""Bereinigung der extrahierten Texte.

Reihenfolge:
1. Zeichen reparieren (Windows-1252-Steuerzeichen, Ligaturen mit Leerzeichen,
   NFKC, Bindestrichvarianten)
2. Text vor der Überschrift abschneiden (nur Jahrgänge ohne Lesezeichen)
3. Restliche Seitenzahlen und Kolumnentitel entfernen
4. Silbentrennung auflösen
5. Segmente bilden: Zwischenüberschriften (zwischen <<UE>> und <</UE>>),
   Aufzählungspunkte, Fließtext
Ergebnis: data/processed/abschnitte/ und
          data/processed/segmente_zentrale_herausforderungen.csv
"""

from pathlib import Path
import re
import unicodedata

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
EINGABE = PROJEKT / "data" / "interim" / "abschnitte"
AUSGABE = PROJEKT / "data" / "processed" / "abschnitte"
TABELLE = PROJEKT / "data" / "processed" / "segmente_zentrale_herausforderungen.csv"

UEBERSCHRIFT = "zentrale herausforderungen"
KOLUMNENTITEL = {"wichtige ergebnisse im überblick", "zentrale herausforderungen"}
UE_START = "<<UE>>"
UE_ENDE = "<</UE>>"
# Start über die Überschrift bestimmt: Text davor gehört zum vorigen Abschnitt
SCHNITT_JAHRE = {2010, 2012, 2014, 2016, 2020}
# Jahrgänge, die feste Bindestriche als weiches Trennzeichen kodieren
HARTE_TRENNZEICHEN_JAHRE = {2020}
KLEIN = "a-zäöüß"
GROSS = "A-ZÄÖÜ"
TRENN = "[-\u00ad]"
KONJUNKTION = r"(und|oder|bzw|sowie)\b"
LIGATUREN = "[\ufb00-\ufb04]"
# Eigenständige Wörter nach einer Ligatur: nicht anhängen ("Begriff und")
EIGENSTAENDIG = {"und", "oder", "in", "im", "zu", "zum", "zur", "der", "die", "das",
                 "des", "den", "dem", "ein", "eine", "sich", "ist", "sind", "wird",
                 "werden", "auch", "als", "bei", "mit", "von", "vom", "für", "auf",
                 "an", "am", "nicht", "so", "wie", "aus", "nach"}


def normalisiere(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def verbinde_ligaturen(text):
    def ersetze(m):
        ligatur, wort = m.group(1), m.group(2)
        return f"{ligatur} {wort}" if wort in EIGENSTAENDIG else f"{ligatur}{wort}"
    return re.sub(rf"({LIGATUREN}) ([{KLEIN}]+)", ersetze, text)


def repariere_zeichen(text):
    # C1-Steuerzeichen stammen aus falsch dekodiertem Windows-1252 (U+0084 steht für „)
    text = re.sub(r"[\x80-\x9f]",
                  lambda m: bytes([ord(m.group())]).decode("cp1252", errors="replace"),
                  text)
    text = verbinde_ligaturen(text)
    # NFKC löst Ligaturen auf und ersetzt geschützte und schmale Leerzeichen
    text = unicodedata.normalize("NFKC", text)
    return text.replace("\u2010", "-").replace("\u2011", "-")


def schneide_vor_ueberschrift(text):
    zeilen = text.splitlines()
    for i, zeile in enumerate(zeilen):
        if normalisiere(zeile) == UEBERSCHRIFT:
            return "\n".join(zeilen[i + 1:])
    return text


def entferne_seitenrauschen(text):
    behalten = []
    for zeile in text.splitlines():
        n = normalisiere(zeile)
        if not n or n.isdigit() or n in KOLUMNENTITEL:
            continue
        behalten.append(zeile)
    return "\n".join(behalten)


def loese_trennung_auf(text, jahr):
    # weiches Trennzeichen nach Leerzeichen hat keine Funktion
    text = re.sub(r"(?<=\s)\u00ad", "", text)
    # Ergänzungsstrich vor Konjunktion: "Schul-" + "und" wird "Schul- und"
    text = re.sub(rf"{TRENN}[ \t]*\n\s*(?={KONJUNKTION})", "- ", text)
    text = re.sub(rf"\u00ad(?= {KONJUNKTION})", "-", text)
    # Trennung am Zeilenende vor Kleinbuchstaben: Wortteile verbinden
    text = re.sub(rf"(?<=\w){TRENN}[ \t]*\n\s*(?=[{KLEIN}])", "", text)
    # Trennung am Zeilenende vor Großbuchstaben: fester Bindestrich
    text = re.sub(rf"(?<=\w){TRENN}[ \t]*\n\s*(?=[{GROSS}])", "-", text)
    # weiches Trennzeichen mitten in der Zeile
    if jahr in HARTE_TRENNZEICHEN_JAHRE:
        text = re.sub(r"\u00ad(?=\w)", "-", text)
    else:
        text = re.sub(rf"\u00ad(?=[{GROSS}])", "-", text)
    return text.replace("\u00ad", "")


def segmente(text):
    ergebnis, aktuell, typ = [], [], "text"

    def abschliessen():
        if aktuell:
            ergebnis.append((typ, " ".join(aktuell)))

    for zeile in text.splitlines():
        zeile = zeile.strip()
        if zeile == UE_START:
            abschliessen()
            aktuell, typ = [], "ueberschrift"
        elif zeile == UE_ENDE:
            abschliessen()
            aktuell, typ = [], "text"
        elif typ == "text" and zeile.startswith("•"):
            abschliessen()
            aktuell = [zeile.lstrip("• ").strip()]
        elif zeile:
            aktuell.append(zeile)
    abschliessen()
    return ergebnis


def glaette(text):
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r" (?=[.,;:!?)])", "", text).strip()


def bereinige(text, jahr):
    text = repariere_zeichen(text)
    if jahr in SCHNITT_JAHRE:
        text = schneide_vor_ueberschrift(text)
    text = entferne_seitenrauschen(text)
    text = loese_trennung_auf(text, jahr)
    return [(typ, glaette(t)) for typ, t in segmente(text) if t.strip()]


def main():
    AUSGABE.mkdir(parents=True, exist_ok=True)
    alle = []
    for datei in sorted(EINGABE.glob("zentrale_herausforderungen_*.txt")):
        jahr = int(datei.stem[-4:])
        segs = bereinige(datei.read_text(encoding="utf-8"), jahr)
        text = "\n".join(f"## {t}" if typ == "ueberschrift" else t for typ, t in segs)
        (AUSGABE / datei.name).write_text(text, encoding="utf-8")
        for nr, (typ, t) in enumerate(segs, start=1):
            alle.append({"jahr": jahr, "nr": nr, "typ": typ, "text": t})

        ueberschriften = [t for typ, t in segs if typ == "ueberschrift"]
        print(f"--- {jahr} --- Segmente {len(segs)}, davon Überschriften {len(ueberschriften)}, "
              f"Zeichen {len(text)}")
        for u in ueberschriften:
            print(f"  ## {u}")
        print(f"  Anfang Text: {next((t for typ, t in segs if typ == 'text'), '')[:120]}")

    pd.DataFrame(alle).to_csv(TABELLE, index=False, encoding="utf-8-sig")
    print(f"\nGespeichert: {TABELLE}")


if __name__ == "__main__":
    main()