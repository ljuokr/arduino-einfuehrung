# Arduino · Design & Technik

Lokale Single-File-Version von https://sites.google.com/view/arduino-einfuehrung/home für den begleiteten Workshop mit Lehrpersonen. Stand: 21. September 2026.

## Verwenden

Doppelklick auf **arduino.html**. Kein Server, kein Node, kein Internet nötig. Alle 13 Seiten, 29 Bilder, 30 Codebeispiele mit Kopierbutton, Suche und Schriften stecken in der einen Datei (rund 2 MB). Nur die zwei SWITCHtube-Videos laden auf Klick von extern.

## Bearbeiten

- `content.json`: sämtliche Inhalte (Texte, Aufgaben, Codebeispiele, Bildverweise).
- `style.css`: Gestaltung.
- `build.py`: erzeugt `arduino.html` neu. Bettet Bilder als WebP und die Lato-Schrift reduziert auf die benutzten Zeichen ein.
- `assets/`, `fonts/`: Originalbilder und Schriften (Lato unter OFL-Lizenz, siehe `fonts/OFL.txt`).

Nach Änderungen neu bauen (benötigt Python 3 mit Pillow und fontTools):

```sh
python3 build.py
```

## Inhalt

Alle Inhalte der Vorlage sind übernommen. Fachliche und sprachliche Korrekturen sind in `AENDERUNGEN.md` dokumentiert. Bilder und Texte wurden auf ausdrücklichen Wunsch des Seiteninhabers übernommen, die Website selbst ist eine Neuimplementierung ohne Google-Skripte oder Google-Analysefunktionen.
