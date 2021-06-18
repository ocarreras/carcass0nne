import os

from engine.placement import EdgeConnection
from engine.tile import Tile, ShapeType
from engine.city import CityPlacement
from engine.monastery import MonasteryPlacement
from engine.road import RoadPlacement
from engine.field import FieldPlacement, EdgeConnection

tile_types = {
    "A": Tile(
        image=os.path.join("base_game", "A.png"),
        borders=[ShapeType.FIELD, ShapeType.FIELD, ShapeType.ROAD, ShapeType.FIELD],
        monastery_placement=MonasteryPlacement(meeple_xy=[0, 0]),
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 25])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.UL, EdgeConnection.UR, EdgeConnection.RU,
                                                      EdgeConnection.RD, EdgeConnection.DL, EdgeConnection.DR,
                                                      EdgeConnection.LU, EdgeConnection.LD],
                                         meeple_xy=[20, 20],
                                         city_connections=[])],
    ),
    "B": Tile(
        image=os.path.join("base_game", "B.png"),
        borders=[ShapeType.FIELD, ShapeType.FIELD, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=MonasteryPlacement(meeple_xy=[0, 0]),
        city_placements=[],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.UL, EdgeConnection.UR, EdgeConnection.RU,
                                                      EdgeConnection.RD, EdgeConnection.DL, EdgeConnection.DR,
                                                      EdgeConnection.LU, EdgeConnection.LD],
                                         meeple_xy=[20, 20],
                                         city_connections=[])],

    ),
    "C": Tile(
        image=os.path.join("base_game", "C.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.CITY, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.D, EdgeConnection.R,
                                                    EdgeConnection.L],
                                       shield=True,
                                       meeple_xy=[0, 0])],
        road_placements=[],
        field_placements=[],
    ),
    "D": Tile(
        image=os.path.join("base_game", "D.png"),
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.FIELD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R, EdgeConnection.L],
                                       meeple_xy=[0, 0])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.LU],
                                         city_connections=[0],
                                         meeple_xy=[0, -11]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.LD, EdgeConnection.DL,
                                                      EdgeConnection.DR],
                                         meeple_xy=[0, 11],
                                         city_connections=[])],

    ),
    "E": Tile(
        image=os.path.join("base_game", "E.png"),
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.RD, EdgeConnection.DL,
                                                      EdgeConnection.DR, EdgeConnection.LU, EdgeConnection.LD],
                                         meeple_xy=[0, 0],
                                         city_connections=[0])],
    ),
    "F": Tile(
        image=os.path.join("base_game", "F.png"),
        borders=[ShapeType.FIELD, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.R, EdgeConnection.L],
                                       meeple_xy=[0, 0],
                                       shield=True)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.UL, EdgeConnection.UR],
                                         meeple_xy=[0, -22],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.DL, EdgeConnection.DR],
                                         meeple_xy=[0, 26],
                                         city_connections=[0])],
    ),
    "G": Tile(
        image=os.path.join("base_game", "G.png"),
        borders=[ShapeType.FIELD, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.R, EdgeConnection.L],
                                       meeple_xy=[0, 0],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.UL, EdgeConnection.UR],
                                         meeple_xy=[0, -22],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.DL, EdgeConnection.DR],
                                         meeple_xy=[0, 26],
                                         city_connections=[0])],
    ),
    "H": Tile(
        image=os.path.join("base_game", "H.png"),
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False),
                         CityPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 22],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.RD, EdgeConnection.LU,
                                                      EdgeConnection.LD],
                                         meeple_xy=[0, 0],
                                         city_connections=[0, 1])],
    ),
    "I": Tile(
        image=os.path.join("base_game", "I.png"),
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False),
                         CityPlacement(connections=[EdgeConnection.L],
                                       meeple_xy=[-22, 0],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.RD, EdgeConnection.DL,
                                                      EdgeConnection.DR],
                                         meeple_xy=[5, 5],
                                         city_connections=[0, 1])],
    ),
    "J": Tile(
        image=os.path.join("base_game", "J.png"),
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R, EdgeConnection.D],
                                       meeple_xy=[2, 2])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.LU, EdgeConnection.LD,
                                                      EdgeConnection.DL],
                                         meeple_xy=[0, -10],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[26, 26],
                                         city_connections=[]),
                          ],
    ),
    "K": Tile(
        image=os.path.join("base_game", "K.png"),
        borders=[ShapeType.CITY, ShapeType.FIELD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.L, EdgeConnection.D],
                                       meeple_xy=[2, -2])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.RD, EdgeConnection.DR,
                                                      EdgeConnection.LU],
                                         meeple_xy=[0, 10],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.LD, EdgeConnection.DL],
                                         meeple_xy=[-15, 15],
                                         city_connections=[]),
                          ],
    ),
    "L": Tile(
        image=os.path.join("base_game", "L.png"),
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -22],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R],
                                       meeple_xy=[22, 0]),
                         RoadPlacement(connections=[EdgeConnection.L],
                                       meeple_xy=[-22, 0]),
                         RoadPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 22])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.LU],
                                         meeple_xy=[-25, -12],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.LD, EdgeConnection.DL],
                                         meeple_xy=[-20, 20],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[20, 20],
                                         city_connections=[])]),
    "M": Tile(
        image=os.path.join("base_game", "M.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.R],
                                       meeple_xy=[12, -12],
                                       shield=True)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.LU, EdgeConnection.LD, EdgeConnection.DL,
                                                      EdgeConnection.DR],
                                         meeple_xy=[-12, 12],
                                         city_connections=[0])]),
    "N": Tile(
        image=os.path.join("base_game", "N.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.R],
                                       meeple_xy=[12, -12],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.LU, EdgeConnection.LD, EdgeConnection.DL,
                                                      EdgeConnection.DR],
                                         meeple_xy=[-12, 12],
                                         city_connections=[0])]),
    "O": Tile(
        image=os.path.join("base_game", "O.png"),
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.L],
                                       meeple_xy=[-12, -12],
                                       shield=True)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R, EdgeConnection.D],
                                       meeple_xy=[12, 12])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.DL],
                                         meeple_xy=[-12, 20],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[20, 20],
                                         city_connections=[])]),
    "P": Tile(
        image=os.path.join("base_game", "P.png"),
        borders=[ShapeType.CITY, ShapeType.ROAD, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.L],
                                       meeple_xy=[-12, -12],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R, EdgeConnection.D],
                                       meeple_xy=[12, 12])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.DL],
                                         meeple_xy=[-12, 20],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[20, 20],
                                         city_connections=[])]),
    "Q": Tile(
        image=os.path.join("base_game", "Q.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.L, EdgeConnection.R],
                                       meeple_xy=[0, -10],
                                       shield=True)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.DL, EdgeConnection.DR],
                                         meeple_xy=[0, 20],
                                         city_connections=[0])]),
    "R": Tile(
        image=os.path.join("base_game", "R.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.FIELD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.L, EdgeConnection.R],
                                       meeple_xy=[0, -10],
                                       shield=False)],
        road_placements=[],
        field_placements=[FieldPlacement(connections=[EdgeConnection.DL, EdgeConnection.DR],
                                         meeple_xy=[0, 20],
                                         city_connections=[0])]),
    "S": Tile(
        image=os.path.join("base_game", "S.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.L, EdgeConnection.R],
                                       meeple_xy=[0, -10],
                                       shield=True)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 16])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.DL],
                                         meeple_xy=[-10, 20],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.DR],
                                         meeple_xy=[10, 20],
                                         city_connections=[0])
                          ]),
    "T": Tile(
        image=os.path.join("base_game", "T.png"),
        borders=[ShapeType.CITY, ShapeType.CITY, ShapeType.ROAD, ShapeType.CITY],
        monastery_placement=None,
        city_placements=[CityPlacement(connections=[EdgeConnection.U, EdgeConnection.L, EdgeConnection.R],
                                       meeple_xy=[0, -10],
                                       shield=False)],
        road_placements=[RoadPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 16])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.DL],
                                         meeple_xy=[-10, 20],
                                         city_connections=[0]),
                          FieldPlacement(connections=[EdgeConnection.DR],
                                         meeple_xy=[10, 20],
                                         city_connections=[0])
                          ]),
    "U": Tile(
        image=os.path.join("base_game", "U.png"),
        borders=[ShapeType.ROAD, ShapeType.FIELD, ShapeType.ROAD, ShapeType.FIELD],
        monastery_placement=None,
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeConnection.U, EdgeConnection.D],
                                       meeple_xy=[0, 0])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.UR, EdgeConnection.RU, EdgeConnection.RD,
                                                      EdgeConnection.DR],
                                         meeple_xy=[10, 0],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.UL, EdgeConnection.LU, EdgeConnection.LD,
                                                      EdgeConnection.DL],
                                         meeple_xy=[-10, 0],
                                         city_connections=[])]),
    "V": Tile(
        image=os.path.join("base_game", "V.png"),
        borders=[ShapeType.FIELD, ShapeType.FIELD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeConnection.L, EdgeConnection.D],
                                       meeple_xy=[-10, 10])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.LU, EdgeConnection.UR, EdgeConnection.UL,
                                                      EdgeConnection.RU, EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[10, -10],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.LD, EdgeConnection.DL],
                                         meeple_xy=[-15, 15],
                                         city_connections=[])]),
    "W": Tile(
        image=os.path.join("base_game", "W.png"),
        borders=[ShapeType.FIELD, ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R],
                                       meeple_xy=[20, 0]),
                         RoadPlacement(connections=[EdgeConnection.L],
                                       meeple_xy=[-20, 0]),
                         RoadPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 20])],
        field_placements=[FieldPlacement(connections=[EdgeConnection.LU, EdgeConnection.UR, EdgeConnection.UL,
                                                      EdgeConnection.RU],
                                         meeple_xy=[0, -10],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.LD, EdgeConnection.DL],
                                         meeple_xy=[-15, 15],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[15, 15],
                                         city_connections=[])]),
    "X": Tile(
        image=os.path.join("base_game", "X.png"),
        borders=[ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD, ShapeType.ROAD],
        monastery_placement=None,
        city_placements=[],
        road_placements=[RoadPlacement(connections=[EdgeConnection.R],
                                       meeple_xy=[20, 0]),
                         RoadPlacement(connections=[EdgeConnection.L],
                                       meeple_xy=[-20, 0]),
                         RoadPlacement(connections=[EdgeConnection.D],
                                       meeple_xy=[0, 20]),
                         RoadPlacement(connections=[EdgeConnection.U],
                                       meeple_xy=[0, -20])
                         ],
        field_placements=[FieldPlacement(connections=[EdgeConnection.LU, EdgeConnection.UL],
                                         meeple_xy=[-15, -15],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.RU, EdgeConnection.UR],
                                         meeple_xy=[15, -15],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.LD, EdgeConnection.DL],
                                         meeple_xy=[-15, 15],
                                         city_connections=[]),
                          FieldPlacement(connections=[EdgeConnection.RD, EdgeConnection.DR],
                                         meeple_xy=[15, 15],
                                         city_connections=[])])
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
