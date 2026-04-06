import pygame
from settings import *

# =========================
# Colors
# =========================

LOW = (50, 106, 168)    # Low-energy cube
HIGH = (137, 212, 255)   # High-energy cube
LOW_DOOR = (42, 73, 109)
HIGH_DOOR = (86, 126, 152)

BG = (34, 40, 49)
WALL = (57, 62, 70)
GOAL = (56, 235, 77)
KILL = (255, 90, 90)

PLATE_LOW = (38, 56, 78)
PLATE_HIGH = (59, 83, 100)
LOW_WALL = (42, 73, 109)
HIGH_WALL = (86, 126, 152)
OPEN_WALL = (44, 50, 57)

Z_CHOICE = (245, 245, 255)
OBSERVE = (214, 210, 198)

# =========================
# Drawing
# =========================

def draw(game):
    # Draw background
    game.screen.fill(BG)
    
    # Draw level
    for y, row in enumerate(game.level.tiles):
        for x, c in enumerate(row):
            # Walls
            if c == "#":
                draw_rect(game, x, y, WALL)

            # Goal area
            elif c == "G":
                draw_rect(game, x, y, GOAL)

            # Observation block
            elif c == "O":
                draw_pattern(game, x, y, [
                    [0,0,0],
                    [0,1,0],
                    [0,0,0]
                    ], OBSERVE)
                
            # Killer block
            elif c == "K":
                draw_rect(game, x, y, KILL)

            # Filter doors
            elif c == "L":
                draw_pad(game, x, y, LOW_DOOR)
            elif c == "H":
                draw_pad(game, x, y, HIGH_DOOR)
            
            # Low-energy plate
            elif c == "P":  
                draw_pattern(game, x, y, [
                    [1,0,1],
                    [0,1,0],
                    [1,0,1]
                    ], PLATE_LOW)
            
            # High-energy plate
            elif c == "Q":
                draw_pattern(game, x, y, [
                    [0,1,0],
                    [1,1,1],
                    [0,1,0]
                    ], PLATE_HIGH)
                
            # Low-linked door
            elif c == "D":  
                if  game.plate_pressed(0,0) and not game.plate_pressed(0,1) or game.is_tile_occupied(x,y):
                    draw_rect(game, x, y, OPEN_WALL)
                else:
                    draw_rect(game, x, y, LOW_WALL)

            # High-linked door
            elif c == "E":  
                if game.plate_pressed(1,1) and not game.plate_pressed(1,0) or game.is_tile_occupied(x,y):
                    draw_rect(game, x, y, OPEN_WALL)
                else:
                    draw_rect(game, x, y, HIGH_WALL)
            
    # Draw the player
    for p in game.players:
        draw_player(game, p)

    # Update the frame
    pygame.display.flip()

# =========================
# Helpers
# =========================

# Draw a rectangle
def draw_rect(game, x, y, color):
    shape = (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(game.screen, color, shape)

# Draw a pad
def draw_pad(game, x, y, color):
    shape = (x*TILE_SIZE+10, y*TILE_SIZE+10, TILE_SIZE-20, TILE_SIZE-20)
    pygame.draw.rect(game.screen, color, shape)

# Draw a 3x3 pattern in a tile
def draw_pattern(game, x, y, pattern, color):
    sub = TILE_SIZE // 3
    for rowi in range(3):
        for coli in range(3):
            if pattern[rowi][coli]:
                pygame.draw.rect(game.screen, color, (x*TILE_SIZE+coli*sub, y*TILE_SIZE+rowi*sub, sub, sub))

# Draw the player
def draw_player(game, p):
        base_color = HIGH if p.energy else LOW

        if not p.superposed:
            pygame.draw.rect(game.screen, base_color, (p.x*TILE_SIZE, p.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        else:
            if p.energy == 0:
                draw_pattern(game, p.x, p.y, [
                    [0,1,0],
                    [1,0,1],
                    [0,1,0]
                    ], LOW)
            else:
                draw_pattern(game, p.x, p.y, [
                    [1,0,1],
                    [0,0,0],
                    [1,0,1]
                    ], HIGH)
            
            # Visualize Z-choice with a border instead of a dot
            font = pygame.font.SysFont(None, 28)  # None = default font, 28pt size
            text_surface = font.render(f"Z choice {'HIGH' if game.z else 'LOW'}", True, HIGH if game.z else LOW)
            game.screen.blit(text_surface, (10, 10))  # Top-left corner