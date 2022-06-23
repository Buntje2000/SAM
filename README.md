# SAM - Smart Anonymizer for Metadata (and Images)

## Setup

Als je nog niet met Python hebt gewerkt, moet je eerst Python installeren. Dat doe je als volgt. Installeer eerst Choco package manager.
Daarna voer je als administrator het volgende commando uit:

```bash
choco install python --pre
```

Eerst moet je een virtual environment aanmaken. Daarvoor voer je de volgende commando's uit in de project map.

```bash
py -m pip install --user virtualenv

py -m venv venv
```

Nu heb je een virtuele omgeving aangemaakt. Vervolgens moet je deze 'venv' activeren. Roep hiervoor het volgende commando aan.

```bash
venv\Scripts\activate
```

Nu de virtuele omgeving is geactiveerd, kunnen we de benodigde packages gaan installeren.
Dat doe je door het volgende commando aan te roepen.

```bash
pip install -r requirements.txt
```

Pip is de package manager van Python. Deze zal nu de benodigde packages installeren.

Om de Pixel-search & Pixel-clean pipelines te draaien moet Tesseract OCR geïnstalleerd zijn op het systeem.

## Run

Om een pipeline via de terminal te draaien,
voer je het volgende commando uit:

```bash
python run.py -a [m/ps/pc] -i [filename.dcm] -s [search keyword] -p [low/medium/high] -r [replacement value]
```

De pipeline wordt nu uitgevoerd.

#### Legenda argumenten

- -a/--action: welke pipeline er gedraaid moet worden (m: meta-cleaner, ps: pixel-search, pc: pixel-cleaner). [verplicht]
- -i/--image: bestandsnaam. [verplicht]
- -s/--search: waarde waarop gezocht moet worden in de afbeelding. [niet verplicht]
- -p/--profile: mate van anonimisatie (profiel). [niet verplicht - standaard high]
- -r/--replacement: pseudoniem wat op de plaats van persoonsgegevens komt te staan. [niet verplicht - standaard waarde in config.ini]
