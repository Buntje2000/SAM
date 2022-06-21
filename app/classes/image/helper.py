from app.config import config
import logging

logger = logging.getLogger('file')


def getPixelThreshold():
    cft = None
    try:
        # Spelfouten acceptatie ratio
        cft = float(config("PIXEL", "similarity_threshold"))
    except Exception as e:
        logger.warning(e)

    if cft != None and cft < 0.3:
        threshold = cft
        logger.warning(
            "Pixel threshold is erg laag ingesteld (< 0.3). Dit verhoogt de kans op foutieve waarden. Controleer config.ini")
    elif cft != None:
        threshold = cft
    else:
        threshold = 0.6
        logger.warning(
            "Pixel threshold is niet goed ingesteld. Standaardwaarde wordt gebruikt (0.6). Controleer config.ini")

    return threshold


def getMinConfidence():
    cnf = None
    try:
        # Minimale zekerheid van herkenning
        cnf = int(config("PIXEL", "min_confidence"))
    except Exception as e:
        logger.warning(e)

    if cnf != None and cnf < 30:
        conf = cnf
        logger.warning(
            "Minimale 'confidence' is erg laag ingesteld (< 30). Dit verhoogt de kans op foutieve waarden. Controleer config.ini")
    elif cnf != None:
        conf = cnf
    else:
        conf = 60
        logger.warning(
            "Minimale 'confidence' is niet goed ingesteld. Standaardwaarde wordt gebruikt (60). Controleer config.ini")

    return conf
