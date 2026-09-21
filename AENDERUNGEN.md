# Korrekturen gegenüber der Vorlage

Stand: 9. September 2026. Seitenstruktur, Aufgaben und Bilder bleiben erhalten.

- **Home:** Arduino als Plattform aus Boards und Software beschrieben; vom Mikrocontroller auf dem Board unterschieden. [Arduino](https://www.arduino.cc/en/Main/AboutUs)
- **Arduino einrichten:** Board und Port als Verbindungskriterium erklärt. Die frühere Unterscheidung nach Fettdruck ersetzt. [Board und Port wählen](https://support.arduino.cc/hc/en-us/articles/4406856349970-Select-board-and-port-in-Arduino-IDE)
- **LED-Schaltungen:** Vorwiderstände auch für kurze Versuche vorgeschrieben; LED-Anschlussbeschreibungen angepasst. Die Original-Schaltungsbilder bleiben unverändert; bei den betroffenen Aufgaben steht ausdrücklich, dass ein im Bild fehlender Widerstand ergänzt werden muss. [Arduino Blink](https://docs.arduino.cc/built-in-examples/basics/Blink/)
- **FET-Aufgabe:** Für die Erweiterung zum Dimmen PWM-Pin 6 statt A0 gewählt. Den Austausch von `LED_BUILTIN` im Beispielcode konkret benannt. [Arduino PWM](https://support.arduino.cc/hc/en-us/articles/9350537961500-Use-PWM-output-with-Arduino)
- **OLED:** `display.setTextWrap(false)` ergänzt, damit die bewegte Grafik am Rand abgeschnitten wird und nicht in die nächste Zeile umbricht. Versorgungsspannung vom verwendeten Displaymodul abhängig gemacht. [Adafruit GFX](https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives)
- **Programmierung:** `LED_BUILTIN` boardabhängig erklärt; die wiederholte Auswertung von `if` präzisiert; fehlerhaften Kommentar vor einer schliessenden Klammer korrigiert. Die Strukturbeispiele behalten echte Zeilenumbrüche. Die Aussage über `delay()` präzisiert. [Arduino Blink](https://docs.arduino.cc/built-in-examples/basics/Blink/), [if-Referenz](https://github.com/arduino/reference-en/blob/master/Language/Structure/Control%20Structure/if.adoc), [delay-Referenz](https://github.com/arduino/reference-en/blob/master/Language/Functions/Time/delay.adoc)
- **Sensoren / Joystick:** PWM als zeitliches Ein- und Ausschalten erklärt, nicht als frei einstellbare Gleichspannung. [analogWrite](https://docs.arduino.cc/language-reference/en/functions/analog-io/analogWrite/)
- **Ultraschall:** Timeout ergänzt; ein fehlendes Echo schaltet die LED aus, statt als Abstand null interpretiert zu werden. [pulseIn](https://docs.arduino.cc/language-reference/en/functions/advanced-io/pulseIn/)
- **Servo / Schrittmotor:** Modellabhängige Bewegungsbereiche und Impulsgrenzen benannt. Versorgung des Servos vom tatsächlichen Strombedarf abhängig gemacht. Das Schrittmotorbeispiel auf den abgebildeten Typ 28BYJ-48 mit ULN2003 angepasst: ungefähr 2048 Vollschritte statt 200, Konstruktor-Pinreihenfolge 8/10/9/11 und ungefähr 6 statt 60 U/min. Motorvariante, Getriebeabweichungen und externe Versorgung ausdrücklich beschrieben. [Servo](https://github.com/arduino-libraries/Servo/blob/master/docs/api.md), [28BYJ-48 / ULN2003](https://www.seeedstudio.com/blog/2019/03/04/driving-a-28byj-48-stepper-motor-with-a-uln2003-driver-board-and-arduino/)
- **Smart Textiles:** Waschbarkeit von geeigneten LilyPad-Projekten mit Batterieentnahme und vollständigem Trocknen erklärt. Lichtsensor-Kommentare von A0 auf den tatsächlich verwendeten Pin A4 korrigiert. Farbwechsel beim Touch-Sensor auf eine Auslösung pro neuer Berührung umgestellt. [SparkFun LilyPad](https://learn.sparkfun.com/tutorials/lilypad-development-board-hookup-guide/technical-notes), [Arduino Flankenerkennung](https://docs.arduino.cc/built-in-examples/digital/StateChangeDetection/)
- **Fehlersuche:** Weitere mögliche Ursachen eines fehlenden Ports berücksichtigt; Syntaxprüfung beim Kompilieren erläutert. [Arduino-Verbindungsprüfung](https://support.arduino.cc/hc/en-us/articles/4412955149586-If-your-board-is-not-detected-by-Arduino-IDE)
- **Redaktionell:** Tippfehler wie „Piezzo“, „Variabeln“ und „einzlene“ korrigiert, Schweizer Schreibweise vereinheitlicht und einen defekten Sprunglink repariert.

## Didaktische Ergänzungen

Zwischenzeitlich waren 22 markierte Lernhilfen ergänzt. Da der Workshop begleitet stattfindet und die Zielgruppe Lehrpersonen ohne Vorkenntnisse sind, wurden sie am 20. September 2026 auf zwei Hardware-Infokästen reduziert: Breadboard-Kontaktgruppen (mit neuer Grafik) und LED-Stromkreis mit Vorwiderstand, beide am Ende der Seite Verbindungen. Die übrigen Selbstlern-Aufträge übernimmt die Kursleitung mündlich.

## Nachträgliche Textprüfung (20. September 2026)

Vollständiger Wort-für-Wort-Durchgang mit rund 90 Korrekturen: restliche „ß" auf Schweizer Schreibweise, Anführungszeichen einheitlich «…», Grammatik- und Tippfehler (u. a. „under", „GND der Arduinos"), Durchkopplungen, NeoPixel-Schreibweise, beschreibende Alt-Texte für alle Galeriebilder. Alle 30 Codeblöcke einheitlich formatiert (2 Leerzeichen, bündige Kommentare) und die Kommentare für die Zielgruppe redigiert.

## Lokale Umsetzung

Die Website ist eine einzelne Datei `arduino.html`, erzeugt aus `content.json` per `build.py`. 30 Codeblöcke mit Kopierbuttons als „Codeausschnitt". Kopiert wird der reine Programmtext ohne Überschrift oder Buttontext. 29 Bilder (als WebP) und die Lato-Schrift sind eingebettet. Die Seitensuche ist als lokale Inhaltssuche implementiert. Originalvideos bleiben per Klick eingebettet. Aufklappbare Aufgaben als Karten mit runden Ecken statt der Google-Sites-Trennlinien.

Keine Veröffentlichung und keine Änderung an der bestehenden Google-Sites-Seite.

## Ergänzende fachliche Prüfung

- Den fehlenden LED-Vorwiderstand auch beim Smart-Textiles-Foto ausdrücklich benannt und die Erweiterungsaufgabe in Tinkercad ergänzt. Die Originalbilder bleiben erhalten und sind dort ohne diese Ergänzung keine vollständige Aufbauanleitung.
- Die OLED-Voraussetzungen konkretisiert: SSD1306, I²C, 128 × 32 Pixel, Adresse 0x3C, kein separat angesteuerter Reset. [Adafruit](https://learn.adafruit.com/monochrome-oled-breakouts/arduino-library-and-examples)
- Texte, vollständige Codebeispiele und relevante Schaltungsbilder nochmals miteinander abgeglichen. Unvollständige Ergänzungsaufgaben sind absichtlich keine eigenständig lauffähigen Programme.

Die Prüfung umfasst eine Quellen-, Text- und Codeprüfung. Die Arduino-Beispiele wurden nicht mit den tatsächlichen Boards und Bauteilen kompiliert oder auf Hardware ausgeführt. Die Funktionsprüfung der Website ist davon getrennt. Eine vollständige praktische Freigabe für den Unterricht setzt einen Test mit dem konkret verwendeten Material voraus.

## Korrektur der Bedienung

- Die Navigation verwendet direkte lokale Links. Damit hängt der Seitenwechsel nicht vom fehlerhaften Client-Router des statischen Exports ab.
- Das mobile Menü zeigt alle Links mit ausreichendem Abstand untereinander.
- Der Kopierbutton verwendet zuerst das synchrone Kopieren innerhalb des Klicks und zeigt die Erfolgsrückmeldung «Kopiert!».
- Navigation, Aufklappen und Suche mit Sprung zum passenden Abschnitt wurden im eingebauten Browser durchgeklickt.
