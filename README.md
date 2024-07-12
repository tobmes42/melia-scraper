# Meliá Hotel Buchungsanfrage Scraper

Dieses Python-Skript ermöglicht es, Buchungsanfragen für das Meliá Frankfurt City Hotel über die offizielle Website von Meliá zu automatisieren. Es verwendet Selenium für die Webseiten-Interaktion und BeautifulSoup für das Parsen des HTML-Codes. Die Ergebnisse werden in eine CSV-Datei geschrieben, die die Verfügbarkeit von Zimmertypen für jeden Tag im angegebenen Zeitraum zeigt.

## Funktionalitäten

- Automatisches Besuchen der Meliá Hotel Buchungsseite für den Meliá Frankfurt City Standort.
- Scrapen der verfügbaren Zimmerkategorien (Melia Zimmer, Junior Suite, The Level Zimmer) für jeden Tag im angegebenen Zeitraum.
- Speichern der Ergebnisse in einer CSV-Datei für eine einfache Analyse oder Weiterverarbeitung.

## Installation

### Voraussetzungen

- Python 3.x installiert (https://www.python.org/downloads/)
- Pip installiert (wird normalerweise während der Python-Installation installiert)
- Chrome Browser installiert

### Abhängigkeiten installieren

1. Öffnen Sie die Kommandozeile oder das Terminal.
2. Navigieren Sie zum Verzeichnis des Projekts.

Führen Sie dann den folgenden Befehl aus, um die erforderlichen Python-Bibliotheken zu installieren:

```bash
pip install selenium webdriver-manager beautifulsoup4 pytz
```

### Webdriver für Chrome installieren

Das Skript verwendet Selenium, um den Chrome WebDriver zu steuern. Dieser WebDriver muss installiert werden, damit das Skript auf Ihrem System funktioniert.

1. Führen Sie den folgenden Befehl in der Kommandozeile aus, um den Chrome WebDriver automatisch zu installieren:

```bash
pip install webdriver-manager
```

## Ausführung

### Auf Windows ausführen

1. Öffnen Sie die Kommandozeile.
2. Navigieren Sie zum Verzeichnis, in dem sich die Datei `script.py` befindet.
3. Führen Sie das Skript mit folgendem Befehl aus:

```bash
python script.py -s 2024-10-01 -e 2024-10-05
```

Ersetzen Sie `script.py` durch den tatsächlichen Namen des Python-Skripts, falls er anders ist. Dieser Befehl startet das Skript und scraped die Daten für den Zeitraum vom 1. Oktober 2024 bis zum 5. Oktober 2024. Die Ergebnisse werden in die Datei `buchungsanfragen.csv` geschrieben, die im gleichen Verzeichnis wie das Skript erstellt wird.

### Beispiel-Aufruf

```bash
python script.py -s 2024-10-01 -e 2024-10-05
```

Dieser Befehl ruft das Skript auf, um die Buchungsanfragen für den Zeitraum vom 1. Oktober 2024 bis zum 5. Oktober 2024 zu machen.

---

Speichern Sie diesen Inhalt in einer Datei namens `README.md` oder `README.txt` im gleichen Verzeichnis wie Ihr Python-Skript (`script.py`). Diese README-Datei dient dann als Anleitung für andere Benutzer, die Ihr Skript verwenden möchten.
