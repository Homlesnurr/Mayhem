import pygame
from src.visuals import Display
import config

class InputHandler:
    '''
    InputHandler handles all the inputs from the user. This is to prevent bloating the main game loop.
    '''
    def __init__(self, display: Display):
        self.display = display
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():                
            mouse_sprite = pygame.sprite.Sprite()
            mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)

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