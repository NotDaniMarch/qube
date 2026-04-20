import pygame

# Modules defined for the game
from classes.state import GameState
from static.settings import *  # all setting constants
from classes.levels import Level
from classes.button import Button
import render

class Game:
    # =========================
    # Setup
    # =========================
    
    # Set up the game environment
    def __init__(self):
        pygame.init()
        render.window_title()

        # Pygame attributes
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Qube game attributes
        self.level = None           # The current level
        self.state = GameState.MENU     # The game state

    # =========================
    # Menu
    # =========================
    
    def menu(self):
        buttons = Level.buttonify(40, 300)  # define menu buttons from level names

        while self.state == GameState.MENU:
            self.clock.tick(60)
            mouse_pos = (0,0)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                    return

                # open corresponding level when the button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button in buttons:
                        if button.is_hovered(mouse_pos):
                            # Set the level
                            self.level = Level(button.text)
                            self.state = GameState.LEVEL

            render.menu(self.screen, buttons)

    # =========================
    # Game loop
    # =========================

    def run(self):
        while self.state == GameState.LEVEL:
            self.clock.tick(60)
            qube = self.level.qube
            dx, dy = 0, 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.state = GameState.MENU
                        return
                    if event.key == pygame.K_r:
                        self.level.start()
                    if event.key == pygame.K_1:
                        self.state = GameState.WIN
                        return
                    if event.key == pygame.K_2:
                        self.state = GameState.LOSE
                        return
                    if event.key == pygame.K_LEFT: dx = -1
                    if event.key == pygame.K_RIGHT: dx = 1
                    if event.key == pygame.K_UP: dy = -1
                    if event.key == pygame.K_DOWN: dy = 1

                    # X gate
                    if event.key == pygame.K_x:
                        qube.toggle_energy()

                    # Z gate (superposition toggle)
                    if event.key == pygame.K_z:
                        qube.toggle_z()

                    # H gate (split/merge)
                    if event.key == pygame.K_h:
                        qube.hadamard()

            # Move the player
            qube.move(self.level, dx, dy)

            # Decide state from collision with tiles
            self.state = self.level.update_collisions()

            # Draw the level on the screen
            render.level(self.screen, self.level)

    def end(self):
        next_level_name = Level.get_next_level_name(self.level.name)
        
        # Define end screen buttons
        button_layout = {    
                "retry":[],
                "menu":[]
            }
        if self.state == GameState.WIN and next_level_name != None: button_layout["next >>>"] = []
        buttons = Button.from_dict(button_layout, 50, 200)

        while self.state == GameState.WIN or self.state == GameState.LOSE:
            self.clock.tick(60)
            mouse_pos = (0,0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.state = GameState.MENU
                        return
                    if event.key == pygame.K_r:
                        self.state = GameState.LEVEL
                        self.level.start()
                        return

                # When a button is clicked do corresponding action
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button in buttons:
                        if button.is_hovered(mouse_pos):
                            match button.text:
                                case "next >>>":
                                    self.level = Level(next_level_name)
                                    self.state = GameState.LEVEL
                                case "retry":
                                    self.state = GameState.LEVEL
                                    self.level.start()
                                case "menu":
                                    self.state = GameState.MENU
                            return
            
            # Win screen on top of the level
            render.level(self.screen, self.level, self.state)
            render.end(self.screen, buttons, self.state)
        
# =========================
# Run the game
# =========================

game = Game()

while True:
    match game.state:
        case GameState.QUIT:
            break
        case GameState.MENU:
            game.menu()  
        case GameState.LEVEL:
            game.run()
        case GameState.WIN | GameState.LOSE:
            game.end()

pygame.quit()