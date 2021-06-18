import os
import random

from tkinter import *
from tkinter import Button, messagebox
from engine.game_state import GameState
from engine.placement import Placement
from engine.tile import Tile
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
        self.meeple_size = 15
        self.tk_root = Tk()

        self.tk_root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = Canvas(self.tk_root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.center_x = self.canvas_width / 2 - self.tile_size / 2
        self.center_y = self.canvas_height / 2 - self.tile_size / 2
        self.canvas.pack(fill='both', expand=True)
        self.images_path = os.path.join('engine', 'resources', 'images')
        self.meeple_images = []
        for i in range(6):
            abs_file_path: str = os.path.join(self.images_path, 'meeples', f"{str(i)}.png")
            image = Image.open(abs_file_path).resize((self.meeple_size, self.meeple_size),
                                                     Image.ANTIALIAS)
            self.meeple_images.append(image)
        self.image_ref = []
        self.save_images = []

        self.input_available_tile_placements = {}
        self.input_selected_tile_placement_coord = None
        self.input_selected_tile_placement_rotation = None
        self.input_selected_tile = None
        self.input_selected_meeple_placement = 0
        self.input_available_meeple_placements = []
        self.game_state = None

    def save_canvas_img(self):
        self.canvas.postscript(file="save_canvas.eps")
        img = Image.open("save_canvas.eps")
        self.save_images.append(img)
        if len(self.save_images) > 0:
            self.save_images[0].save("save_canvas.gif",
                                     save_all=True, append_images=self.save_images[1:],
                                     optimize=False,
                                     duration=500, loop=0)

    def callback_button(self, event, img_id):
        print("CALLBACK")
        print(img_id)
        print(event)
        # print(NUM)
        self.canvas.delete(img_id)

    def __pixels_to_coords(self, x, y):
        return Coords((y - self.center_y) // self.tile_size,
                      (x - self.center_x) // self.tile_size)

    def callback_input_tile_placement_right(self, event):
        print("TILE - BUTON 2")
        if self.input_selected_tile_placement_coord:
            self.ask_new_meeple_placement()

    def callback_input_tile_placement(self, event):
        coords = self.__pixels_to_coords(event.x, event.y)
        selected = self.input_available_tile_placements[
            coords] if coords in self.input_available_tile_placements else None

        if coords == Coords(-8, -12):
            print("CLICK!!")
            self.ask_new_meeple_placement()

        if selected:
            if self.input_selected_tile_placement_coord and coords == self.input_selected_tile_placement_coord:
                print(selected['rotations'])
                ind = (self.input_selected_tile_placement_rotation + 1) % len(selected['rotations'])
                self.input_selected_tile_placement_rotation = selected['rotations'][ind]
            else:
                self.input_selected_tile_placement_coord = coords
                self.input_selected_tile_placement_rotation = selected['rotations'][0]
            self.__draw_input_tile_placement()

    def __draw_input_tile_placement(self):
        for coords in self.input_available_tile_placements:
            if 'img_id' in self.input_available_tile_placements[coords]:
                self.canvas.delete(self.input_available_tile_placements[coords]['img_id'])

        for coords in self.input_available_tile_placements:
            if self.input_selected_tile_placement_coord and coords == self.input_selected_tile_placement_coord:
                continue
            abs_file_path: str = os.path.join(self.images_path, "Empty.png")
            empty_img = Image.open(abs_file_path).resize((self.tile_size, self.tile_size),
                                                         Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(empty_img)
            self.image_ref.append(photo_image)
            x, y = self.__coords_to_pixels(coords)
            img_id = self.canvas.create_image(x, y, anchor=NW, image=photo_image)
            self.input_available_tile_placements[coords]['img_id'] = img_id
        if self.input_selected_tile_placement_coord:
            self.input_selected_tile.rotation = self.input_selected_tile_placement_rotation
            self.__draw_tile(self.input_selected_tile_placement_coord, self.input_selected_tile)

    def __draw_input_meeple_placement(self):
        for ind, placement in enumerate(self.input_available_tile_placements):
            if not placement:
                continue
            if ind == self.input_selected_meeple_placement:
                self.__draw_meeple(self.input_selected_tile_placement_coord,
                                   placement.meeple_xy,
                                   self.input_selected_tile_placement_rotation, 5)
            else:
                self.__draw_meeple(self.input_selected_tile_placement_coord,
                                   placement.meeple_xy,
                                   self.input_selected_tile_placement_rotation, 4)

    def callback_input_meeple_placement_right(self, event):
        print("MEEPLE SELECTION RIGHT")
        placement = self.input_available_tile_placements[self.input_selected_meeple_placement]
        print("SELECTED PLACEMENT")
        print(placement)
        self.game_state.insert_tile(self.input_selected_tile_placement_coord, self.input_selected_tile,
                                    self.input_selected_tile_placement_rotation, placement)
        self.ask_new_tile_placement()

    def callback_input_meeple_placement(self, event):
        coords = self.__pixels_to_coords(event.x, event.y)
        if coords == Coords(-8, -12):
            print("CLICK!!")
            placement = self.input_available_tile_placements[self.input_selected_meeple_placement]
            print("SELECTED PLACEMENT")
            print(placement)
            self.game_state.insert_tile(self.input_selected_tile_placement_coord, self.input_selected_tile,
                                        self.input_selected_tile_placement_rotation, placement)
            self.ask_new_tile_placement()

        print("MEEEEple")
        self.input_selected_meeple_placement = (self.input_selected_meeple_placement + 1) % \
                                               len(self.input_available_tile_placements)
        self.__draw_input_meeple_placement()

    def ask_new_meeple_placement(self):
        placements = self.game_state.get_available_meeple_placements(self.input_selected_tile,
                                                                     self.input_selected_tile_placement_coord,
                                                                     self.input_selected_tile_placement_rotation)
        self.input_available_tile_placements = placements
        self.__draw_input_meeple_placement()
        self.canvas.bind("<Button-1>", lambda e: self.callback_input_meeple_placement(e))
        self.canvas.bind("<Double-3>", lambda e: self.callback_input_meeple_placement_right(e))
        self.canvas.bind("<KeyPress-Down>", lambda e: self.callback_input_meeple_placement_right(e))
        """

        self.ask_new_tile_placement()
        """

    def ask_new_tile_placement(self):
        if self.game_state.current_player == 1:
            print("PLAYER 1")
            tile: Tile = self.game_state.deck.pop()
            tile_placements = self.game_state.get_available_tile_placements(tile)
            if len(tile_placements) == 0:
                print("BOOOM")
                assert False
            coords, rotation = tile_placements[0]
            meeple_placements = self.game_state.get_available_meeple_placements(tile, coords, rotation)
            random.shuffle(meeple_placements)
            meeple_placement = meeple_placements[0] if len(meeple_placements) > 0 else None
            self.game_state.insert_tile(coords, tile, rotation, meeple_placement)

        print("NEW USER TILE PLACEMENT")
        tile: Tile = self.game_state.deck.pop()
        tile_placements = self.game_state.get_available_tile_placements(tile)
        self.input_selected_tile = tile

        self.draw_game_state(self.game_state, False)
        self.__draw_tile(Coords(-8, -12), tile)

        self.input_selected_tile_placement_coord = None
        self.input_selected_tile_placement_rotation = None
        self.input_available_tile_placements = {}
        for tile_placement in tile_placements:
            coords, rotation = tile_placement
            if coords not in self.input_available_tile_placements:
                self.input_available_tile_placements[coords] = {}
                self.input_available_tile_placements[coords]['rotations'] = []
            self.input_available_tile_placements[coords]['rotations'].append(rotation)
        self.__draw_input_tile_placement()
        self.canvas.bind("<Button-1>", lambda e: self.callback_input_tile_placement(e))
        self.canvas.bind("<Double-3>", lambda e: self.callback_input_tile_placement_right(e))
        self.canvas.bind("<KeyPress-Down>", lambda e: self.callback_input_tile_placement_right(e))

    def interactive(self, state):
        self.game_state = state
        self.ask_new_tile_placement()
        self.tk_root.mainloop()

    def draw_game_state(self, game_state: GameState, draw_free_sqares: bool = True):
        self.canvas.delete('all')
        self.image_ref = []
        PhotoImage(master=self.canvas, width=self.canvas_width, height=self.canvas_height)

        for player in range(game_state.n_players):
            self.canvas.create_text((0, player * 20), text=f"Player {player:02d} : {game_state.scores[player]:03d} "
                                                           + f"| {game_state.meeples[player]:02d}",
                                    anchor=NW, fill='blue')

        for coords in game_state.board.board.keys():
            tile = game_state.board[coords]
            self.__draw_tile(coords, tile)
            for placement_type in tile.placements:
                for placement in tile.placements[placement_type]:
                    if placement and placement.meeple is not None:
                        self.__draw_meeple(coords, placement.meeple_xy, tile.rotation, placement.meeple)

        if draw_free_sqares:
            for coords in game_state.board.freeSquares:
                self.__draw_empty(coords)

        self.canvas.update()
        # self.save_canvas_img()

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
        x = x + self.tile_size / 2 - self.meeple_size / 2 + rotated_offsets[0]
        y = y + self.tile_size / 2 - self.meeple_size / 2 + rotated_offsets[1]
        photo_image = ImageTk.PhotoImage(image)
        self.image_ref.append(photo_image)
        self.canvas.create_image(x, y, anchor=NW, image=photo_image)
