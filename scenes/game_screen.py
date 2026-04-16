import pygame
import config
from scenes import SceneBase
from src.ui import RoundedButton, ImageLoader, Display, SpaceshipSprite, Map
from src.game_logic import Spaceship, PhysicsEngine, Obstacle, Fueldrop

class GameScreen(SceneBase):
    '''
    Class containing everything pertaining to the main menu.
    '''
    def __init__(self, display: Display):
        super().__init__()
        self.physics_engine = PhysicsEngine()
        width = config.screen_dimensions[0]
        height = config.screen_dimensions[1]
        background = ImageLoader('assets\\temp_background.jpeg', (width, height))
        self.map = Map()
        self.obstacle = Obstacle(600, 300)
        self.player1 = Spaceship('Player 1')
        self.player2 = Spaceship('Player 2')
        self.add(background)
        self.physics_engine.add_solid(self.map)
        self.physics_engine.add_solid(self.obstacle)
        self.physics_engine.add_spaceship(self.player1)
        self.physics_engine.add_spaceship(self.player2)

    def add(self, element):
        self.objects.add(element)

    def remove(self, element):
        self.objects.remove(element)

