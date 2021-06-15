from enum import Enum
from engine.placement import Placement


class FieldConnection(Enum):
    UL = 0
    UR = 1
    RU = 2
    RD = 3
    DR = 4
    DL = 5
    LD = 6
    LU = 7


##
# This class represents each field possible placement inside a tile.
class FieldPlacement(Placement):
    def __init__(self, connections: [FieldConnection], city_connections=None, meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections = connections
        self.cityConnections = city_connections
