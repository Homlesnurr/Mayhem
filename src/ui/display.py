from __future__ import annotations
from typing import Any
import pygame
import config

class Display:
    '''
    Display class handler everything we currently want to be displayed on the screen.
    
    Different screens/menus/scenes should be implemented elsewhere, and this class should be used for displaying them.
    '''
    def __init__(self):
        import scenes
        self.screen = pygame.display.set_mode(config.screen_dimensions)
        self.main_menu      = scenes.MainMenu(self)
        self.game_screen    = scenes.GameScreen()
        self.settings       = scenes.SettingsMenu(self)

        self.set_scene(self.main_menu)

    def open_game(self):
        self.set_scene(self.game_screen)

    def open_settings(self):
        self.set_scene(self.settings)

    def set_scene(self, scene: object):
        self.active_scene = scene
    
    def edit_config(self, variable: str, value: Any):
        '''
        DANGEROUS!!

        This function edits the config file. Wrong use will corrupt the config file, render the game unplayable.
        '''
        with open('config.py', 'r') as f:
            lines = f.readlines()
        with open('config.py', 'w') as f:
            for line in lines:
                if line.startswith(f'{variable}=') or line.startswith(f'{variable} ='):
                    f.write(f'{variable} = {repr(value)}\n')
                else:
                    f.write(line)

    def process(self):
        '''
        Updates and draws all pygame groups, for the active scene.
        '''
        import scenes
        if isinstance(self.active_scene, scenes.GameScreen):
            self.active_scene.all_sprites.update()
            self.active_scene.physics_engine.update()
            self.active_scene.all_sprites.draw(self.screen)
            self.active_scene.physics_engine.draw(self.screen)
        else:
            self.active_scene.all_sprites.update()
            self.active_scene.all_sprites.draw(self.screen)
        pygame.display.flip()