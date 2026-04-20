from enum import Enum

# Moved into it's own module because of a circular import
class GameState(Enum):
    MENU = 1
    LEVEL = 2
    QUIT = 3
    WIN = 4
    LOSE = 5