import pygame
import config
from scenes import SceneBase
from src.visuals import RoundedButton, ImageLoader, Display

class MainMenu(SceneBase):
    '''
    Class containing everything pertaining to the main menu.
    '''
    def __init__(self, display: Display):
        super().__init__()
        self.button_width       = config.screen_dimensions[0] // 3
        self.button_height      = config.screen_dimensions[1] // 5
        background = ImageLoader('assets\\faker.jpg', config.screen_dimensions)
        play_button    = RoundedButton(self.screen_center_x,
                                       self.screen_center_y - self.button_height - self.screen_center_y*0.3,
                                       self.button_width,
                                       self.button_height,
                                       (50,50,200),
                                       'Play',
                                       display.open_game)
        settings_button= RoundedButton(self.screen_center_x,
                                       self.screen_center_y + self.button_height - self.screen_center_y*0.3,
                                       self.button_width,
                                       self.button_height,
                                       (50,50,200),
                                       'Settings',
                                       display.open_settings)
        self.add(background)
        self.add(play_button)
        self.add(settings_button)

    def add(self, element):
        self.objects.add(element)

    def remove(self, element):
        self.objects.remove(element)