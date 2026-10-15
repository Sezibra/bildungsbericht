"""Defekt kodierte Textstellen im Bericht 2014 dekodieren.

Regel (Verschiebung um 32 Positionen):
- Zeichen U+0001 bis U+005E werden um 0x20 verschoben: Großbuchstaben zu
  Kleinbuchstaben, '!' bis '?' zu Großbuchstaben, Steuerzeichen zu Ziffern
  und Satzzeichen.
- 'ß' steht für das Leerzeichen und trennt Teilstücke, 'i' steht für 'ä'.
- Unbekannte Zeichen: Kandidat mit den meisten Treffern im sauberen
  Wortschatz des Berichts 2014, zwei Durchgänge.
Erkennung: 'ß' direkt vor Großbuchstabe oder Steuerzeichen als Ausgangspunkt,
Erweiterung auf benachbarte Wörter aus Zeichen der defekten Kodierung.
Teilstücke:
- ohne normales Ende (Kleinbuchstaben): ganz dekodieren
- normales Ende mit mindestens 2 Zeichen davor: nur den Anfang dekodieren
- normales Ende mit höchstens 1 Zeichen davor: unverändert ('Eine')
Satzzeichen am Wortende bleiben erhalten.
Ergänzt Spalte 'dekodiert' in data/processed/korpus_absaetze.csv.
Reihenfolge: direkt nach korpus.py ausführen.
"""

from collections import Counter
from pathlib import Path
import re

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
KORPUS = PROJEKT / "data" / "processed" / "korpus_absaetze.csv"
JAHR = 2014

VERSCHIEBBAR = {chr(c) for c in range(0x01, 0x20)} | {chr(c) for c in range(0x21, 0x5F)}
SICHER = {"i": "ä"}
MOEGLICH_UNBEKANNT = {"~", "⁄", "†", "Â", "§", "Ä", "Ö", "Ü", "„", "•"}
KANDIDATEN = ["", "•", "ö", "ü", "ß", "Ä", "Ö", "Ü", "-", "–"]
SAAT = re.compile(r"ß[\x01-\x1f!-^]")
NORMALES_ENDE = re.compile(r"[a-zäöü]*[a-hj-zäöü][a-zäöü]*$")
ENDZEICHEN = ".,;:!?)"


def faehig(token):
    return bool(token) and all(
        c in VERSCHIEBBAR or c in SICHER or c == "ß" or c in MOEGLICH_UNBEKANNT
        for c in token)


def markiere(text):
    teile = re.split(r"(\s+)", text)  # gerade Indizes: Wörter, ungerade: Leerraum
    markiert = {k for k in range(0, len(teile), 2) if SAAT.search(teile[k])}
    geaendert = True
    while geaendert:
        geaendert = False
        for k in list(markiert):
            for n in (k - 2, k + 2):
                if 0 <= n < len(teile) and n not in markiert and faehig(teile[n]):
                    markiert.add(n)
                    geaendert = True
    return teile, markiert


def zerlege(stueck):
    """Liefert (zu dekodierender Anfang, unveränderter Rest)."""
    treffer = NORMALES_ENDE.search(stueck)
    if not treffer:
        return stueck, ""
    anfang, rest = stueck[:treffer.start()], stueck[treffer.start():]
    if len(anfang) >= 2:
        return anfang, rest
    return "", stueck


def dekodiere_teil(teil, unbekannt):
    zeichen = []
    for c in teil:
        if c in SICHER:
            zeichen.append(SICHER[c])
        elif c in unbekannt:
            zeichen.append(unbekannt[c])
        elif 0x01 <= ord(c) <= 0x5E:
            zeichen.append(chr(ord(c) + 0x20))
        else:
            zeichen.append(c)
    return "".join(zeichen)


def teile_des_tokens(token):
    ende = ""
    if len(token) > 1 and token[-1] in ENDZEICHEN:
        token, ende = token[:-1], token[-1]
    return [zerlege(s) for s in token.split("ß")], ende


def dekodiere_token(token, unbekannt):
    stuecke, ende = teile_des_tokens(token)
    return " ".join(dekodiere_teil(a, unbekannt) + r for a, r in stuecke) + ende


