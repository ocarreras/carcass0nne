from enum import Enum
from engine.placement import Placement


class RoadConnection(Enum):
    U = 0
    R = 1
    D = 2
    L = 3


##
# This class represents each road part inside a tile.
class RoadPlacement(Placement):
    def __init__(self, connections: [RoadConnection],
                 termination=False,
                 meeple_xy=None):
        super().__init__(meeple_xy)
        self.connections = connections
        self.termination = termination
