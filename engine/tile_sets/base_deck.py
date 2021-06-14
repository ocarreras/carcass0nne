import os
from engine.tile import Tile, TileBorderType

tile_types = {
    "A": Tile(
        [TileBorderType.FIELD, TileBorderType.FIELD, TileBorderType.ROAD, TileBorderType.FIELD],
        image=os.path.join("base_game", "A.png")
    ),
    "B": Tile(
        [TileBorderType.FIELD, TileBorderType.FIELD, TileBorderType.FIELD, TileBorderType.FIELD],
        image=os.path.join("base_game", "B.png")
    ),
    "C": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.CITY, TileBorderType.CITY],
        image=os.path.join("base_game", "C.png")
    ),
    "D": Tile(
        [TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.FIELD, TileBorderType.ROAD],
        image=os.path.join("base_game", "D.png")
    ),
    "E": Tile(
        [TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.FIELD, TileBorderType.FIELD],
        image=os.path.join("base_game", "E.png")
    ),
    "F": Tile(
        [TileBorderType.FIELD, TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.CITY],
        image=os.path.join("base_game", "F.png")
    ),
    "G": Tile(
        [TileBorderType.FIELD, TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.CITY],
        image=os.path.join("base_game", "G.png")
    ),
    "H": Tile(
        [TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.CITY, TileBorderType.FIELD],
        image=os.path.join("base_game", "H.png")
    ),
    "I": Tile(
        [ TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.FIELD, TileBorderType.CITY],
        image=os.path.join("base_game", "I.png")
    ),
    "J": Tile(
        [TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.FIELD],
        image=os.path.join("base_game", "J.png")
    ),
    "K": Tile(
        [TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.ROAD, TileBorderType.ROAD],
        image=os.path.join("base_game", "K.png")
    ),
    "L": Tile(
        [TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.ROAD],
        image=os.path.join("base_game", "L.png")
    ),
    "M": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.FIELD],
        image=os.path.join("base_game", "M.png")
    ),
    "N": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.FIELD],
        image=os.path.join("base_game", "N.png")
    ),
    "O": Tile(
        [TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.CITY],
        image=os.path.join("base_game", "O.png")
    ),
    "P": Tile(
        [TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.CITY],
        image=os.path.join("base_game", "P.png")
    ),
    "Q": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.CITY],
        image=os.path.join("base_game", "Q.png")
    ),
    "R": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.FIELD, TileBorderType.CITY],
        image=os.path.join("base_game", "R.png")
    ),
    "S": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.CITY],
        image=os.path.join("base_game", "S.png")
    ),
    "T": Tile(
        [TileBorderType.CITY, TileBorderType.CITY, TileBorderType.ROAD, TileBorderType.CITY],
        image=os.path.join("base_game", "T.png")
    ),
    "U": Tile(
        [TileBorderType.ROAD, TileBorderType.FIELD, TileBorderType.ROAD, TileBorderType.FIELD],
        image=os.path.join("base_game", "U.png")
    ),
    "V": Tile(
        [TileBorderType.FIELD, TileBorderType.FIELD, TileBorderType.ROAD, TileBorderType.ROAD],
        image=os.path.join("base_game", "V.png")
    ),
    "W": Tile(
        [TileBorderType.FIELD, TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.ROAD],
        image=os.path.join("base_game", "W.png")
    ),
    "X": Tile(
        [TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.ROAD, TileBorderType.ROAD],
        image=os.path.join("base_game", "X.png")
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
