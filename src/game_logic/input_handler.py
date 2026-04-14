import pygame
from src.ui import Display
from scenes import GameScreen, MainMenu

class InputHandler:
    '''
    InputHandler handles all the inputs from the user. This is to prevent bloating the main game loop.
    '''
    def __init__(self, display: Display):
        self.display = display
        self.running = True

    def player_input(self,  pressed: pygame.key.ScancodeWrapper, clicked: int = None):
        ships = self.display.active_scene.physics_engine.spaceships
        for ship in ships:
            if ship.player_tag == 'Player 1':
                if pressed[pygame.K_w]     or clicked == pygame.K_w:       ship.thrust()
                if pressed[pygame.K_a]     or clicked == pygame.K_a:       ship.rotate('left')
                if pressed[pygame.K_d]     or clicked == pygame.K_d:       ship.rotate('right')
                if pressed[pygame.K_s]     or clicked == pygame.K_s:       ship.fire_bullet(self.display.active_scene.physics_engine)

            if ship.player_tag == 'Player 2':
                if pressed[pygame.K_UP]    or clicked == pygame.K_UP:      ship.thrust()
                if pressed[pygame.K_LEFT]  or clicked == pygame.K_LEFT:    ship.rotate('left')
                if pressed[pygame.K_RIGHT] or clicked == pygame.K_RIGHT:   ship.rotate('right')
                if pressed[pygame.K_DOWN]  or clicked == pygame.K_DOWN:    ship.fire_bullet(self.display.active_scene.physics_engine)


    def handle_events(self):
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)
        pressed_keys = pygame.key.get_pressed()
        if isinstance(self.display.active_scene, GameScreen):
            self.player_input(pressed_keys)
        hovered_sprites = pygame.sprite.spritecollide(mouse_sprite, self.display.active_scene.objects, False)
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