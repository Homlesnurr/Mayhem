import pygame
import config
from src.ui import SpriteBase, ImageLoader


class SpaceshipSprite(SpriteBase):
    def __init__(self, pos: list[int, int]):
        super().__init__()
        self.ship_sprite = ImageLoader('assets\\rocket_ship_blue.png', scale=0.7)
        self.pos = pos
        self.image = self.ship_sprite.image
        self.image_base = self.image.copy()
        self.rect = self.image.get_rect(center = self.pos)
    
    def rotate_sprite(self, angle):
        self.image = pygame.transform.rotate(self.image_base, angle)
        self.rect = self.image.get_rect(center = self.pos)
        

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = (pos)

    def update(self,
               pos: list[int, int] = [config.screen_dimensions[0] // 2, config.screen_dimensions[1] // 2],
               angle: int | float = 0):
        angle = self.rotate_sprite(angle)
        pos = self.set_pos(pos)
