import pygame
import config

class ImageLoader(pygame.sprite.Sprite):
    def __init__(self, image_path: str = None):
        super().__init__()
        self.dimensions = config.screen_dimensions
        try:
            self.image = pygame.transform.smoothscale(pygame.image.load(image_path), config.screen_dimensions)
            self.rect = self.image.get_rect()
        except:
            print(f'Couldnt load image: {image_path}')
    
    def update(self):
        pass