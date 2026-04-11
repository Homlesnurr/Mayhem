import pygame


class InputHandler:
    '''
    InputHandler handles all the inputs from the user. This is to prevent bloating the main game loop.
    '''
    def __init__(self):
        self.running = True
        self.fullscreen = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if self.fullscreen:
                    pygame.display.set_mode((1920, 1080))
                    pygame.display.set_mode((800, 600))
                else:
                    pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                self.fullscreen = not self.fullscreen