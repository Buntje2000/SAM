import random
from app.config import config
from app.classes.meta.helper import getReplacement, stringSplitter, valueSplitter, getMetaThreshold

_replacement = str(random.randint(100, 999999))


def test_get_replacement():
    assert getReplacement(_replacement) == _replacement


def test_string_splitter():
    string = "Dit is een string."
    assert stringSplitter(string) == ["Dit", "is", "een", "string"]


def test_value_splitter():
    value1 = ["Test123"]
    value2 = ["Dit123is456een789test"]

    assert valueSplitter(value1) == [
        "Test", "123"]
    assert valueSplitter(value2) == [
        "Dit", "123", "is", "456", "een", "789", "test"]


def test_get_meta_threshold():
    _threshold = float(config("META", "similarity_threshold"))

    if _threshold != None:
        assert getMetaThreshold() == _threshold
    else:
        assert getMetaThreshold() == 0.8
