import random
from enum import Enum

class Energy(Enum):
    LOW = 0
    HIGH = 1

    # =========================
    # Utilities for render
    # ========================= 

    def flip(self):
        return Energy.HIGH if self == Energy.LOW else Energy.LOW
    
    def low(self):
        return self == Energy.LOW
    
    def high(self):
        return self == Energy.HIGH

# An instance of the cube (can be just player if there's no superposition/splitting)
class Cube:
    def __init__(self, energy, x, y):
        self.energy = energy
        self.x = x
        self.y = y

    def move(self, level, dx, dy):
        x, y = self.x + dx, self.y + dy

        if level.can_move(self.energy, x, y):
            self.x = x
            self.y = y

    def get_position(self):
        return self.x, self.y

# A quantum cube that can go into superposition of two component cubes (split)
class Qube:
    def __init__(self, x, y):
        self.cubes = [Cube(Energy.LOW, x, y)]   # The component cubes for superposition, in case of single instance it's just the player
        self.z = Energy.LOW                     # The current Z choise

    def move(self, level, dx, dy):
        for cube in self.cubes:
            cube.move(level, dx, dy)

    def kill(self):
        self.cubes = []

    # =========================
    # Quantum behaviour
    # ========================= 

    # Simulates Hadamard gate application - superposition and interference
    def hadamard(self):
        if self.dead(): return
        
        if self.superposed():
            # Compress two players into one (represents interference which is constructive/destructive for low/high energy)
            for cube in self.cubes:
                if cube.energy == self.z:
                    self.cubes = [Cube(self.z, cube.x,cube.y)]
                    self.z = Energy.LOW     # for consistency
                    break
        else:
            # Split player into two instances (represents the superposition of high/low energy states)
            cube = self.cubes[0]
            self.cubes = [Cube(Energy.LOW, cube.x, cube.y), Cube(Energy.HIGH, cube.x, cube.y)]
    
    # Choose one player instance 50/50 (represents the observation)
    def observe(self):
        if not self.superposed(): return

        new_energy = random.choice([Energy.LOW, Energy.HIGH])
        x, y = self.get_position(new_energy)
        
        self.cubes = [Cube(new_energy, x, y)]
        self.z = Energy.LOW     # for consistency

    # =========================
    # Setters
    # =========================

    def toggle_energy(self):
        if not self.superposed() and not self.dead():
            self.cubes[0].energy = self.cubes[0].energy.flip()

    def toggle_z(self):
        if self.superposed() and not self.dead():
            self.z = self.z.flip()

    # =========================
    # Getters
    # =========================

    # Get player position(s)
    def get_position(self, energy):
        if self.dead(): return

        if not self.superposed():
            return self.cubes[0].x, self.cubes[0].y
        else:
            return self.cubes[energy.value].get_position()
        
    # Get the energy of the singular qube (not in superposition)
    def get_energy(self):
        if self.dead() or self.superposed(): return

        return self.cubes[0].energy

    # =========================
    # Checks
    # =========================

    def dead(self):
        return not self.cubes
    
    # Check if the player is in superposition
    def superposed(self):
        return len(self.cubes) == 2