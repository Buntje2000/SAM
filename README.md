# Smart-Systems-AMC

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

## Run

Activeer vervolgends de pipeline door dit commando aan te roepen:

```bash
python main.py -i [filename.dcm] -s [search keyword] -p [low/medium/high] -r [replacement value]
```

De pipeline draait nu.
