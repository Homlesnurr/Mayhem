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
        '''
        Handles all inputs the player can do.
        
        We use both pygame.key.get_pressed(), and pygame.event.get(), because pygame.key.get_pressed() will always have 1 frame of input lag,
        something that pygame.event.get() does not have.
        '''
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
        '''
        Handles all events the user can do
        '''
        # Makes a 1x1 rect at the cursor location, so we can easily check if the cursor is hovering any sprites in the all_sprites group.
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)
        pressed_keys = pygame.key.get_pressed()

        # Handles player input only if the active scene is the game screen.
        if isinstance(self.display.active_scene, GameScreen):
            self.player_input(pressed_keys)
        
        # Stores all hovered sprites
        hovered_sprites = pygame.sprite.spritecollide(mouse_sprite, self.display.active_scene.all_sprites, False)
        for sprite in hovered_sprites:
            if hasattr(sprite, 'hoverable'): sprite.hover()
        
        # Handles general keyboard and click events
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