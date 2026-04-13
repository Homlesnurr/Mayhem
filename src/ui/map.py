import pygame
import config
from src.ui import SpriteBase, ImageLoader

class Map(SpriteBase):
    def __init__(self):
        super().__init__()
        border = 10 #7
        width = config.screen_dimensions[0]
        height = config.screen_dimensions[1]
        map_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        background = ImageLoader('assets\\temp_background.jpeg', (width, height))
        map_surface.blit(background.image, (0,0))
        # Horizontal border
        pygame.draw.rect(map_surface, (167,167,167), (0, 0, width,border))
        pygame.draw.rect(map_surface, (167,167,167), (0, height-border, width, height))
        # Veritcal border
        pygame.draw.rect(map_surface, (167,167,167), (0, 0, border,height))
        pygame.draw.rect(map_surface, (167,167,167), (width-border, 0, width, height))
        
        self.image = map_surface
        self.rect = map_surface.get_rect()

    def update(self):
        pass