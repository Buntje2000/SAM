from app.classes.Fruit import Fruit

from app.classes.image.preProcessImage import *

class TestClass:
    prop = "test"
    _fruit = Fruit()

    def read(self):
        return self._fruit.get_apple()