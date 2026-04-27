from enum import Enum
import copy

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
            "#####################",
            "#....H..##..D..DQ..G#",
            "#....H..Q#..#..DQ..G#",
            "#....H......#..DQ..G#",
            "#.S..################",
            "#....L...E.##..PE..G#",
            "#....L.###.P#..PE..G#",
            "#....L.###.....PE..G#",
            "#####################",
        ],
        "comments": {
            "text": (
                "This level seems impossible, huh.\n"
                "There's plates that open walls - you gotta stand on them.\n"
                "Just make sure that your energy/shape mathes the plate.\n"
                "If you apply Hadamard gate to a qubit, it exists in both states.\n"
                "Try pressing [H], now you're in superosition."
            ),
            "color": (0, 0, 255),
        },
    },
    "observation": {
        "layout": [
            "####################",
            "#.......K##OO.E...G#",
            "#..S..O.K.....E...G#",
            "#.....O....OO.E...G#",
            "##HHH###############",
            "##...#O.....O....###",
            "##........K...Q..###",
            "##KKK#....K.O....###",
            "####################",
        ],
        "comments": {
            "text": (
                "Observation collapses superposition into one state.\n"
                "It is random — you cannot choose the result.\n"
                "White dots, red cubes, and green cubes observe you.\n"
                "After observation you may end up killed or miss the goal.\n"
                "So I would recommend pressing [H] before finish."
            ),
            "color": (255, 255, 0),
        },
    },
    "interference": {
        "layout": [
            "######################",
            "#KPPPPL.S..D...L...###",
            "#######....D...L...###",
            "#######..###...##EE###",
            "#######..###KK.##...G#",
            "###...D..###...##...G#",
            "#PH...D..###.KK#######",
            "###...D..###.....Q####",
            "######################",
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
    "bonus": {
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
                "Now you know how to operate the qube.\n"
                "You also know the basic quantum mechanics of the qubit.\n"
                "This is one more bonus level.\n"
                "Have fun!\n"
                ":D"
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
        return Tile.from_char(self.tiles[y][x])
    
    # Get the tile below a cube
    def get_cube_tile(self, cube):
        x, y = cube.get_position()
        return Tile.from_char(self.tiles[y][x])
    
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

    def plate_pressed(self, energy, qube=None):
        if qube == None: qube = self.qube
        if qube.dead() or not qube.superposed(): return False

        plates = self.low_plates if energy.low() else self.high_plates
        cube = qube.get_position(energy)

        return cube in plates

    # =========================
    # Tile interactions
    # =========================

    # Influence the player state depending on the tile they have stepped in
    def update(self, dx, dy):
        sim_qube = copy.deepcopy(self.qube)
        sim_qube.move(dx, dy)

        # Check if move is possible and update player position(s)
        for cube, sim_cube in zip(self.qube.cubes, sim_qube.cubes):
            tile = self.get_cube_tile(sim_cube)
            blocked = (
                tile == Tile.WALL or
                (tile == Tile.DOOR_LOW and sim_cube.energy != Energy.LOW) or
                (tile == Tile.DOOR_HIGH and sim_cube.energy != Energy.HIGH) or
                # Check both current position and simulated movement for plate state evaluation
                (tile == Tile.LINKED_WALL_LOW and not self.plate_pressed(Energy.LOW, sim_qube) and not self.plate_pressed(Energy.LOW, self.qube)) or
                (tile == Tile.LINKED_WALL_HIGH and not self.plate_pressed(Energy.HIGH, sim_qube) and not self.plate_pressed(Energy.HIGH, self.qube))
            )
            if not blocked: cube.move(dx, dy)

        state = GameState.LEVEL

        # Check collisions and update game state
        for cube in self.qube.cubes:
            match self.get_cube_tile(cube):
                case Tile.KILL:
                    self.qube.kill()
                    if self.qube.dead(): state = GameState.LOSE
                    break
                case Tile.OBSERVE:
                    self.qube.observe()
                    break
                case Tile.GOAL:
                    self.qube.kill()

                    # GOAL block is killing (removing) qube/twin
                    # if block gets removed it counts as winning
                    # if a twin "survives" then the win doesn't happen
                    if self.qube.dead(): state = GameState.WIN

        return state
    
    # =========================
    # Other
    # =========================

    # Create button list objects from LEVELS variable
    # x, y is the position of the button list
    @classmethod
    def buttonify(self, x, y):
        return Button.from_dict(LEVELS, x, y)