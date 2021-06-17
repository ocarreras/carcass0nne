import os

from engine.placement import EdgeOrientation
from engine.tile import Tile, ShapeType
from engine.city import CityPlacement
from engine.monastery import MonasteryPlacement
from engine.road import RoadPlacement
from engine.field import FieldPlacement, FieldConnection

tile_types = {
    "A": Tile(
        borders=[ShapeType.FIELD, ShapeType.FIELD, ShapeType.ROAD, ShapeType.FIELD],
        monastery_placement=MonasteryPlacement(meeple_xy=[0, 0]),
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=(0, 25))],
        field_placements=[FieldPlacement([FieldConnection.UL, FieldConnection.UR, FieldConnection.RU,
                                          FieldConnection.RD, FieldConnection.DL, FieldConnection.DR,
                                          FieldConnection.LU, FieldConnection.LD],
                                         city_connections=[])],
        image=os.path.join("base_game", "A.png")
    ),
    "B": Tile(
        borders=[ShapeType.FIELD, ShapeType.FIELD, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=MonasteryPlacement(meeple_xy=[0, 0]),
        city_placements=[],
        road_placements=[],
        field_placements=[FieldPlacement([FieldConnection.UL, FieldConnection.UR, FieldConnection.RU,
                                          FieldConnection.RD, FieldConnection.DL, FieldConnection.DR,
                                          FieldConnection.LU, FieldConnection.LD],
                                         city_connections=[])],
        image=os.path.join("base_game", "B.png")
    ),
    "C": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.CITY, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.D, EdgeOrientation.R,
                                                    EdgeOrientation.L],
                                       shield=True,
                                       meeple_xy=(0, 0))],
        field_placements=[],
        road_placements=[],
        image=os.path.join("base_game", "C.png")
    ),
    "D": Tile(
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.FIELD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R, EdgeOrientation.L],
                                       meeple_xy=[0, 0])],
        field_placements=[FieldPlacement([FieldConnection.RU, FieldConnection.LU],
                                         city_connections=[0]),
                          FieldPlacement([FieldConnection.RD, FieldConnection.LD],
                                         city_connections=[])],
        image=os.path.join("base_game", "D.png")
    ),
    "E": Tile(
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement([FieldConnection.RU, FieldConnection.RD, FieldConnection.DL,
                                          FieldConnection.DR, FieldConnection.LU, FieldConnection.LD],
                                         city_connections=[0])],
        image=os.path.join("base_game", "E.png")
    ),
    "F": Tile(
        borders=[ShapeType.FIELD, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.R, EdgeOrientation.L],
                                       meeple_xy=[0, 0],
                                       shield=True)],
        road_placements=[],
        field_placements=[FieldPlacement([FieldConnection.UL, FieldConnection.UR],
                                         city_connections=[0]),
                          FieldPlacement([FieldConnection.DL, FieldConnection.DR],
                                         city_connections=[0]),
                          ],
        image=os.path.join("base_game", "F.png")
    ),
    "G": Tile(
        borders=[ShapeType.FIELD, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.R, EdgeOrientation.L],
                                       meeple_xy=[0, 0],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement([FieldConnection.UL, FieldConnection.UR],
                                         city_connections=[0]),
                          FieldPlacement([FieldConnection.DL, FieldConnection.DR],
                                         city_connections=[0]),
                          ],
        image=os.path.join("base_game", "G.png")
    ),
    "H": Tile(
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False),
                         CityPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=[0, 22],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement([FieldConnection.RU, FieldConnection.RD,
                                          FieldConnection.LU, FieldConnection.LD],
                                         city_connections=[0, 1])
                          ],
        image=os.path.join("base_game", "H.png")
    ),
    "I": Tile(
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False),
                         CityPlacement(connections=[EdgeOrientation.L],
                                       meeple_xy=[-22, 0],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement([FieldConnection.RU, FieldConnection.RD,
                                          FieldConnection.DL, FieldConnection.DR],
                                         city_connections=[0, 1])
                          ],
        image=os.path.join("base_game", "I.png")
    ),
    "J": Tile(
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R, EdgeOrientation.D],
                                       meeple_xy=[2, 2])],
        field_placements=[FieldPlacement([FieldConnection.RU, FieldConnection.LU, FieldConnection.LD,
                                          FieldConnection.DL],
                                         city_connections=[0]),
                          FieldPlacement([FieldConnection.RD, FieldConnection.DR],
                                         city_connections=[]),
                          ],
        image=os.path.join("base_game", "J.png")
    ),
    "K": Tile(
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.L, EdgeOrientation.D],
                                       meeple_xy=[2, -2])],
        field_placements=[],
        image=os.path.join("base_game", "K.png")
    ),
    "L": Tile(
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R],
                                       meeple_xy=[14, 0]),
                         RoadPlacement(connections=[EdgeOrientation.L],
                                       meeple_xy=[-14, 0]),
                         RoadPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=[0, 14])],
        field_placements=[],
        image=os.path.join("base_game", "L.png")
    ),
    "M": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.R],
                                       meeple_xy=[12, -12],
                                       shield=True)],
        road_placements=[],
        field_placements=[],
        image=os.path.join("base_game", "M.png")
    ),
    "N": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.R],
                                       meeple_xy=[12, -12],
                                       shield=False)],
        road_placements=[],
        field_placements=[],
        image=os.path.join("base_game", "N.png")
    ),
    "O": Tile(
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.L],
                                       meeple_xy=[-12, -12],
                                       shield=True)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R, EdgeOrientation.D],
                                       meeple_xy=[12, 12])],
        field_placements=[],
        image=os.path.join("base_game", "O.png")
    ),
    "P": Tile(
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.L],
                                       meeple_xy=[-12, -12],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R, EdgeOrientation.D],
                                       meeple_xy=[12, 12])],
        field_placements=[],
        image=os.path.join("base_game", "P.png")
    ),
    "Q": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.L, EdgeOrientation.R],
                                       meeple_xy=[0, -10],
                                       shield=True)],
        road_placements=[],
        field_placements=[],
        image=os.path.join("base_game", "Q.png")
    ),
    "R": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.L, EdgeOrientation.R],
                                       meeple_xy=[0, -10],
                                       shield=False)],
        road_placements=[],
        field_placements=[],
        image=os.path.join("base_game", "R.png")
    ),
    "S": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.L, EdgeOrientation.R],
                                       meeple_xy=[0, -10],
                                       shield=True)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=[0, 16])],
        field_placements=[],
        image=os.path.join("base_game", "S.png")
    ),
    "T": Tile(
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeOrientation.U, EdgeOrientation.L, EdgeOrientation.R],
                                       meeple_xy=[0, -10],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=[0, 16])],
        field_placements=[],
        image=os.path.join("base_game", "T.png")
    ),
    "U": Tile(
        borders=[ShapeType.ROAD, ShapeType.FIELD, ShapeType.ROAD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.U, EdgeOrientation.D],
                                       meeple_xy=[0, 0])],
        field_placements=[],
        image=os.path.join("base_game", "U.png")
    ),
    "V": Tile(
        borders=[ShapeType.FIELD, ShapeType.FIELD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.L, EdgeOrientation.D],
                                       meeple_xy=[-10, 10])],
        field_placements=[],
        image=os.path.join("base_game", "V.png")
    ),
    "W": Tile(
        borders=[ShapeType.FIELD, ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        image=os.path.join("base_game", "W.png"),
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R],
                                       meeple_xy=[20, 0]),
                         RoadPlacement(connections=[EdgeOrientation.L],
                                       meeple_xy=[-20, 0]),
                         RoadPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=[0, 20])],
        field_placements=[],
    ),
    "X": Tile(
        borders=[ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        image=os.path.join("base_game", "X.png"),
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeOrientation.R],
                                       meeple_xy=[20, 0]),
                         RoadPlacement(connections=[EdgeOrientation.L],
                                       meeple_xy=[-20, 0]),
                         RoadPlacement(connections=[EdgeOrientation.D],
                                       meeple_xy=[0, 20]),
                         RoadPlacement(connections=[EdgeOrientation.U],
                                       meeple_xy=[0, -20])
                         ],
        field_placements=[],
    ),
}

##
# Setting D=4 as we will use one as the initial tile.
tile_counts = {
    "A": 2,
    "B": 4,
    "C": 1,
    "D": 4,
    "E": 5,
    "F": 2,
    "G": 1,
    "H": 3,
    "I": 2,
    "J": 3,
    "K": 3,
    "L": 3,
    "M": 2,
    "N": 3,
    "O": 2,
    "P": 3,
    "Q": 1,
    "R": 3,
    "S": 2,
    "T": 1,
    "U": 8,
    "V": 9,
    "W": 4,
    "X": 1
}
