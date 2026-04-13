import pygame
from abc import ABC, abstractmethod

class SpriteBase(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self):
        pass