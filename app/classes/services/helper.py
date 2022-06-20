import difflib


def similarity(word, pattern):
    return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()
