import pygame
from .game_logic.input_handler import InputHandler


class MainGame:
    '''
    Main game class where the game loop is run. All the game logic is executed in this run-loop.
    '''
    FPS = 60
    RESOLUTION = (800, 600)
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.input_handler = InputHandler()
        self.clock = pygame.time.Clock()
        self.running = True


    def run(self):
        while self.input_handler.running:
            self.input_handler.handle_events()
            self.clock.tick(self.FPS)
            
            self.screen.fill((67, 67, 67))
            pygame.display.flip()