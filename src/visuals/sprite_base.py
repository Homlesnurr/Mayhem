import pygame
from abc import ABC, abstractmethod

class SpriteBase(pygame.sprite.Sprite(), ABC):
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def set_image(self):
        pass

    @abstractmethod
    def set_rect(self):
        pass