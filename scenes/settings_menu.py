import pygame
import config
from scenes import SceneBase
from src.ui import RoundedButton, ImageLoader, Display

class SettingsMenu(SceneBase):
    '''
    Class containing everything pertaining to the main menu.
    '''
    def __init__(self, display: Display):
        super().__init__()
        self.button_width       = config.screen_dimensions[0] // 3
        self.button_height      = config.screen_dimensions[1] // 5
        background = ImageLoader('assets\\faker.jpg', config.screen_dimensions)
        change_res_800_400    = RoundedButton(self.screen_center_x,
                                       self.screen_center_y - self.button_height - self.screen_center_y*0.3,
                                       self.button_width,
                                       self.button_height,
                                       (50,50,200),
                                       'res: 800 x 400',
                                       lambda: display.edit_config('screen_dimensions', (800, 400)))
        change_res_1600_920    = RoundedButton(self.screen_center_x,
                                       self.screen_center_y + self.button_height - self.screen_center_y*0.3,
                                       self.button_width,
                                       self.button_height,
                                       (50,50,200),
                                       'res: 1600 x 920',
                                       lambda: display.edit_config('screen_dimensions', (1600, 920)))
        self.add(background)
        self.add(change_res_800_400)
        self.add(change_res_1600_920)

    def add(self, element):
        self.all_sprites.add(element)

    def remove(self, element):
        self.all_sprites.remove(element)