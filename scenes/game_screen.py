""""
Module for handling the main game screen. This is where we add all the sprites and the physics engine. Authors: Abel Yttervik, Vincent Anuwat Van Duin
"""

import pygame
import config
from scenes import SceneBase
from src.ui import RoundedButton, ImageLoader, Display, SpaceshipSprite
from src.game_logic import Spaceship, PhysicsEngine, Obstacle, Fueldrop, Player

class GameScreen(SceneBase):
    '''
    Class containing everything pertaining to the main menu.
    '''
    def __init__(self):
        super().__init__()
        self.physics_engine = PhysicsEngine()
        width = config.screen_dimensions[0]
        height = config.screen_dimensions[1]
        background = ImageLoader('assets\\temp_background.jpeg', (width, height))
        self.obstacle = Obstacle(600, 300)
        self.fueldrop1 = Fueldrop(100, 550)
        self.fueldrop2 = Fueldrop(1100, 550)
        self.players = {
            'player_1': Player('Player 1'),
            'player_2': Player('Player 2')
        }
        self.add(background)
        self.make_map()
        self.physics_engine.add_player(self.players['player_1'])
        self.physics_engine.add_player(self.players['player_2'])
        self.physics_engine.add_solid(self.obstacle)
        self.physics_engine.add_solid(self.fueldrop1)
        self.physics_engine.add_solid(self.fueldrop2)

    def add(self, element):
        self.all_sprites.add(element)

    def remove(self, element):
        self.all_sprites.remove(element)

    def make_map(self):
        '''
        Creates single walls for the outline of the map. Collision checks are way faster, so when there are many bullets on screen, the game wont lag.
        '''
        top_wall = Wall((0,0), (config.screen_dimensions[0], config.border))
        bot_wall = Wall((0,config.screen_dimensions[1]-config.border), (config.screen_dimensions[0], config.screen_dimensions[1]))
        left_wall = Wall((0,0), (config.border, config.screen_dimensions[1]))
        right_wall = Wall((config.screen_dimensions[0]-config.border, 0), (config.screen_dimensions[0], config.screen_dimensions[1]))
        self.physics_engine.add_solid(top_wall)
        self.physics_engine.add_solid(bot_wall)
        self.physics_engine.add_solid(left_wall)
        self.physics_engine.add_solid(right_wall)

class Wall(pygame.sprite.Sprite):
    '''
    Creates a single wall surface at specified location.
    '''
    def __init__(self, top_left: tuple[int,int], bot_right: tuple[int,int]):
        super().__init__()
        self.surf = pygame.Surface((bot_right[0] - top_left[0], bot_right[1] - top_left[1]))
        self.rect = self.surf.fill((167,167,167))
        self.rect.topleft = top_left
        self.image = self.surf

    def update(self):
        pass