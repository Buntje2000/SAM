import logging
from app.config import config
import re

logger = logging.getLogger('file')


def stringSplitter(value) -> list:
    values = re.findall(r"[\w']+", value)
    return values


def valueSplitter(values: list) -> list:
    for i in range(len(values)):
        value = re.findall('\d+|\D+', values[i])
        values[i] = value[0]
        value.pop(0)
        for i in range(len(value)):
            values.append(value[i])
    return values


def getReplacement(replacement):
    if replacement == None:
        replacement = str(config("META", "replacement_value"))
    else:
        replacement = replacement

    return replacement


def getMetaThreshold():
    cft = None
    try:
        # Spelfouten acceptatie ratio
        cft = float(config("META", "similarity_threshold"))
    except Exception as e:
        logger.warning(e)

    if cft != None and cft < 0.4:
        threshold = cft
        logger.warning(
            "Meta threshold is erg laag ingesteld (< 0.4). Dit verhoogt de kans op foutieve waarden. Controleer config.ini")
    elif cft != None:
        threshold = cft
    else:
        threshold = 0.8
        logger.warning(
            "Meta threshold is niet goed ingesteld. Standaardwaarde wordt gebruikt (0.8). Controleer config.ini")

    return threshold
