import pygame
import config
from src.ui import SpriteBase, ImageLoader


class BulletSprite(SpriteBase):
    def __init__(self, pos: tuple[int, int], angle: float):
        super().__init__()
        self.bullet_surf = pygame.Surface((10, 2), pygame.SRCALPHA)
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
               pos: list[int, int] | tuple[int, int] = None,
               angle: int | float = None):
        if angle:
            self.rotate_sprite(angle)
        if pos:
            self.set_pos(pos)
