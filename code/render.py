import pygame
from enum import Enum
import re

import static.text as text
from static.settings import *
from classes.player import Energy
from classes.levels import Tile
from classes.state import GameState

# =========================
# Fonts
# =========================
# Have to be implemented as functions since they require the pygame to be initialized

# -------- Game -----------

def get_default_font():
    return pygame.font.SysFont(None, 28)

def get_info_font():
    return pygame.font.SysFont(None, 28, italic=True)

# -------- Menu -----------

def get_title_font():
    return pygame.font.SysFont("consolas", 50, bold=True)

def get_subtitle_font():
    return pygame.font.SysFont("consolas", 30)


# =========================
# Colors
# =========================

class Color(Enum):
    BG_MENU = (15, 18, 24)
    TITLE_TEXT = (245, 245, 255)
    SUBTITLE_TEXT = 224, 234, 242

    ENERGY_LOW = (50, 106, 168)
    ENERGY_HIGH = (137, 212, 255)
    DOOR_LOW = (42, 73, 109)
    DOOR_HIGH = (86, 126, 152)

    BG = (34, 40, 49)
    WALL = (57, 62, 70)
    GOAL = (56, 235, 77)

    KILL = (255, 90, 90)
    OBSERVE = (214, 210, 198)

    LINKED_WALL_LOW = (42, 73, 109)
    LINKED_WALL_HIGH = (86, 126, 152)
    LINKED_WALL_OPEN = (44, 50, 57)
    PLATE_LOW = WALL
    PLATE_HIGH = WALL

    # Winning colors
    BG_WIN = (34, 49, 37)
    WALL_WIN = (57, 70, 61)

    # Losing colors
    BG_LOSE = (49, 34, 34)
    WALL_LOSE = (70, 57, 57)

    # For text background
    SHADOW = (0,0,0,150)

    # Conditional color utility
    def from_energy(energy):
        return Color.ENERGY_HIGH.rgb if energy.high() else Color.ENERGY_LOW.rgb
    
    # Nicer looking vay to get color values
    @property
    def rgb(self):
        return self.value
    

# =========================
# Window Title
# ========================= 
# added here for consistency (all the rendering is done in this module)

def window_title():
    pygame.display.set_caption(text.WINDOW_TITLE)


# =========================
# Menu
# =========================

def menu(screen, buttons):
    screen.fill(Color.BG_MENU.rgb)

    # Title
    screen.blit(
        get_title_font().render(text.GAME_TITLE.title(), True, Color.TITLE_TEXT.rgb),
        (50, 50)
    )

    # Seperating line
    draw_line_break(screen, 110, 50, 700, Color.TITLE_TEXT.rgb)

    # Add description
    draw_multiline(
        screen,
        sentence_case(text.GAME_DESCRIPTION),
        (50, 130),
        get_subtitle_font(),
        Color.SUBTITLE_TEXT.rgb,
        Color.BG.rgb,
    )

    # Promt to select level
    screen.blit(
        get_subtitle_font().render(text.LEVEL_SELECTION_PROMPT.upper(), True, Color.SUBTITLE_TEXT.rgb),
        (50, 260)
    )

    # Add level buttons
    for button in buttons:
        draw_button(screen, button, Color.ENERGY_LOW.rgb, Color.ENERGY_HIGH.rgb)

    pygame.display.flip()


# =========================
# Level
# =========================

def level(screen, level, status=GameState.LEVEL):
    # Draw background
    bg_color = Color.BG.rgb
    match status:
        case GameState.WIN:
            bg_color = Color.BG_WIN.rgb
        case GameState.LOSE:
            bg_color = Color.BG_LOSE.rgb
    
    screen.fill(bg_color)
    
    # Draw level
    for y, row in enumerate(level.tiles):
        for x, char in enumerate(row):
            match Tile.from_char(char):
                # Walls
                case Tile.WALL:
                    wall_color = Color.WALL.rgb
                    match status:
                        case GameState.WIN:
                            wall_color = Color.WALL_WIN.rgb
                        case GameState.LOSE:
                            wall_color = Color.WALL_LOSE.rgb
                    draw_rect(screen, x, y, wall_color)

                # Goal area
                case Tile.GOAL:
                    draw_rect(screen, x, y, Color.GOAL.rgb)

                # Observation block
                case Tile.OBSERVE:
                    draw_pattern(screen, x, y, [
                        [0,0,0],
                        [0,1,0],
                        [0,0,0]
                    ], Color.OBSERVE.rgb)
                    
                # Killer block
                case Tile.KILL:
                    draw_rect(screen, x, y, Color.KILL.rgb)

                # Filter doors
                case Tile.DOOR_LOW:
                    draw_pad(screen, x, y, Color.DOOR_LOW.rgb)
                case Tile.DOOR_HIGH:
                    draw_pad(screen, x, y, Color.DOOR_HIGH.rgb)
                
                # Low-energy plate
                case Tile.PLATE_LOW:  
                    draw_pattern(screen, x, y, [
                        [1,0,1],
                        [0,1,0],
                        [1,0,1]
                    ], Color.PLATE_LOW.rgb)
                
                # High-energy plate
                case Tile.PLATE_HIGH:
                    draw_pattern(screen, x, y, [
                        [0,1,0],
                        [1,1,1],
                        [0,1,0]
                    ], Color.PLATE_HIGH.rgb)
                    
                # Low-linked door
                case Tile.LINKED_WALL_LOW:  
                    if  level.plate_pressed(Energy.LOW) or level.tile_occupied(x,y):
                        draw_rect(screen, x, y, Color.LINKED_WALL_OPEN.rgb)
                    else:
                        draw_rect(screen, x, y, Color.LINKED_WALL_LOW.rgb)

                # High-linked door
                case Tile.LINKED_WALL_HIGH:  
                    if level.plate_pressed(Energy.HIGH) or level.tile_occupied(x,y):
                        draw_rect(screen, x, y, Color.LINKED_WALL_OPEN.rgb)
                    else:
                        draw_rect(screen, x, y, Color.LINKED_WALL_HIGH.rgb)
            
    # Draw the player
    draw_qube(screen, level.qube)

    # Darker background for comments (should stay even after win/lose)
    draw_shadow(screen, pygame.Rect(0, HEIGHT - COMMENT_HEIGHT, WIDTH, COMMENT_HEIGHT))

    if status == GameState.LEVEL: 
        # Add the level comments
        draw_multiline(
            screen,
            level.comments,
            (20, HEIGHT - COMMENT_HEIGHT + 10),
            get_subtitle_font(),
            Color.SUBTITLE_TEXT.rgb,
            level.color
        )

        # Update the frame (it's here because win and lose screens need more details before flip)
        pygame.display.flip()

