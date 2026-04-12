import pygame
import config
from src.visuals import SpriteBase, ImageLoader


class SpaceshipSprite(SpriteBase):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image: pygame.Surface = ImageLoader('assets\\rocket_ship_blue.png', scale=0.7)
        self.image.rect.center = (pos)
    
    def rotate_sprite(self, angle):
        pygame.transform.rotate(self.image, angle)

    def set_pos(self, pos):
        self.image.rect.center = (pos)

    def update(self, pos: list[int, int] | tuple[int, int] = None, angle: int | float = None):
        if angle:
            self.rotate_sprite(angle)
        if pos:
            self.set_pos(pos)
