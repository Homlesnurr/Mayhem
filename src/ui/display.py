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

        self.set_scene(self.main_menu)

    def open_game(self):
        self.set_scene(self.game_screen)

    def set_scene(self, scene: object):
        self.active_scene = scene

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