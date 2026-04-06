import pygame
import random

# Modules defined for the game
from settings import *  # all setting constants
from levels import Level
from player import Cube
import render

class Game:
    # =========================
    # Setup
    # =========================
    
    # Set up the game environment
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.clock = pygame.time.Clock()

        # Initializing blank attributes
        self.players = []   # Player and it's instances
        self.z = 0  # The current Z choice
        self.high_plates = []   # The coordinates of all high energy plates
        self.low_plates = []    # The coordinates of all low energy plates
        self.level = None   # The current chosen level
        self.running = False    # Is a level being played?
    
    def open_level(self, level_name):
        # Set the level
        level = Level(level_name)
        self.level = level

        # Set the player at the start position
        self.reset()

    # =========================
    # Main game loop
    # =========================

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)

            dx, dy = 0, 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_LEFT: dx = -1
                    if event.key == pygame.K_RIGHT: dx = 1
                    if event.key == pygame.K_UP: dy = -1
                    if event.key == pygame.K_DOWN: dy = 1

                    # X gate
                    if event.key == pygame.K_x and len(self.players) == 1:
                        self.players[0].energy ^= 1

                    # Z gate (superposition toggle)
                    if event.key == pygame.K_z and len(self.players) == 2:
                        self.z ^= 1

                    # H gate (split/merge)
                    if event.key == pygame.K_h:
                        if len(self.players) == 1:
                            p = self.players[0]
                            self.players = [Cube(p.x,p.y,0,1), Cube(p.x,p.y,1,1)]
                            self.z = 0
                        elif len(self.players) == 2:
                            for p in self.players:
                                if p.energy == self.z:
                                    self.players = [Cube(p.x,p.y,self.z,0)]
                                    break

            # Move players
            for p in self.players:
                p.move(self, dx, dy)

            # Tile interactions
            new_players = []
            for p in self.players:
                tile = self.level.getTileAt(p.y, p.x)
                if tile == "K":  # Kill
                    new_players = []
                    break
                if tile == "O" and len(self.players) > 1:  # Observation
                    chosen_player = random.choice(self.players)
                    new_players = [Cube(chosen_player.x,chosen_player.y,chosen_player.energy,0)]
                    break
                if tile == "G":
                    self.running = False
                new_players.append(p)
            self.players = new_players

            render.draw(self)

        pygame.quit()

    # =========================
    # Helpers
    # =========================

    # reset the game by resetting the player
    def reset(self):
        # if self.level == None: return

        x, y = self.level.find_start()
        self.players = [Cube(x, y, 0,0)]

    def is_tile_occupied(self, x, y):
        return any(p.x == x and p.y == y for p in self.players)

    def plate_pressed(self, player_energy, plate_energy):
        # Ignore when player is killed or not superposed
        if len(self.players) == 0 or not self.players[0].superposed: return False

        plate_poss = self.level.low_plates if plate_energy == 0 else self.level.high_plates
        player_pos = (self.players[player_energy].x, self.players[player_energy].y)
        opp_player_pos = (self.players[player_energy ^ 1].x, self.players[player_energy ^ 1].y)

        return player_pos in plate_poss and not opp_player_pos in plate_poss
        
# =========================
# Run the game
# =========================

qube = Game()
qube.open_level("observation")
qube.run()