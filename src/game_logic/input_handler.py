import pygame


class InputHandler:
    '''
    InputHandler handles all the inputs from the user. This is to prevent bloating the main game loop.
    '''
    def __init__(self):
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False