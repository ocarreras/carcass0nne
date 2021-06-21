import os
import random

from tkinter import *
from engine.game_state import GameState
from engine.tile import Tile
from engine.coords import Coords
from PIL import ImageTk, Image

import numpy as np
from agents.alpha0.utils import *
from agents.alpha0.MCTS import MCTS
from agents.alpha0.nn.NNet import NNetWrapper as nn

args = dotdict({
    'numIters': 1000,
    'numEps': 2,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

class Gui:
    def on_closing(self):
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.tk_root.destroy()
        if self.game_state:
            print("FINAL_SCORE")
            self.game_state.calc_final_score()
            self.game_state.print_score()

    def __init__(self, game):
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

        ##
        # For interactive game-hack
        self.input_available_tile_placements = {}
        self.input_selected_tile_placement_coord = None
        self.input_selected_tile_placement_rotation = None
        self.input_selected_tile = None
        self.input_selected_meeple_placement = 0
        self.input_available_meeple_placements = []
        self.input_available_meeple_placements_imgs = []
        self.game_state = None

        ##
        # ML - HAX
        if 0:
            self.game = game
            self.n1 = nn(self.game)
            self.n1.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
            self.n1mcts = MCTS(self.game, self.n1, args)
            self.current_V = 0
    ##
    # Generate gif animations
    def save_canvas_img(self):
        self.canvas.postscript(file="save_canvas.eps")
        img = Image.open("save_canvas.eps")
        self.save_images.append(img)
        if len(self.save_images) > 0:
            self.save_images[0].save("save_canvas.gif",
                                     save_all=True, append_images=self.save_images[1:],
                                     optimize=False,
                                     duration=500, loop=0)

    def __pixels_to_coords(self, x, y):
        return Coords(int((y - self.center_y) // self.tile_size),
                      int((x - self.center_x) // self.tile_size))

    def callback_input_tile_placement_next(self, event=None):
        if self.input_selected_tile_placement_coord:
            self.ask_new_meeple_placement()

    def callback_input_tile_placement(self, event):
        coords = self.__pixels_to_coords(event.x, event.y)
        selected = self.input_available_tile_placements[coords] if coords in self.input_available_tile_placements \
            else None
        if selected:
            if self.input_selected_tile_placement_coord and coords == self.input_selected_tile_placement_coord:
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
            x, y = self.__get_canvas_xy_from_game_coords(coords)
            empty_img_id = self.__draw_image(abs_file_path, x, y, 0)
            self.input_available_tile_placements[coords]['img_id'] = empty_img_id

        if self.input_selected_tile_placement_coord:
            self.input_selected_tile.rotation = self.input_selected_tile_placement_rotation
            self.__draw_tile(self.input_selected_tile_placement_coord, self.input_selected_tile)

    def __draw_input_meeple_placement(self):
        for img in self.input_available_meeple_placements_imgs:
            self.canvas.delete(img)
        self.input_available_meeple_placements_imgs = []
        for ind, placement in enumerate(self.input_available_tile_placements):
            if not placement:
                continue
            if ind == self.input_selected_meeple_placement:
                img = self.__draw_meeple(self.input_selected_tile_placement_coord,
                                         placement.meeple_xy,
                                         self.input_selected_tile_placement_rotation, 5)
            else:
                img = self.__draw_meeple(self.input_selected_tile_placement_coord,
                                         placement.meeple_xy,
                                         self.input_selected_tile_placement_rotation, 4)
            self.input_available_meeple_placements_imgs.append(img)

    def callback_input_meeple_placement_next(self, event=None):
        print("Meeple Callback - Next")
        placement = self.input_available_tile_placements[self.input_selected_meeple_placement]
        print("Inserting")
        print(self.input_selected_tile_placement_coord)
        print(self.input_selected_tile_placement_rotation)
        print(placement)
        self.game_state.insert_tile(self.input_selected_tile_placement_coord, self.input_selected_tile,
                                    self.input_selected_tile_placement_rotation, placement)
        self.ask_new_tile_placement()

    def callback_input_meeple_placement(self, event):
        coords = self.__pixels_to_coords(event.x, event.y)
        print("Meeple Callback")
        selected_placement = 0
        min_dist = None
        for ind in range(len(self.input_available_tile_placements)):
            placement = self.input_available_tile_placements[ind]
            if not placement:
                continue
            coords = self.input_selected_tile_placement_coord
            rotation = self.input_selected_tile_placement_rotation
            x, y = self.__get_canvas_xy_from_meeple_coords(coords, placement.meeple_xy, rotation)
            dist = (x+self.meeple_size/2-event.x)**2 + (y+self.meeple_size/2-event.y)**2
            if dist < 150:
                if not min_dist or dist < min_dist:
                    selected_placement = ind

        if selected_placement != self.input_selected_meeple_placement:
            self.input_selected_meeple_placement = selected_placement
            self.__draw_input_meeple_placement()


    def ask_new_meeple_placement(self):
        placements = self.game_state.get_available_meeple_placements(self.input_selected_tile,
                                                                     self.input_selected_tile_placement_coord,
                                                                     self.input_selected_tile_placement_rotation)
        self.input_selected_meeple_placement = 0
        self.input_available_tile_placements = placements
        if len(placements) <= 1:
            return self.callback_input_meeple_placement_next()
        self.__draw_input_meeple_placement()
        self.canvas.bind("<Button-1>", lambda e: self.callback_input_meeple_placement(e))
        self.canvas.bind("<Button-2>", lambda e: self.callback_input_meeple_placement_next(e))

    def play_ai_random(self):
        if 0:
            tile_placements = []
            while len(tile_placements) == 0:
                if len(self.game_state.deck) == 0:
                    return self.on_closing()
                tile: Tile = self.game_state.deck.pop()
                tile_placements = self.game_state.get_available_tile_placements(tile)
            print("RANDOM_PLAY")
            print(f"PLAYER: {self.game_state.current_player}")
            random.shuffle(tile_placements)
            coords, rotation = tile_placements[0]
            meeple_placements = self.game_state.get_available_meeple_placements(tile, coords, rotation)
            random.shuffle(meeple_placements)
            meeple_placement = meeple_placements[0] if len(meeple_placements) > 0 else None
            self.game_state.insert_tile(coords, tile, rotation, meeple_placement)
        else:
            tile = self.game_state.get_new_tile()
            if not tile:
                return self.on_closing()

            canonical = self.game.getCanonicalForm(self.game_state, -1)
            action_id = np.argmax(self.n1mcts.getActionProb(canonical, temp=0))
            print("ML Action ID")
            print(action_id)
            self.game_state, curPlayer = self.game.getNextState(self.game_state, -1, action_id)
            _, self.current_V = self.n1.predict(self.game_state.ml_get_board(), self.game_state.ml_get_aux())

    def ask_new_tile_placement(self):
        if self.game_state.current_player == 1:
            self.play_ai_random()
        print(f"USER_PLAY")
        print(f"PLAYER: {self.game_state.current_player}")

        tile = self.game_state.get_new_tile()
        if not tile:
            return self.on_closing()
        tile_placements = self.game_state.get_available_tile_placements(tile)
        self.input_selected_tile = tile

        self.draw_game_state(self.game_state, False)
        self.__draw_tile(Coords(-8, -12), tile)
        self.input_selected_tile_placement_coord = None
        self.input_selected_tile_placement_rotation = None
        self.input_available_tile_placements = {}

        # This is very uggly, but will do for now.
        for tile_placement in tile_placements:
            coords, rotation = tile_placement
            if coords not in self.input_available_tile_placements:
                self.input_available_tile_placements[coords] = {}
                self.input_available_tile_placements[coords]['rotations'] = []
            self.input_available_tile_placements[coords]['rotations'].append(rotation)
        self.__draw_input_tile_placement()
        self.canvas.bind("<Button-1>", lambda e: self.callback_input_tile_placement(e))
        self.canvas.bind("<Button-2>", lambda e: self.callback_input_tile_placement_next(e))

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
        self.canvas.create_text((0, 60), text=f"Deck size : {len(game_state.deck)}",
                                anchor=NW, fill='blue')
        self.canvas.create_text((0, 80), text=f"V         : {self.current_V}",
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

    def __draw_image(self, image_path: str, x, y, rotation):
        image = Image.open(image_path).resize((self.tile_size, self.tile_size),
                                              Image.ANTIALIAS).rotate(-90 * rotation)
        self.image_ref.append(image)
        photo_image = ImageTk.PhotoImage(image)
        self.image_ref.append(photo_image)
        self.canvas.create_image(x, y, anchor=NW, image=photo_image)
        return photo_image

    def __draw_meeple(self, coords: Coords, offsets, rotation, player):
        image = self.meeple_images[player]
        x, y = self.__get_canvas_xy_from_meeple_coords(coords, offsets, rotation)
        photo_image = ImageTk.PhotoImage(image)
        self.image_ref.append(photo_image)
        self.canvas.create_image(x, y, anchor=NW, image=photo_image)
        return photo_image

    def __draw_tile(self, coords: Coords, tile):
        tile_file = os.path.join("base_game", f"{tile.tile_type}.png")
        abs_file_path: str = os.path.join(self.images_path, tile_file)
        x, y = self.__get_canvas_xy_from_game_coords(coords)
        self.__draw_image(abs_file_path, x, y, tile.rotation)

    def __draw_empty(self, coords: Coords):
        abs_file_path: str = os.path.join(self.images_path, "Empty.png")
        x, y = self.__get_canvas_xy_from_game_coords(coords)
        self.__draw_image(abs_file_path, x, y, 0)

    def __get_canvas_xy_from_game_coords(self, coords: Coords):
        return self.center_x + coords.x * self.tile_size, \
               self.center_y + coords.y * self.tile_size

    def __get_canvas_xy_from_meeple_coords(self, coords, offsets, rotation):
        x, y = self.__get_canvas_xy_from_game_coords(coords)
        rotated_offsets = [offsets[0], offsets[1]]
        for i in range(rotation):
            rotated_offsets[0], rotated_offsets[1] = -rotated_offsets[1], rotated_offsets[0]
        x = x + self.tile_size / 2 - self.meeple_size / 2 + rotated_offsets[0]
        y = y + self.tile_size / 2 - self.meeple_size / 2 + rotated_offsets[1]
        return x, y
