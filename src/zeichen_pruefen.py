"""Sonderzeichen und Zeilenenden in den ausgeschnittenen Abschnitten prüfen."""

from collections import Counter
from pathlib import Path
import unicodedata

ORDNER = Path(__file__).resolve().parents[1] / "data" / "interim" / "abschnitte"
UMLAUTE = set("äöüÄÖÜß")

for datei in sorted(ORDNER.glob("*.txt")):
    text = datei.read_text(encoding="utf-8")
    zaehler = Counter(c for c in text if ord(c) > 127 and c not in UMLAUTE)
    print(f"--- {datei.stem[-4:]} ---")
    for c, n in zaehler.most_common(10):
        print(f"  U+{ord(c):04X}  {unicodedata.name(c, 'ohne Namen'):<40} {n}")
    zeilen = [z for z in text.splitlines() if z.strip()]
    print("  Zeilenenden:", "  ".join(ascii(z[-4:]) for z in zeilen[5:13]))