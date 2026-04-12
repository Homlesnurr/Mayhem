import pygame
import config
from src.visuals import SpriteBase, ImageLoader


class SpaceshipSprite(SpriteBase):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image: pygame.Surface = ImageLoader('assets\\rocket_ship_blue.png', scale=0.7)
        self.image.rect.center = (pos)
    
    def rotate_sprite(self, dtheta):
        pygame.transform.rotate(self.image, dtheta)

    def set_pos(self, pos):
        self.image.rect.center = (pos)

    def update(self, pos):
        self.set_pos(pos)
