# Bildung in Deutschland 2006 bis 2026: Was 20 Jahre Bildungsbericht sagen

**20 Jahre Bildungsbericht in drei Befunden:** Der Bericht beschreibt fast nur, seine Themen wandern von Strukturen zu Lebenslagen, und fünf Herausforderungen kehren seit 2006 immer wieder.

<p align="center">
  <img src="figures/social/folie_2.png" width="49%" alt="Befund 1: Handlungsbedarf steht vor allem außerhalb der Kernkapitel">
  <img src="figures/social/folie_3.png" width="49%" alt="Befund 2: Die Themen verschieben sich von Strukturen zu Lebenslagen">
</p>
<p align="center">
  <img src="figures/social/folie_4.png" width="49%" alt="Befund 3: Fünf Herausforderungen kehren über 20 Jahre wieder">
  <img src="figures/social/folie_5.png" width="49%" alt="Drei Anregungen für den nächsten Bildungsbericht">
</p>

<sub>Alle Folien als PDF: [figures/social/bildungsbericht_karussell.pdf](figures/social/bildungsbericht_karussell.pdf)</sub>

Diese Analyse wertet die elf nationalen Bildungsberichte "Bildung in Deutschland" (2006 bis 2026) als Textdaten aus. Sie fragt, welche Themen der Bericht über 20 Jahre setzt, wie stark er beschreibt, bewertet oder Handlungsbedarf benennt und zu welchen Themen er wiederholt Handlungsbedarf sieht. Im Mittelpunkt stehen Inhalte, nicht Formulierungen oder Stil.

## Auf einen Blick

- **Der Bericht beschreibt.** Rund 89 Prozent der Sätze beschreiben, je rund 5 Prozent bewerten oder benennen Handlungsbedarf. Daran ändert sich in 20 Jahren wenig.
- **Handlungsbedarf steht vor allem im Überblick, in der Einleitung und im Schwerpunktkapitel.** In den Kernkapiteln¹ liegt sein Anteil stabil bei 3,5 bis 5,1 Prozent, im Überblick zeitweise bei 12 bis 13 Prozent.
- **Die Themen verschieben sich von Strukturen zu Lebenslagen.** Zuwanderung, Familie und soziale Risikolagen, frühe Bildung, Digitalisierung sowie Programme und Qualitätssicherung gewinnen an Gewicht. Internationaler Vergleich, demografischer Wandel, Schularten und Ausbildungsberufe verlieren.
- **Fünf Herausforderungen kehren belastbar wieder:** Steuerung des Bildungssystems, demografischer und wirtschaftlicher Wandel, pädagogisches Personal, soziale Herkunft und Ungleichheit sowie Lehrkräfte.

<sub>¹ Kernkapitel: die Kapitel A bis G und I, die in jedem Bericht dieselben Bildungsbereiche und Indikatoren fortschreiben. Details im Abschnitt "Kapitelgruppen".</sub>

## Fragen

1. Welche Themen bleiben über 20 Jahre konstant, welche kommen hinzu, welche gehen zurück?
2. Welche Herausforderungen benennt der Bericht wiederholt, und wie entwickeln sich die zugehörigen Indikatoren im selben Zeitraum?
3. Wie verteilen sich Beschreibung, Bewertung und Handlungsbedarf im Text?

Frage 1, Frage 3 und der erste Teil von Frage 2 sind beantwortet. Der Abgleich mit den Indikatoren folgt.

## Datengrundlage

