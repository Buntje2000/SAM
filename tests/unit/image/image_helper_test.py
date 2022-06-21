from app.classes.image.helper import getPixelThreshold, getMinConfidence
from app.config import config


def test_get_pixel_threshold():
    _threshold = float(config("PIXEL", "similarity_threshold"))

    if _threshold != None:
        assert getPixelThreshold() == _threshold
    else:
        assert getPixelThreshold() == 0.6


def test_min_confidence():
    _confidence = int(config("PIXEL", "min_confidence"))

    if _confidence != None:
        assert getMinConfidence() == _confidence
    else:
        assert getMinConfidence() == 60
