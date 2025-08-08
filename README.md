# Scrape and Analyse

Minimalistische App, um im Internet nach Startups zu suchen und Basisinformationen auszulesen.

## Projektstruktur

```
Scrape-and-analyse/
├── data/            # Ablage für gespeicherte Rohdaten
├── src/             # Flask-Anwendung und Hilfsfunktionen
│   └── app.py
├── static/          # CSS-Dateien
│   └── style.css
├── templates/       # HTML-Templates für die Weboberfläche
│   ├── index.html
│   └── results.html
├── tests/           # Automatische Tests
│   └── test_app.py
├── requirements.txt # Benötigte Python-Pakete
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Nutzung

```bash
python src/app.py
```

Öffne danach [http://localhost:5000](http://localhost:5000) im Browser und gib einen Suchbegriff ein.

## Tests

```bash
pytest
```

Die Ergebnisse stammen aus öffentlichen Webseiten und können unvollständig sein.
