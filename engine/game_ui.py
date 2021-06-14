import os
from tkinter import *
from tkinter import messagebox
from engine.game_state import GameState
from PIL import ImageTk, Image


class Gui:
    """
    meeple_icons = {
        MeepleType.NORMAL: ["blue_meeple.png", "refrom tkd_meeple.png", "black_meeple.png", "yellow_meeple.png", "green_meeple.png", "pink_meeple.png"],
        MeepleType.ABBOT: ["blue_abbot.png", "red_abbot.png", "black_abbot.png", "yellow_abbot.png", "green_abbot.png", "pink_abbot.png"]
    }    
    meeple_size = 15
    big_meeple_size = 25
    meeple_size = 15

    meeple_position_offsVisualiserets = {
        Side.TOP: (tile_size / 2, (meeple_size / 2) + 3),
        Side.RIGHT: (tile_size - (meeple_size / 2) - 3, tile_size / 2),
        Side.BOTTOM: (tile_size / 2, tile_size - (meeple_size / 2) - 3),
        Side.LEFT: ((meeple_size / 2) + 3, tile_size / 2),
        Side.CENTER: (tile_size / 2, tile_size / 2),
        Side.TOP_LEFT: (tile_size / 4, (meeple_size / 2) + 3),
        Side.TOP_RIGHT: ((tile_size / 4) * 3, (meeple_size / 2) + 3),
        Side.BOTTOM_LEFT: (tile_size / 4, tile_size - (meeple_size / 2) - 3),
        Side.BOTTOM_RIGHT: ((tile_size / 4) * 3, tile_size - (meeple_size / 2) - 3)
    }

    big_meeple_position_offsets = {
        Side.TOP: (tile_size / 2, (big_meeple_size / 2) + 3),
        Side.RIGHT: (tile_size - (big_meeple_size / 2) - 3, tile_size / 2),
        Side.BOTTOM: (tile_size / 2, tile_size - (big_meeple_size / 2) - 3),
        Side.LEFT: ((big_meeple_size / 2) + 3, tile_size / 2),
        Side.CENTER: (tile_size / 2, tile_size / 2),
        Side.TOP_LEFT: (tile_size / 4, (big_meeple_size / 2) + 3),Image.open(
        Side.TOP_RIGHT: ((tile_size / 4) * 3, (big_meeple_size / 2) + 3),
        Side.BOTTOM_LEFT: (tile_size / 4, tile_size - (big_meeple_size / 2) - 3),
        Side.BOTTOM_RIGHT: ((tile_size / 4) * 3, tile_size - (big_meeple_size / 2) - 3)
    }
    """

    def on_closing(self):
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.tk_root.destroy()

    def __init__(self):
        self.canvas_width = 1800
        self.canvas_height = 1020
        self.tile_size = 60
        self.tk_root = Tk()

        self.tk_root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = Canvas(self.tk_root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.center_x = self.canvas_width/2 - self.tile_size/2
        self.center_y = self.canvas_height/2 - self.tile_size/2
        self.canvas.pack(fill='both', expand=True)
        self.images_path = os.path.join('engine', 'resources', 'images')
        self.image_ref = []

    def draw_game_state(self, game_state: GameState):
        self.canvas.delete('all')
        self.image_ref = []

        for coords in game_state.board.keys():
            tile = game_state.board[coords]
            self.__draw_tile(coords, tile)

        for coords in game_state.freeSquares:
            self.__draw_empty(coords)

        #for row_index, row in enumerate(game_state.board):Image.open(
        #    for column_index, tile in enumerate(row):
        #        tile: Tile
        #        if tile is not None:
        #            self.__draw_tile(column_index, row_index, tile)

        #for player, placed_meeples in enumerate(game_state.placed_meeples):
        #    meeple_position: MeeplePosition
        #    for meeple_position in placed_meeples:
        #        self.__draw_meeple(player, meeple_position)
        self.canvas.update()

    def __coords_to_pixels(self, coords):
        return self.center_x + coords[1] * self.tile_size, \
               self.center_y + coords[0] * self.tile_size

    def __draw_square(self, coords, image):
        photo_image = ImageTk.PhotoImage(image)
        self.image_ref.append(photo_image)
        x, y = self.__coords_to_pixels(coords)
        self.canvas.create_image(x, y, anchor=NW, image=photo_image)

    def __draw_tile(self, coords, tile):
        print(f"Rotation: {tile.rotation}")
        abs_file_path: str = os.path.join(self.images_path, tile.image)
        image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size),
                                                 Image.ANTIALIAS).rotate(90 * tile.rotation)
        self.__draw_square(coords, image)

    def __draw_empty(self, coords):
        abs_file_path: str = os.path.join(self.images_path, "Empty.png")
        image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size),
                                                 Image.ANTIALIAS)
        self.__draw_square(coords, image)

    """
    def __draw_meeple(self, player_index: int, meeple_position: MeeplePosition):
        image = self.__get_image(player=player_index, meeple_type=meeple_position.meeple_type)
        self.image_ref.append(image)

        if meeple_position.meeple_type == MeepleType.BIG:
            x = meeple_position.coordinate_with_side.coordinate.column * self.tile_size + self.big_meeple_position_offsets[meeple_position.coordinate_with_side.side][0]
            y = meeple_position.coordinate_with_side.coordinate.row * self.tile_size + self.big_meeple_position_offsets[meeple_position.coordinate_with_side.side][1]
        else:
            x = meeple_position.coordinate_with_side.coordinate.column * self.tile_size + self.meeple_position_offsets[meeple_position.coordinate_with_side.side][0]
            y = meeple_position.coordinate_with_side.coordinate.row * self.tile_size + self.meeple_position_offsets[meeple_position.coordinate_with_side.side][1]

        self.canvas.create_image(
            x,
            y,
            anchor=CENTER,
            image=image
        )
        
    def __get_image(self, player: int, meeple_type: MeepleType):
        icon_type = MeepleType.NORMAL
        if meeple_type == MeepleType.ABBOT:
            icon_type = meeple_type

        image_filename = self.meeple_icons[icon_type][player]
        abs_file_path = os.path.join(self.images_path, image_filename)

        if meeple_type == MeepleType.NORMAL or meeple_type == MeepleType.ABBOT:
            return ImageTk.PhotoImage(Image.open(abs_file_path).resize((self.meeple_size, self.meeple_size), Image.ANTIALIAS))
        elif meeple_type == MeepleType.BIG:
            return ImageTk.PhotoImage(Image.open(abs_file_path).resize((self.big_meeple_size, self.big_meeple_size), Image.ANTIALIAS))
        elif meeple_type == MeepleType.FARMER:
            return ImageTk.PhotoImage(Image.open(abs_file_path).resize((self.meeple_size, self.meeple_size), Image.ANTIALIAS).rotate(-90))
        elif meeple_type == MeepleType.BIG_FARMER:
            return ImageTk.PhotoImage(Image.open(abs_file_path).resize((self.big_meeple_size, self.big_meeple_size), Image.ANTIALIAS).rotate(-90))        
    """
