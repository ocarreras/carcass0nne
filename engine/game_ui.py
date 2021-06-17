import os
from tkinter import *
from tkinter import messagebox
from engine.game_state import GameState
from engine.placement import Placement
from engine.coords import Coords
from PIL import ImageTk, Image
from PIL import ImageGrab

# https://stackoverflow.com/questions/40658728/clickable-images-for-python

class Gui:
    def on_closing(self):
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.tk_root.destroy()

    def __init__(self):
        self.canvas_width = 1800
        self.canvas_height = 1020
        self.tile_size = 60
        self.meeple_size = 20
        self.tk_root = Tk()

        self.tk_root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = Canvas(self.tk_root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.center_x = self.canvas_width/2 - self.tile_size/2
        self.center_y = self.canvas_height/2 - self.tile_size/2
        self.canvas.pack(fill='both', expand=True)
        self.images_path = os.path.join('engine', 'resources', 'images')
        self.meeple_images = []
        for i in range(5):
            abs_file_path: str = os.path.join(self.images_path, 'meeples', f"{str(i)}.png")
            image = Image.open(abs_file_path).resize((self.meeple_size, self.meeple_size),
                                                 Image.ANTIALIAS)
            self.meeple_images.append(image)
        self.image_ref = []
        self.save_images = []

    def save_canvas_img(self):
        self.canvas.postscript(file="save_canvas.eps")
        img = Image.open("save_canvas.eps")
        self.save_images.append(img)
        if len(self.save_images) > 0:
            self.save_images[0].save("save_canvas.gif",
                                     save_all=True, append_images=self.save_images[1:],
                                     optimize=False,
                                     duration=500, loop=0)

    def draw_game_state(self, game_state: GameState):
        self.canvas.delete('all')
        self.image_ref = []
        PhotoImage(master=self.canvas, width=self.canvas_width, height=self.canvas_height)

        for player in range(game_state.n_players):
            self.canvas.create_text((0, player*20), text=f"Player {player:02d} : {game_state.scores[player]:03d} "
                                                         + f"| {game_state.meeples[player]:02d}",
                                    anchor=NW, fill='blue')

        for coords in game_state.board.board.keys():
            tile = game_state.board[coords]
            self.__draw_tile(coords, tile)
            for placement_type in tile.placements:
                for placement in tile.placements[placement_type]:
                    if placement and placement.meeple is not None:
                        self.__draw_meeple(coords, placement.meeple_xy, tile.rotation, placement.meeple)

        for coords in game_state.board.freeSquares:
            self.__draw_empty(coords)

        self.canvas.update()
        self.save_canvas_img()

    def __coords_to_pixels(self, coords: Coords):
        return self.center_x + coords.x * self.tile_size, \
               self.center_y + coords.y * self.tile_size

    def __draw_square(self, coords: Coords, image):
        photo_image = ImageTk.PhotoImage(image)
        self.image_ref.append(photo_image)
        x, y = self.__coords_to_pixels(coords)
        self.canvas.create_image(x, y, anchor=NW, image=photo_image)

    def __draw_tile(self, coords: Coords, tile):
        abs_file_path: str = os.path.join(self.images_path, tile.image)
        image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size),
                                                 Image.ANTIALIAS).rotate(-90 * tile.rotation)
        self.image_ref.append(image)
        self.__draw_square(coords, image)

    def __draw_empty(self, coords: Coords):
        abs_file_path: str = os.path.join(self.images_path, "Empty.png")
        image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size),
                                                 Image.ANTIALIAS)
        self.__draw_square(coords, image)

    def __draw_meeple(self, coords: Coords, offsets, rotation, player):
        image = self.meeple_images[player]
        x, y = self.__coords_to_pixels(coords)
        rotated_offsets = [offsets[0], offsets[1]]
        for i in range(rotation):
            rotated_offsets[0], rotated_offsets[1] = -rotated_offsets[1], rotated_offsets[0]
        x = x + self.tile_size/2 - self.meeple_size/2 + rotated_offsets[0]
        y = y + self.tile_size/2 - self.meeple_size/2 + rotated_offsets[1]
        photo_image = ImageTk.PhotoImage(image)
        self.image_ref.append(photo_image)
        self.canvas.create_image(x, y, anchor=NW, image=photo_image)