def dekodiere_text(text, unbekannt):
    teile, markiert = markiere(text)
    if not markiert:
        return text, False
    for k in markiert:
        teile[k] = dekodiere_token(teile[k], unbekannt)
    return re.sub(r" {2,}", " ", "".join(teile)).strip(), True


def waehle_zuordnung(anfaenge, unbekannte, wortschatz, vorher):
    zuordnung = {}
    for u in unbekannte:
        betroffen = [a for a in anfaenge if u in a]
        punkte = {}
        for kandidat in KANDIDATEN:
            probe = {**vorher, u: kandidat}
            woerter = [w for a in betroffen
                       for w in re.findall(r"[a-zäöüß]{3,}", dekodiere_teil(a, probe).lower())]
            punkte[kandidat] = sum(1 for w in woerter if w in wortschatz)
        zuordnung[u] = max(KANDIDATEN, key=lambda k: punkte[k])
        zuordnung[u + "_punkte"] = punkte
    return zuordnung


def main():
    korpus = pd.read_csv(KORPUS)
    jahr = korpus["jahr"] == JAHR

    sauber = korpus[jahr & ~korpus["text"].str.contains(SAAT)]
    wortschatz = Counter(w for t in sauber["text"]
                         for w in re.findall(r"[a-zäöüß]{3,}", t.lower()))

    anfaenge = []
    for text in korpus.loc[jahr, "text"]:
        teile, markiert = markiere(text)
        for k in markiert:
            stuecke, _ = teile_des_tokens(teile[k])
            anfaenge += [a for a, _ in stuecke if a]
    unbekannte = sorted({c for a in anfaenge for c in a
                         if c not in VERSCHIEBBAR and c not in SICHER})

    ergebnis = waehle_zuordnung(anfaenge, unbekannte, wortschatz, {})
    erste = {u: ergebnis[u] for u in unbekannte}
    ergebnis = waehle_zuordnung(anfaenge, unbekannte, wortschatz, erste)
    zuordnung = {u: ergebnis[u] for u in unbekannte}

    print("Unbekannte Zeichen und gewählte Zuordnung (zweiter Durchgang):")
    for u in unbekannte:
        anzahl = sum(1 for a in anfaenge if u in a)
        punkte = ergebnis[u + "_punkte"]
        rangfolge = ", ".join(f"{k!r}:{v}" for k, v in
                              sorted(punkte.items(), key=lambda x: -x[1])[:4])
        print(f"  {u!r} ({anzahl} Teilstücke) -> {zuordnung[u]!r}   Treffer: {rangfolge}")

    korpus["dekodiert"] = False
    beispiele, neue_woerter = [], Counter()
    for i in korpus.index[jahr]:
        alt = korpus.at[i, "text"]
        neu, geaendert = dekodiere_text(alt, zuordnung)
        if geaendert:
            korpus.at[i, "text"] = neu
            korpus.at[i, "dekodiert"] = True
            korpus.at[i, "zeichen"] = len(neu)
            korpus.at[i, "ziffernanteil"] = round(sum(c.isdigit() for c in neu) / len(neu), 3)
            beispiele.append((korpus.at[i, "seite"], alt, neu))
            teile, markiert = markiere(alt)
            for k in markiert:
                for w in re.findall(r"[a-zäöüß]{3,}", dekodiere_token(teile[k], zuordnung).lower()):
                    if w not in wortschatz:
                        neue_woerter[w] += 1

    print(f"\nDekodierte Einheiten: {len(beispiele)}")
    for seite, alt, neu in beispiele[:5]:
        stelle = max(SAAT.search(alt).start() - 40, 0)
        print(f"\n  S.{seite} vorher:  {alt[stelle:stelle + 160]}")
        print(f"  S.{seite} nachher: {neu[stelle:stelle + 160]}")

    print("\nDekodierte Wörter, die im Wortschatz 2014 fehlen (häufigste 30):")
    print("  " + ", ".join(f"{w} ({n})" for w, n in neue_woerter.most_common(30)))

    rest = korpus.loc[jahr, "text"].str.count(SAAT).sum()
    print(f"\nVerbliebene Ausgangspunkte nach der Dekodierung: {rest}")
    korpus.to_csv(KORPUS, index=False, encoding="utf-8-sig")
    print(f"Gespeichert: {KORPUS}")


if __name__ == "__main__":
    main()