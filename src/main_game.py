import pygame
from .game_logic.input_handler import InputHandler
from .visuals.display import Display
import scenes
import config

class MainGame:
    '''
    Main game class where the game loop is run. All the game logic is executed in this run-loop.
    '''
    pygame.init()
    FPS = config.FPS
    display = Display()
    input_handler = InputHandler(display)
    clock = pygame.time.Clock()

    def __init__(self):
        self.running = True

    def run(self):
        while self.input_handler.running:
            self.input_handler.handle_events()
            self.display.process()
            self.clock.tick(self.FPS)