import pygame
from src.visuals import SpriteBase
import config

class ImageLoader(SpriteBase):
    def __init__(self,
                 image_path: str = None,
                 size: tuple[int, int] = None,
                 scale: int = None):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path)
            if size:
                self.image = pygame.transform.smoothscale(self.image, size)
            elif scale:
                self.image = pygame.transform.smoothscale_by(self.image, scale)
            self.rect = self.image.get_rect()
        except:
            raise SyntaxError(f'Couldnt load image: {image_path}')
    
    def update(self):
        pass