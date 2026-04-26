"""
Module for handling all user inputs. This is where we do the keypress checks and mouse clicks. Authors: Abel Yttervik, Vincent Anuwat Van Duin
"""

import pygame
from src.ui import Display
from scenes import GameScreen, MainMenu

class InputHandler:
    '''
    InputHandler handles all the inputs from the user. This is to prevent bloating the main game loop. Authors: Abel Yttervik, Vincent Anuwat Van Duin.
    '''
    def __init__(self, display: Display):
        self.display = display
        self.running = True

    def player_input(self,  pressed: pygame.key.ScancodeWrapper, clicked: int = None):
        players = self.display.active_scene.players

        if pressed[pygame.K_w]     or clicked == pygame.K_w:       players['player_1'].ship.thrust()
        if pressed[pygame.K_a]     or clicked == pygame.K_a:       players['player_1'].ship.rotate('left')
        if pressed[pygame.K_d]     or clicked == pygame.K_d:       players['player_1'].ship.rotate('right')
        if pressed[pygame.K_s]     or clicked == pygame.K_s:       players['player_1'].ship.fire_bullet(self.display.active_scene.physics_engine)

        if pressed[pygame.K_UP]    or clicked == pygame.K_UP:      players['player_2'].ship.thrust()
        if pressed[pygame.K_LEFT]  or clicked == pygame.K_LEFT:    players['player_2'].ship.rotate('left')
        if pressed[pygame.K_RIGHT] or clicked == pygame.K_RIGHT:   players['player_2'].ship.rotate('right')
        if pressed[pygame.K_DOWN]  or clicked == pygame.K_DOWN:    players['player_2'].ship.fire_bullet(self.display.active_scene.physics_engine)


    def handle_events(self):
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)
        pressed_keys = pygame.key.get_pressed()
        if isinstance(self.display.active_scene, GameScreen):
            self.player_input(pressed_keys)
        hovered_sprites = pygame.sprite.spritecollide(mouse_sprite, self.display.active_scene.all_sprites, False)
        for sprite in hovered_sprites:
            if hasattr(sprite, 'hoverable'): sprite.hover()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if isinstance(self.display.active_scene, MainMenu):
                        self.running = False
                    self.display.set_scene(self.display.main_menu)
                if isinstance(self.display.active_scene, GameScreen):
                    self.player_input(pressed_keys, event.key)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sprite in hovered_sprites:
                    if hasattr(sprite, 'click_func'): sprite.click()