# Level end screen
def end(screen, buttons, state):
    for button in buttons:
            draw_button(screen, button, Color.TITLE_TEXT.rgb, with_shadow=True)
    
    # Win message
    draw_shadow(screen, pygame.Rect(0, 0, WIDTH, 150))
    button_text = text.CONGRATS.upper() if state == GameState.WIN else text.GAME_OVER.upper()
    screen.blit(
        get_title_font().render(button_text, True, Color.TITLE_TEXT.rgb),
        (60, 60)
    )

    pygame.display.flip()


# =========================
# Draw UI elements
# =========================

# Draw multiline text (default doesn't support multiple lines)
def draw_multiline(screen, text, pos, font, color, gradient_color):
    base_color = color
    x, y = pos

    for line in text.split("\n"):
        base_color = blend(base_color, gradient_color, 0.1)
        surf = font.render("# " + line, True, base_color)
        screen.blit(surf, (x, y))
        y += font.get_height() + 5

# Draw a button    
def draw_button(screen, button, color, hovered_color=None, with_shadow=False):
    text_color = color

    # Add a shadow
    if with_shadow: draw_shadow(screen, button.rect)

    # Change button if it is hovered
    if  button.is_hovered(pygame.mouse.get_pos()): 
        pygame.draw.rect(screen, Color.TITLE_TEXT.rgb, button.rect, 2)
        if hovered_color != None: text_color = hovered_color

    # Add the text
    screen.blit(
        get_subtitle_font().render("--- " + button.text, True, text_color), 
        button.position(10, 10)
    )

# Draw a semi-transparent background
def draw_shadow(screen, rect):
    shadow = pygame.Surface(rect.size, pygame.SRCALPHA)
    shadow.fill(Color.SHADOW.value)  # RGBA (alpha = transparency)
    screen.blit(shadow, rect.topleft)

# =========================
# Draw shapes
# =========================

# Draw a horizontal line
def draw_line_break(screen, x, y, length, color):
    pygame.draw.line(screen, color, (y, x), (y+length, x), 2)

# Draw a rectangle
def draw_rect(screen, x, y, color):
    shape = (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, color, shape)

# Draw a pad
def draw_pad(screen, x, y, color):
    shape = (x*TILE_SIZE+10, y*TILE_SIZE+10, TILE_SIZE-20, TILE_SIZE-20)
    pygame.draw.rect(screen, color, shape)

# Draw a 3x3 pattern in a tile
def draw_pattern(screen, x, y, pattern, color):
    sub = TILE_SIZE // 3
    for rowi in range(3):
        for coli in range(3):
            if pattern[rowi][coli]:
                pygame.draw.rect(screen, color, (x*TILE_SIZE+coli*sub, y*TILE_SIZE+rowi*sub, sub, sub))


# =========================
# Draw the player
# =========================

def draw_qube(screen, qube):
    if qube.dead(): return
    
    for cube in qube.cubes:
        x, y = cube.get_position()
        
        if not qube.superposed():
            draw_rect(screen, x, y, Color.from_energy(cube.energy))
        else:
            if cube.energy.low():
                draw_pattern(screen, x, y, [
                    [0,1,0],
                    [1,0,1],
                    [0,1,0]
                ], Color.ENERGY_LOW.rgb)
            else:
                draw_pattern(screen, x, y, [
                    [1,0,1],
                    [0,0,0],
                    [1,0,1]
                ], Color.ENERGY_HIGH.rgb)
            
            # Visualize Z-choice in top-left corner
            screen.blit(
                get_default_font().render(f"Z choice {'HIGH' if qube.z.high() else 'LOW'}", True, Color.from_energy(qube.z)), 
                (10, 10)
            )

# =========================
# Helpers
# =========================

# make sentence case work
def sentence_case(text):
    text = text.lower()

    sentences = re.split(r'([.!?]\s*)', text)  # keep punctuation
    result = ""

    for i in range(0, len(sentences), 2):
        chunk = sentences[i]
        punct = sentences[i+1] if i+1 < len(sentences) else ""

        chunk = chunk.strip().capitalize()
        result += chunk + punct

    return result

# dynamically change the color (used to make gradients)
def blend(color, target, factor):
    r1, g1, b1 = color
    r2, g2, b2 = target

    return (
        int(r1 + (r2 - r1) * factor),
        int(g1 + (g2 - g1) * factor),
        int(b1 + (b2 - b1) * factor),
    )