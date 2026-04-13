import pygame
from src.ui import Display
from src.game_logic import Spaceship
from scenes import GameScreen
import config

class InputHandler:
    '''
    InputHandler handles all the inputs from the user. This is to prevent bloating the main game loop.
    '''
    def __init__(self, display: Display):
        self.display = display
        self.running = True

    def player_input(self, event: int | pygame.key.ScancodeWrapper):
        if event not in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
            if not isinstance(event, pygame.key.ScancodeWrapper):
                return
        ship1, ship2 = self.display.active_scene.physics_engine.spaceships
        if isinstance(event, pygame.key.ScancodeWrapper):
            if event[pygame.K_w]:       ship1.thrust()
            if event[pygame.K_a]:       ship1.rotate('left')
            if event[pygame.K_d]:       ship1.rotate('right')
            if event[pygame.K_s]:       ship1.fire_bullet(); self.display.active_scene.physics_engine.bullets.add(ship1.bullet)

            if event[pygame.K_UP]:      ship2.thrust()
            if event[pygame.K_LEFT]:    ship2.rotate('left')
            if event[pygame.K_RIGHT]:   ship2.rotate('right')
            if event[pygame.K_DOWN]:    ship2.fire_bullet(); self.display.active_scene.physics_engine.bullets.add(ship2.bullet)


        if isinstance(event, int):
            if event == pygame.K_w:     ship1.thrust()
            if event == pygame.K_a:     ship1.rotate('left')
            if event == pygame.K_d:     ship1.rotate('right')
            if event == pygame.K_s:     ship1.fire_bullet(); self.display.active_scene.physics_engine.bullets.add(ship1.bullet)

            if event == pygame.K_UP:    ship2.thrust()
            if event == pygame.K_LEFT:  ship2.rotate('left')
            if event == pygame.K_RIGHT: ship2.rotate('right')
            if event == pygame.K_DOWN:  ship2.fire_bullet(); self.display.active_scene.physics_engine.bullets.add(ship2.bullet)



    def handle_events(self):
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)
        pressed_keys = pygame.key.get_pressed()
        if isinstance(self.display.active_scene, GameScreen):
            self.player_input(pressed_keys)

        for event in pygame.event.get():
            if isinstance(self.display.active_scene, GameScreen): self.player_input(event)
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.display.set_scene(self.display.main_menu)
                if isinstance(self.display.active_scene, GameScreen): self.player_input(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                hovered_sprites = pygame.sprite.spritecollide(mouse_sprite, self.display.active_scene.objects, False)
                for sprite in hovered_sprites:
                    try:
                        sprite.click()
                    except:
                        pass