Grundlage sind die elf Vollberichte von der Einleitung bis vor das Literaturverzeichnis, ohne Tabellen und Abbildungen. Daraus entstehen 9.188 Textabsätze (9.125 im Topic Model) und 41.314 Sätze mit mindestens fünf Wörtern. Die Berichte sind auf [bildungsbericht.de](https://www.bildungsbericht.de) frei verfügbar. Dieses Repository enthält keine Texte aus den Berichten, nur eigene Auswertungen.

## Vorgehen

| Schritt | Verfahren | Frage |
|---|---|---|
| Themen finden | Structural Topic Model mit 40 Themen, Absatz als Einheit, Jahr und Kapitel als Kovariaten | 1 |
| Themen vergleichen | Anteil je Thema in den Berichten 2006 bis 2010 und 2022 bis 2026, geprüft mit Modellen mit 30 und 60 Themen | 1 |
| Sätze einordnen | Wörterbuch mit Signalwörtern: Beschreibung, Bewertung, Handlungsbedarf | 3 |
| Herausforderungen finden | Themen, zu denen in mindestens 6 der 11 Berichte überdurchschnittlich oft Handlungsbedarf steht | 2 |
| Robustheit | strenge Wortliste ohne Modalverben, Zählung nur in Kernkapiteln, Modell ohne Signalwörter | 2, 3 |

### Kapitelgruppen

Jeder Bericht hat einen festen und einen wechselnden Teil. Die Analyse trennt sie, weil der wechselnde Teil die Jahreswerte verzerrt: Ein Thema kann in einem Jahr stark steigen, nur weil das Schwerpunktkapitel davon handelt.

| Gruppe | Kapitel | Inhalt |
|---|---|---|
| Kernkapitel | A Rahmenbedingungen, B Grundinformationen, C Frühe Bildung, D Allgemeinbildende Schule, E Berufliche Ausbildung, F Hochschule, G Weiterbildung, I Wirkungen und Erträge | schreiben in jedem Bericht dieselben Indikatoren fort |
| Schwerpunktkapitel | H | wechselt das Thema mit jedem Bericht, 2010 etwa demografischer Wandel, 2026 soziale Herkunft |
| Überblick | Wichtige Ergebnisse im Überblick | fasst zusammen, 2026 erstmals mit "Zentralen Herausforderungen" |
| Einleitung | Einleitung | führt in den Bericht ein |

"Kernkapitel" ist ein Arbeitsbegriff dieser Analyse, kein Begriff der Berichte. 2018 fehlt Kapitel I, weil das Schwerpunktkapitel H selbst Wirkungen und Erträge behandelt.

## Ergebnisse

### Frage 1: Welche Themen bleiben, kommen hinzu, gehen zurück?

![Abbildung 6](figures/abb6_muster_kernkapitel.png)

<sub>Nur Kernkapitel A bis G und I. Grauer Punkt: Durchschnitt der Berichte 2006 bis 2010, farbiger Punkt: 2022 bis 2026.</sub>

- Von 32 inhaltlichen Themen kommen in den Kernkapiteln 8 hinzu, 8 gehen zurück, 7 bleiben konstant, 4 verschieben sich leicht und 5 verändern sich uneinheitlich.
- Am stärksten wachsen Zuwanderung und Integration (0,3 auf 2,8 Prozent) sowie Familie und soziale Risikolagen (2,5 auf 5,5 Prozent).
- Am stärksten sinken internationaler Vergleich (5,2 auf 2,3 Prozent) und demografischer Wandel (4,5 auf 1,9 Prozent).
- Soziale Herkunft bleibt in den Kernkapiteln auf gleichem Niveau (2,6 und 2,8 Prozent). Die Spitzen 2006 und 2026 stammen aus den Schwerpunktkapiteln.
- In allen vergleichbaren Modellen mit 30, 40 und 60 Themen bleibt die Richtung gleich: Es steigen Digitalisierung, Programme und Qualitätssicherung, Familie und soziale Risikolagen, Zuwanderung, frühe Bildung, Ganztag und Lehrkräfte. Es sinken internationaler Vergleich, demografischer Wandel, Schularten, Ausbildungsberufe, Betriebe in Aus- und Weiterbildung, Erträge und kulturelle Bildung, regionale Unterschiede sowie Studienberechtigung und Hochschulabschluss.

![Abbildung 5](figures/abb5_herkunft_kapitel.png)

<sub>Kernkapitel: A bis G und I. Schwerpunkt H: wechselndes Thema je Bericht.</sub>

Der starke Anstieg von Steuerung des Bildungssystems 2026 (8,6 Prozent) stammt vor allem aus dem Überblick (rund 4,9 Prozentpunkte). In den Kernkapiteln steigt das Thema nur wenig, und die Vergleichsmodelle bestätigen diesen Anstieg nicht.

### Frage 3: Beschreibung, Bewertung, Handlungsbedarf

![Abbildung 7](figures/abb7_kategorien_jahr.png)

Der Anteil der beschreibenden Sätze liegt in allen Berichten bei rund 87 bis 91 Prozent. Bewertung (4,7 bis 7,8 Prozent) und Handlungsbedarf (4,1 bis 7,2 Prozent) zeigen keinen Trend.

![Abbildung 8](figures/abb8_kategorien_kapitelgruppe.png)

<sub>Kernkapitel: A bis G und I. Die Einleitung fehlt, weil sie je Bericht nur 12 bis 34 Absätze umfasst.</sub>

Die Kapitelgruppen unterscheiden sich deutlich. In den Kernkapiteln bleibt der Anteil an Handlungsbedarf bei 3,5 bis 5,1 Prozent. Im Überblick erreicht er 2012 bis 2018 rund 12 bis 13 Prozent, im Schwerpunktkapitel 2010 (demografischer Wandel) 16,3 Prozent.

### Frage 2: Welche Herausforderungen kehren wieder?

![Abbildung 10](figures/abb10_handlungsbedarf_themen.png)

<sub>Zahl der Sätze mit Handlungsbedarf je Thema und Bericht, alle Kapitel. Oberer Block: wiederkehrend nach der Hauptregel.</sub>

Ein Thema gilt als wiederkehrend, wenn der Bericht dazu in mindestens 6 der 11 Berichte mindestens 3 Sätze mit Handlungsbedarf schreibt und dieser Anteil über dem des ganzen Berichts liegt. Nach den Robustheitsprüfungen ergeben sich drei Stufen:

| Stufe | Themen |
|---|---|
| belastbar | Steuerung des Bildungssystems, demografischer und wirtschaftlicher Wandel, pädagogisches Personal, soziale Herkunft und Ungleichheit, Lehrkräfte |
| mit Einschränkung | Kindertagesbetreuung (hängt an Modalverben wie "müssen") |
| modellabhängig | Programme und Qualitätssicherung, Ausbildungsmarkt und Übergangssystem, frühe Bildung |

- Steuerung des Bildungssystems hat mit 20 Prozent die höchste Quote: Jeder fünfte Satz zu diesem Thema benennt Handlungsbedarf, in allen 11 Berichten überdurchschnittlich. Auch im Modell ohne Signalwörter bleibt das so (17,4 Prozent). Der Handlungsbedarf steigt von 4 bis 8 Sätzen bis 2012 auf 71 Sätze 2024 und 63 Sätze 2026, steht aber fast nur in Überblick, Einleitung und Schwerpunktkapitel.
- Zum demografischen Wandel benennt der Bericht 2010 noch 50 Sätze mit Handlungsbedarf, 2022 und 2024 je einen.
- Zu Bildungsstand, Studienberechtigung, Bildungsausgaben und internationalem Vergleich benennt der Fließtext kaum Handlungsbedarf (Quote unter 3 Prozent). Was die Tabellen dazu zeigen, ist nicht Teil der Analyse.

## Grenzen und offene Punkte

- **Nur Fließtext.** Tabellen und Abbildungen der Berichte sind nicht ausgewertet. Ein Thema, zu dem der Text wenig sagt, kann in den Tabellen ausführlich dokumentiert sein.
- **Keine Handcodierung.** Die Einordnung beruht auf einem Wörterbuch. Eine Stichprobe von 308 Sätzen für eine Prüfung von Hand ist vorbereitet, aber nicht codiert. Die Robustheitsprüfungen zeigen, welche Befunde stabil sind, nicht ob das Wörterbuch Handlungsbedarf richtig erkennt.
- **Modellabhängigkeit.** 14 der 32 Themen ändern ihre Richtung zwischen den Modellen mit 30, 40 und 60 Themen. Die Ergebnisse oben nennen nur die stabilen Befunde.
- **Selbst gesetzte Schwellen.** Die Regeln für "wiederkehrend" und für die fünf Muster sind festgelegt, nicht aus den Daten abgeleitet. Die Notebooks legen jede Schwelle offen.
- **Sprünge in der Gliederung.** Einige Rückgänge passieren als Sprung zwischen zwei Berichten, etwa Schularten 2022. Sie können auf eine geänderte Gliederung zurückgehen statt auf einen Bedeutungsverlust.
- **Indikatoren fehlen noch.** Ob sich die wiederkehrenden Herausforderungen in den Indikatoren verbessern, zeigt erst der Abgleich mit den Tabellen der Berichte.

## Anregungen für die Berichterstattung

Fünf Anregungen zur Form des Berichts, jede gestützt auf einen klaren Befund. Sie betreffen die Berichterstattung, nicht die Bildungspolitik.

| Nr. | Befund | Anregung |
|---|---|---|
| 1 | Handlungsbedarf steht in den Kernkapiteln in 3,5 bis 5,1 Prozent der Sätze, im Überblick in bis zu 13,2 und in der Einleitung in bis zu 16,3 Prozent. Steuerung ist in allen 11 Berichten eine wiederkehrende Herausforderung, in den Kernkapiteln nur in 3. | Was Überblick und Einleitung als Herausforderung benennen, greift das zugehörige Kernkapitel in einem kurzen, einheitlichen Abschnitt auf. |
| 2 | Fünf Herausforderungen kehren in mindestens 6 der 11 Berichte wieder und bestehen alle Prüfungen: Steuerung, demografischer Wandel, pädagogisches Personal, soziale Herkunft, Lehrkräfte. | Ein festes Register der Herausforderungen: seit wann benannt, an welchem Indikator ablesbar, Entwicklung seit dem letzten Bericht. Das ist der größte Hebel. |
| 3 | Zum demografischen Wandel stehen 2010, im Jahr des Schwerpunkts, 50 Sätze mit Handlungsbedarf, 2022 und 2024 je einer. Zur Digitalisierung 2020, ebenfalls Schwerpunkt, 91, danach 23, 5 und 7. | Spätere Berichte greifen die Herausforderungen früherer Schwerpunkte kurz wieder auf und sagen, was daraus geworden ist. |
| 4 | Einzelne Themen brechen zwischen zwei Berichten ein: Ausbildungsberufe 2018 (4,8 auf 1,6 Prozent), Schularten 2022 (4,6 auf 2,0 Prozent). 2018 fehlt Kapitel I. | Eine Übersicht über alle Berichte, welcher Indikator wann hinzukam, wegfiel oder umzog. So lässt sich eine echte Verschiebung von einer Umstellung unterscheiden. |
| 5 | Die Tabellen stehen als Excel-Dateien bereit, der Text nur als PDF. Für diese Analyse musste der Text mit eigenen Skripten gewonnen werden, 2014 aus einer defekt kodierten Schrift. | Neben dem PDF eine strukturierte Textfassung, etwa XML, mit Kapitel, Abschnitt und Verweis auf die zugehörige Tabelle. |

<sub>Die Anregungen 1 bis 3 beruhen auf der Einordnung mit einem Wörterbuch und nutzen nur die robusten Befunde.</sub>

## Inhalt des Repositorys

| Ordner oder Datei | Inhalt |
|---|---|
| `src/` | Python-Skripte: Text aus den PDF-Dateien extrahieren, bereinigen und nach Kapiteln gliedern |
| `r/00_einrichtung.R` | installiert die benötigten R-Pakete |
| `notebooks/01_vorverarbeitung.ipynb` | Lemmatisierung, Vokabular, Dokument-Wort-Matrix |
| `notebooks/02_stm_modell.ipynb` | Structural Topic Model mit 40 Themen, Frage 1, Abbildungen 1 bis 6 |
| `notebooks/03_bewertung_handlungsbedarf.ipynb` | Einordnung der Sätze, Robustheit, Gegenprobe ohne Signalwörter, Frage 3 und erster Teil von Frage 2, Abbildungen 7 bis 11 |
| `data/processed/` | Ergebnisse als Tabellen: Themen, Muster, Robustheit, Handlungsbedarf je Thema und Bericht |
| `figures/` | alle Abbildungen |

Jedes Notebook erklärt jeden Schritt vor dem Code, hält nach jeder Ausgabe den Befund fest und endet mit einer Zusammenfassung der Entscheidungen, Befunde und Grenzen.

## Daten und Reproduktion

Das Repository enthält keine Texte aus den Berichten. Wer die Analyse wiederholen will, lädt die elf Vollberichte von [bildungsbericht.de](https://www.bildungsbericht.de) herunter und legt sie als `2006.pdf` bis `2026.pdf` unter `data/raw/berichte/` ab.

Nicht veröffentlicht werden alle Zwischenstände, die Text enthalten: das Korpus (`data/processed/korpus_absaetze.csv`), die Abschnitte "Zentrale Herausforderungen" (`data/processed/abschnitte/`, `segmente_zentrale_herausforderungen.csv`), die Lemmatisierung, die Sätze mit ihrer Einordnung, die Stichprobe für die Handcodierung und die typischen Absätze je Thema. Die Notebooks geben keine Sätze aus den Berichten aus.

Ablauf:

1. Python-Pipeline in `src/` ausführen. Sie erzeugt `data/processed/korpus_absaetze.csv`.
2. `r/00_einrichtung.R` ausführen.
3. Die Notebooks in der Reihenfolge 01, 02, 03 ausführen.

Die Schätzungen in `02_stm_modell.ipynb` dauern beim ersten Lauf rund 90 Minuten, die Gegenprobe in `03_bewertung_handlungsbedarf.ipynb` einige Minuten. Die Ergebnisse speichern die Notebooks unter `data/interim/` und laden sie bei jedem weiteren Lauf.

Das Sprachmodell `german-gsd` für die Lemmatisierung (udpipe) steht unter der Lizenz CC BY-NC-SA. Es wird beim ersten Lauf von `01_vorverarbeitung.ipynb` heruntergeladen und ist nicht Teil des Repositorys.

## Software

- Python 3.14 für die Textextraktion
- R 4.6.1 mit `udpipe`, `quanteda`, `stm`, `dplyr`, `tidyr`, `ggplot2`, `readxl` und `writexl`
- Jupyter-Notebooks mit R-Kernel

## Quellen

- Konsortium Bildungsberichterstattung (2006). Bildung in Deutschland. Ein indikatorengestützter Bericht mit einer Analyse zu Bildung und Migration. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2008). Bildung in Deutschland 2008. Ein indikatorengestützter Bericht mit einer Analyse zu Übergängen im Anschluss an den Sekundarbereich I. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2010). Bildung in Deutschland 2010. Ein indikatorengestützter Bericht mit einer Analyse zu Perspektiven des Bildungswesens im demografischen Wandel. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2012). Bildung in Deutschland 2012. Ein indikatorengestützter Bericht mit einer Analyse zur kulturellen Bildung im Lebenslauf. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2014). Bildung in Deutschland 2014. Ein indikatorengestützter Bericht mit einer Analyse zur Bildung von Menschen mit Behinderungen. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2016). Bildung in Deutschland 2016. Ein indikatorengestützter Bericht mit einer Analyse zu Bildung und Migration. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2018). Bildung in Deutschland 2018. Ein indikatorengestützter Bericht mit einer Analyse zu Wirkungen und Erträgen von Bildung. Bielefeld: W. Bertelsmann.
- Autorengruppe Bildungsberichterstattung (2020). Bildung in Deutschland 2020. Ein indikatorengestützter Bericht mit einer Analyse zu Bildung in einer digitalisierten Welt. Bielefeld: W. Bertelsmann.
- Autor:innengruppe Bildungsberichterstattung (2022). Bildung in Deutschland 2022. Ein indikatorengestützter Bericht mit einer Analyse zum Bildungspersonal. Bielefeld: wbv Publikation.
- Autor:innengruppe Bildungsberichterstattung (2024). Bildung in Deutschland 2024. Ein indikatorengestützter Bericht mit einer Analyse zu beruflicher Bildung. Bielefeld: wbv Publikation.
- Autor:innengruppe Bildungsberichterstattung (2026). Bildung in Deutschland 2026. Ein indikatorengestützter Bericht mit einer Analyse zu Bildungsungleichheiten nach sozialer Herkunft. Bielefeld: wbv Publikation.

