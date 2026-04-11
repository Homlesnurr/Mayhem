import pygame
import config
from scenes.scene_base import SceneBase
from src.visuals import RoundedButton, ImageLoader, Display

class GameScreen(SceneBase):
    '''
    Class containing everything pertaining to the main menu.
    '''
    def __init__(self, display: Display):
        super().__init__()
        background = ImageLoader('assets\\temp_background.jpeg')
        self.add(background)


    def add(self, element):
        self.objects.add(element)

    def remove(self, element):
        self.objects.remove(element)