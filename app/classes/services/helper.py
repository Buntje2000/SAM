import difflib


def similarity(word, pattern) -> float:
    return difflib.SequenceMatcher(
        a=word.lower(), b=pattern.lower()).ratio()
