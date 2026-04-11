import pygame
from abc import ABC, abstractmethod

class button(pygame.sprite.Sprite, ABC):
    '''
    Abstract button class that all buttons will inherit from. This is to prevent code duplication and to make it easier to create new buttons.
    '''
    def __init__(self):
        pass
        

    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def hover(self):
        pass

    @abstractmethod
    def leave(self):
        pass

    @abstractmethod
    def draw(self):
        pass