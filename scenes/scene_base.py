"""
Module for handling the base scene. This is where we define the base class for all scenes. Authors: Abel Yttervik, Vincent Anuwat Van Duin.
"""

from abc import ABC, abstractmethod
import config
import pygame

class SceneBase(ABC):
    '''
    Scene baseclass, ensuring a scene can add and remove sprites
    '''
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.screen_center_x = config.screen_dimensions[0] // 2
        self.screen_center_y = config.screen_dimensions[1] // 2

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def remove(self):
        pass

