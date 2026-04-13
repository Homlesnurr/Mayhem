import pygame
from numpy.typing import NDArray
import config
from src.ui import SpriteBase, ImageLoader


class BulletSprite(SpriteBase):
    def __init__(self, pos: list[int, int], angle: float):
        super().__init__()
        self.bullet_surf = pygame.Surface((6, 20), pygame.SRCALPHA)
        self.pos = pos
        self.image_base = self.bullet_surf
        self.image = self.image_base.copy()
        self.rect = pygame.Surface.fill(self.bullet_surf, (255, 0, 0))
        self.rect.center = self.pos
        self.rotate_sprite(angle)
    
    def rotate_sprite(self, angle):
        self.image = pygame.transform.rotate(self.image_base, angle)
        self.rect = self.image.get_rect(center = self.pos)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = (pos)

    def update(self,
               pos: list[int, int] = [config.screen_dimensions[0] // 2, config.screen_dimensions[1] // 2],
               angle: int | float = 0):
        self.rotate_sprite(angle)
        self.set_pos(pos)
