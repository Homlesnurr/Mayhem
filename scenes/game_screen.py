import pygame
import config
from scenes import SceneBase
from src.visuals import RoundedButton, ImageLoader, Display, SpaceshipSprite
from src.game_logic import Spaceship, PhysicsEngine

class GameScreen(SceneBase):
    '''
    Class containing everything pertaining to the main menu.
    '''
    def __init__(self, display: Display):
        super().__init__()
        background = ImageLoader('assets\\temp_background.jpeg', config.screen_dimensions)
        self.physics_engine = PhysicsEngine()
        self.spaceships = pygame.sprite.Group()
        self.player1 = Spaceship(x = 100,
                                 y = config.screen_dimensions[1] - 100,
                                 player_tag = 'Player 1')
        
        self.player2 = Spaceship(x = config.screen_dimensions[0] - 100,
                                 y = config.screen_dimensions[1] - 100,
                                 player_tag = 'Player 2')
        self.add(background)
        self.add_spaceship(self.player1)
        self.add_spaceship(self.player2)

    def add_spaceship(self, spaceship: Spaceship):
        self.spaceships.add(spaceship.sprite.image)
        self.physics_engine.add_spaceship(spaceship)


    def add(self, element):
        self.objects.add(element)

    def remove(self, element):
        self.objects.remove(element)