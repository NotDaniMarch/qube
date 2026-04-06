LEVELS = {
    "basics": [
            "###################",
            "#K.........KKK....#",
            "#K................#",
            "#K......K.........#",
            "####HHH######LLL###",
            "#........##.......#",
            "#........##.......#",
            "#..S.....##...G...#",
            "#........##########",
            "###################",
        ],
    "superposition": [
            "####################",
            "#....H...K.....K...#",
            "#....H...K..K.....Q#",
            "#....#......K..K...#",
            "#.S..###############",
            "#.............E...G#",
            "#.............E...G#",
            "####################",
        ],
    "interference": [
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
    "observation": [
            "####################",
            "##Q###.............#",
            "#.S..D.............#",
            "#....D.............#",
            "#LLL################",
            "#...E..............#",
            "#...#.P...O........#",
            "#...#..............#",
            "####################",
        ]
}

class Level:
    def __init__(self, level_name):
        self.tiles = LEVELS[level_name]

        # Get plate coordinates
        low_plates = []
        high_plates = []
        for y, row in enumerate(self.tiles):
            for x, c in enumerate(row):
                if c == "P":
                    low_plates.append((x, y))
                elif c == "Q":
                    high_plates.append((x, y))
            
        self.low_plates = low_plates
        self.high_plates = high_plates

    def getTileAt(self, y, x):
        return self.tiles[y][x]
    
    def find_start(self):
        for y, row in enumerate(self.tiles):
            for x, column in enumerate(row):
                if column == "S":
                    return x, y
    