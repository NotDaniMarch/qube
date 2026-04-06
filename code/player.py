from levels import Level

class Cube:
    def __init__(self, x, y, energy, superposed):
        self.x = x
        self.y = y
        self.energy = energy
        self.superposed = superposed
        self.alive = True
        
    def move(self, game, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        tile = game.level.getTileAt(ny,nx)

        # Wall
        if tile == "#":
            return

        # Energy doors
        if tile == "L" and self.energy != 0:
            return
        if tile == "H" and self.energy != 1:
            return

        # Linked doors
        if tile == "D" and not any(p.energy==0 and (p.x,p.y) in game.level.low_plates for p in game.players):
            return
        if tile == "E" and not any(p.energy==1 and (p.x,p.y) in game.level.high_plates for p in game.players):
            return

        self.x = nx
        self.y = ny