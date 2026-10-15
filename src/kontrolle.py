"""Qualitätskontrolle des Korpus.

Pro Jahrgang:
- Anteil Textabsätze mit Kleinbuchstaben am Anfang (nicht verbundene Fortsetzung)
- Anteil Textabsätze ohne Satzzeichen am Ende (abgeschnittener Absatz)
- Randnotizen über 200 Zeichen (möglicherweise falsch zugeordneter Fließtext)
"""

from pathlib import Path

import pandas as pd

PROJEKT = Path(__file__).resolve().parents[1]
KORPUS = PROJEKT / "data" / "processed" / "korpus_absaetze.csv"
SATZENDE = tuple('.!?:;"“”)')
LANGE_RANDNOTIZ = 200

korpus = pd.read_csv(KORPUS)
text = korpus[korpus["typ"] == "text"].copy()
text["klein_anfang"] = text["text"].str[:1].str.islower()
text["ohne_ende"] = ~text["text"].str.rstrip().str.endswith(SATZENDE)
rand = korpus[korpus["typ"] == "randnotiz"]

uebersicht = pd.DataFrame({
    "absaetze": text.groupby("jahr").size(),
    "klein_anfang": text.groupby("jahr")["klein_anfang"].mean().round(3),
    "ohne_ende": text.groupby("jahr")["ohne_ende"].mean().round(3),
    "rand_median": rand.groupby("jahr")["zeichen"].median().astype(int),
    "rand_lang": rand[rand["zeichen"] > LANGE_RANDNOTIZ].groupby("jahr").size(),
    "rand_in_ueb": rand[rand["kapitel"] == "UEB"].groupby("jahr").size(),
}).fillna(0)
print(uebersicht.to_string())


def zeige(df, titel, anzahl, seed, laenge=160):
    print(f"\n{titel} ({len(df)}):")
    for _, z in df.sample(min(anzahl, len(df)), random_state=seed).iterrows():
        print(f"  {z['jahr']} {z['kapitel']} S.{z['seite']}: {z['text'][:laenge]}")


zeige(text[text["klein_anfang"]], "Beginnt mit Kleinbuchstaben", 5, 1)
zeige(text[text["ohne_ende"]], "Endet ohne Satzzeichen (Ende des Absatzes)", 5, 2)
ohne_ende = text[text["ohne_ende"]].copy()
ohne_ende["text"] = "... " + ohne_ende["text"].str[-120:]
zeige(ohne_ende, "Endet ohne Satzzeichen (letzte 120 Zeichen)", 5, 2)
zeige(rand[rand["zeichen"] > LANGE_RANDNOTIZ], "Lange Randnotizen", 5, 3, 200)

print("\nKontrollfall 2014, 'diesen Konstellationen':")
fall = text[(text["jahr"] == 2014) & text["text"].str.contains("diesen Konstellationen")]
for _, z in fall.iterrows():
    stelle = z["text"].find("diesen Konstellationen")
    print(f"  S.{z['seite']}: ...{z['text'][max(stelle - 150, 0):stelle + 80]}...")