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

    def handle_events(self):
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)
        pressed_keys = pygame.key.get_pressed()
        if isinstance(self.display.active_scene, GameScreen):
            ships: list[Spaceship] = self.display.active_scene.physics_engine.spaceships

            if pressed_keys[pygame.K_w]:
                for ship in ships:
                    if ship.player_tag == 'Player 1':
                        ship.thrust()
                
            if pressed_keys[pygame.K_a]:
                for ship in ships:
                    if ship.player_tag == 'Player 1':
                        ship.rotate('left')
            
            if pressed_keys[pygame.K_s]:
                for ship in ships:
                    if ship.player_tag == 'Player 1':
                        ship.fire_bullet()
                        self.display.active_scene.physics_engine.bullets.add(ship.bullet)

            if pressed_keys[pygame.K_d]:
                for ship in ships:
                    if ship.player_tag == 'Player 1':
                        ship.rotate('right')

            if pressed_keys[pygame.K_UP]:
                for ship in ships:
                    if ship.player_tag == 'Player 2':
                        ship.thrust()

            if pressed_keys[pygame.K_LEFT]:
                for ship in ships:
                    if ship.player_tag == 'Player 2':
                        ship.rotate('left')
                        
            if pressed_keys[pygame.K_DOWN]:
                for ship in ships:
                    if ship.player_tag == 'Player 2':
                        ship.fire_bullet()
                        self.display.active_scene.physics_engine.bullets.add(ship.bullet)

            if pressed_keys[pygame.K_RIGHT]:
                for ship in ships:
                    if ship.player_tag == 'Player 2':
                        ship.rotate('right')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.display.set_scene(self.display.main_menu)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                hovered_sprites = pygame.sprite.spritecollide(mouse_sprite, self.display.active_scene.objects, False)
                for sprite in hovered_sprites:
                    try:
                        sprite.click()
                    except:
                        pass