Der Bericht 2026 steht mit Ausnahme der Umschlagfotos unter der Lizenz Creative Commons Namensnennung, Weitergabe unter gleichen Bedingungen 4.0 International (CC BY-SA 4.0). Für die übrigen Berichte gelten die Angaben im jeweiligen Impressum. Dieses Repository enthält keine Texte, Tabellen oder Abbildungen aus den Berichten, sondern nur eigene Auswertungen.

## Dank

Ich danke dem DIPF | Leibniz-Institut für Bildungsforschung und Bildungsinformation, das die nationale Bildungsberichterstattung koordiniert, sowie der Autor:innengruppe Bildungsberichterstattung. Ihre Arbeit über 20 Jahre und die freie Bereitstellung der Berichte haben diese Analyse erst möglich gemacht.

Die Auswertungen und ihre Deutung liegen allein in meiner Verantwortung. Sie geben nicht die Position des DIPF oder der Autor:innengruppe wieder.

## Lizenz

- Code (`src/`, `r/`, `notebooks/`): MIT-Lizenz, siehe `LICENSE`.
- Ergebnisse (`data/processed/`, `figures/`): Creative Commons Namensnennung 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/deed.de

Die Lizenzen gelten nur für die eigene Analyse. Die Bildungsberichte selbst sind nicht Teil des Repositorys, ihre Nutzungsbedingungen bleiben unberührt.

## Stand

Frage 1, Frage 3 und der erste Teil von Frage 2 sind beantwortet. Die Ergebnisse zu Frage 2 und 3 beruhen auf einem Wörterbuch, sind auf Robustheit geprüft und nicht an einer Handcodierung validiert. Der Abgleich mit den Indikatoren (zweiter Teil von Frage 2) folgt.
