import pygame
from static.settings import BUTTON_WIDTH, BUTTON_HEIGHT

class Button:
    def __init__(self, x, y, text):
        self.text = text
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # x, y are for adjustments/offsets
    def position(self, x, y):
        return (self.rect.x + x, self.rect.y + y)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    # x, y is the position of the list itself
    @classmethod
    def from_dict(self, dict, x, y):
        buttons = []
        offset = 0
        for name, _ in dict.items():
            buttons.append(Button(x, y + offset, name))
            offset += BUTTON_HEIGHT
        return buttons