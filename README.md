# Arduino · Design & Technik

Lokaler Nachbau von https://sites.google.com/view/arduino-einfuehrung/home, Stand 9. September 2026.

## Starten

Doppelklick auf **Starten.command**, dann **http://127.0.0.1:5173/** im Browser öffnen. Python 3 wird benötigt, weitere Pakete sind für die fertige Seite nicht nötig. Zum Beenden im Terminal Ctrl+C drücken.

Alternativ im Projektordner:

```sh
python3 serve.py
```

Falls der Port bereits belegt ist:

```sh
python3 serve.py --port 5174
```

Die fertige Website liegt unter `dist/client`. Sie benötigt einen lokalen HTTP-Server; `index.html` nicht direkt als Datei öffnen. Navigation, Suche, Bilder, Schriften und Code-Kopierbuttons funktionieren ohne Internet. Verlinkte externe Seiten und die zwei SWITCHtube-Videos benötigen Internet. Videos werden erst nach einem Klick geladen.

## Inhalt und Gestaltung

Alle 13 Seiten, 29 Originalbilder und 30 Codeblöcke sind übernommen. Die linke Navigation, weisse Gestaltung, Typografie, Seitenreihenfolge und aufklappbaren Abschnitte folgen der Vorlage. Ergänzt wurden Kopierbuttons; notwendige inhaltliche und sprachliche Korrekturen sind in `AENDERUNGEN.md` dokumentiert.

HTML, CSS und Bedienlogik wurden neu implementiert. Der Nachbau verwendet keine Google-Sites-Skripte, Google-Sites-Stylesheets, Google-Logos oder Google-Analysefunktionen. Bilder und Texte wurden auf ausdrücklichen Wunsch des Seiteninhabers übernommen. Die lokale Lato-Schrift wird mit ihrer OFL-Lizenz unter `public/fonts/OFL.txt` ausgeliefert.

## Markierte Lernhilfen

Die 22 neuen Lernhilfen sind auf der Seite mit «Didaktische Ergänzung», Nummer und gelbem Hintergrund markiert. Eine Übersicht mit direkten Sprunglinks steht in `DIDAKTISCHE-ERGAENZUNGEN.md`. Die ursprünglichen Inhalte wurden bei dieser Ergänzung nicht verändert. Die neue Breadboard-Grafik ergänzt die 29 Originalbilder.

## Bearbeiten

- `app/content.json`: Seitentexte, Aufgaben, Codebeispiele und Bildverweise.
- `app/site.tsx`: Navigation, Abschnitte, Suche und Kopierbuttons.
- `app/globals.css`: Gestaltung.
- `public/assets`: Originalbilder.

Für die Weiterentwicklung wird Node.js ab 22.13 benötigt:

```sh
npm install
npm run dev -- --port 5173
```

Nach Änderungen die fertige lokale Version neu erzeugen:

```sh
npm run build
```

Prüfungen: TypeScript, Lint des Anwendungscodes, vollständiger Produktionsbuild sowie Ressourcen- und Linkprüfung. Die Arduino-Beispiele wurden auf erkennbare Syntax- und Inhaltsfehler geprüft, nicht auf realer Hardware ausgeführt. Hardwareabhängige Angaben sind dort erläutert, wo sie für den Aufbau erforderlich sind.
