from enum import Enum, IntEnum


class TileBorderType(Enum):
    ROAD = 1
    FIELD = 2
    CITY = 3


class TileBorderOrientation(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Tile:
    def __init__(self, borders: [TileBorderType], image):
        self.borders = borders
        self.rotation = 0
        self.cities = []
        self.roads = []
        self.fields = []
        self.monastery = False
        self.image = image

    def __str__(self):
        return f"{self.image} R:{self.rotation}"

    def get_border(self, orientation: TileBorderOrientation):
        return self.borders[(orientation + self.rotation) % 4]
