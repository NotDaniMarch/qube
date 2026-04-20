from enum import Enum

from .player import *
from .button import Button
from classes.state import GameState

LEVELS = {
    "basics": {
        "layout": [
                "###################",
                "#K.........KKK....#",
                "#K................#",
                "#K......K.........#",
                "####HHH######LLL###",
                "#........##.......#",
                "#........##.......#",
                "#..S.....##..GGG..#",
                "#........##########",
                "###################",
        ],
        "comments": {
            "text": (
                "You are the quantum qubit. RED kills you - GREEN is you goal.\n"
                "The qubit has two basis states - high energy and low energy.\n"
                "Qubit state can be changed with quantum logic gates.\n"
                "The X gate flips your state, try and press [X].\n"
                "Now you can go through energy doors! :D"
            ),
            "color": (0,255,0),
        },
    },
    "superposition": {
        "layout": [
            "####################",
            "#....H...K.....K...#",
            "#....H...K..K.....Q#",
            "#....#......K..K...#",
            "#.S..###############",
            "#.............E...G#",
            "#.............E...G#",
            "####################",
        ],
        "comments": {
            "text": (
                "This level seems impossible, huh.\n"
                "There is high energy plate (+) that opens the wall.\n"
                "Jokes on you, level creator, we have the power of superosition!\n"
                "If you apply Hadamard gate to a qubit, it exists in both states.\n"
                "Try pressing [H], now you're in superosition of both states."
            ),
            "color": (0, 0, 255),
        },
    },
    "interference": {
        "layout": [
            "####################",
            "#KPPPPL.S..D...L...#",
            "#######....D...L...#",
            "#######..###...#EEE#",
            "#######..###KK.#...#",
            "###...D..###...#GGG#",
            "#PH...D..###.KK#####",
            "###...D..###.....Q##",
            "####################",
        ],
        "comments": {
            "text": (
                "Things start to get more convoluted now :0\n"
                "What happens if you press [H] twice?\n"
                "Try [H] [Z] [H], what about now? That's interference.\n"
                "In superposition, Z gate [Z] applies a hidden flip.\n"
                "It changes how states interfere - check top left."
            ),
            "color": (255,0,255),
        },
    },
    "observation": {
        "layout": [
            "#########################",
            "##Q#####KK......##..O..G#",
            "#......D...O.K..QD..O..G#",
            "#...O..D.O...K..##..O..G#",
            "#LLL#####################",
            "#.....E....OK#O.##..O..G#",
            "#..S..#.P#...#O.EP..O..G#",
            "#.....#..#.O....##..O..G#",
            "#########################",
        ],
        "comments": {
            "text": (
                "Those white dots are watching 0_0\n"
                "Observation collapses superposition into one state.\n"
                "It is random — you cannot choose the result.\n"
                "One state survives, the other disappears."
            ),
            "color": (255,0,0),
        },
    },
        
}

class Tile(Enum):
    BG = "."
    START = "S"
    WALL = "#"
    GOAL = "G"

    DOOR_LOW = "L"
    DOOR_HIGH = "H"
    KILL = "K"
    OBSERVE = "O"

    LINKED_WALL_LOW = "D"
    LINKED_WALL_HIGH = "E"
    PLATE_LOW = "P"
    PLATE_HIGH = "Q"

    # Utility to get tile enum from char
    @classmethod
    def from_char(cls, char):
        for tile in cls:
            if tile.value == char:
                return tile
        raise ValueError(f"Unknown tile: {char}")

class Level:
    def __init__(self, level_name):
        # Get level attributes
        self.name = level_name
        self.tiles = LEVELS[level_name]["layout"]
        self.comments = LEVELS[level_name]["comments"]["text"]
        self.color = LEVELS[level_name]["comments"]["color"]

        # Initialize the qube
        self.qube = None
        self.start()

        # The plate coordinates
        low_plates = []
        high_plates = []
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                tile = Tile.from_char(char)
                if tile == Tile.PLATE_LOW:
                    low_plates.append((x, y))
                elif tile == Tile.PLATE_HIGH:
                    high_plates.append((x, y))

        self.low_plates = low_plates
        self.high_plates = high_plates

    def start(self):
        # The player instance
        x, y = self.get_start_position()
        self.qube = Qube(x, y)
    
    # =========================
    # Getters
    # =========================

    # Get the tile type on x, y
    def get_tile(self, x, y):
        return Tile.from_char(self.tiles[x][y])
    
    # Get the start tile coordinates
    def get_start_position(self):
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                if Tile.from_char(char) == Tile.START:
                    return x, y
                
    @classmethod
    def get_next_level_name(cls, current_level_name):
        level_names = list(LEVELS.keys())
        i = level_names.index(current_level_name)
        if i + 1 < len(level_names):
            return level_names[i + 1]
        return None  # no next level

    # =========================
    # Checks
    # =========================

    # Check if a player is standing on a tile    
    def tile_occupied(self, x, y):
        return any(cube.x == x and cube.y == y for cube in self.qube.cubes)

    def plate_pressed(self, energy):
        if self.qube.dead() or not self.qube.superposed(): return False

        plates = self.low_plates if energy.low() else self.high_plates
        cube = self.qube.get_position(energy)

        return cube in plates

    # =========================
    # Tile interactions
    # =========================

    # Indicates if the level layout allows player to move
    def can_move(self, energy, y, x):
        tile = self.get_tile(x,y)
        
        # Wall
        if tile == Tile.WALL:
            return

        # Energy doors
        if tile == Tile.DOOR_LOW and energy != Energy.LOW:
            return
        if tile == Tile.DOOR_HIGH and energy != Energy.HIGH:
            return

        # Linked doors
        if tile == Tile.LINKED_WALL_LOW and not self.plate_pressed(Energy.LOW):
            return
        if tile == Tile.LINKED_WALL_HIGH and not self.plate_pressed(Energy.HIGH):
            return
        
        return True

    # Influence the player state depending on the tile they have stepped in
    def update_collisions(self):
        state = GameState.LEVEL

        for cube in self.qube.cubes:
            match self.get_tile(cube.y, cube.x):
                case Tile.KILL:
                    self.qube.kill()
                    state = GameState.LOSE
                    break
                case Tile.OBSERVE:
                    self.qube.observe()
                    break
                case Tile.GOAL:
                    self.qube.kill()
                    state = GameState.WIN

        return state
    
    # =========================
    # Other
    # =========================

    # Create button list objects from LEVELS variable
    # x, y is the position of the button list
    @classmethod
    def buttonify(self, x, y):
        return Button.from_dict(LEVELS, x, y)