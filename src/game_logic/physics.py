from __future__ import annotations
import pygame
import config
from src.visuals import SpaceshipSprite, Map
#temp const
dt = 1/config.FPS
starting_fuel = 100
rotation_speed = 15

class CorePhysics(pygame.sprite.Sprite):

    """
    Base class for physics based objects: Velocity, acceleration and position updates. All objects that move inherits this.
    """

    def __init__(self, x, y):
        super().__init__()
        self.position = [x, y]
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0] 
        self.angle = 0.0

    def apply_physics(self):
        # Update gravity 
        self.gravity()

        # update velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        #max velocity
        self.velocity[0] = max(-500, min(500, self.velocity[0]))
        self.velocity[1] = max(-500, min(500, self.velocity[1]))

        # update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def gravity(self):
        self.acceleration[1] = 4

    def update(self):
        pass

class PhysicsEngine:
    def __init__(self):
        self.spaceships = []

    def add_spaceship(self, ship: Spaceship):
        self.spaceships.append(ship)
    
    def remove_spaceship(self, ship: Spaceship):
        self.spaceships.remove(ship)
    
    def update(self):
        for spaceship in self.spaceships:
            spaceship.update()

class Spaceship(CorePhysics):
    def __init__(self, x: int, y: int, player_tag: str):
        super().__init__(x, y)
        self.player_tag = player_tag
        self.fuel = starting_fuel

        self.thrusting = False
        self.rotate_left = False
        self.rotate_right = False

        self.sprite = SpaceshipSprite((x,y))


    def update(self):
        self.apply_physics()
        # rotation
        if self.rotate_left:
            self.angle = (self.angle - rotation_speed * dt) % 360
        if self.rotate_right:
            self.angle = (self.angle + rotation_speed * dt) % 360
        
        # thrust
        if self.thrusting and self.fuel > 0:
            pass

        # update sprite
        self.sprite.update(self.position)
    
    def __repr__(self):
        return (
            f'Spaceship:\t{self.player_tag}\n'
            f'Fuel:\t\t{self.fuel}\n'
            f'Position:\t{self.position}\n'
            f'Velocity:\t{self.velocity}\n'
            f'Acceleration:\t{self.acceleration}\n'
            f'Angle:\t\t{self.angle}\n'
            f'Thrusting:\t{self.thrusting}\n'
            f'Rotate L/R:\t{int(self.rotate_left)}/{int(self.rotate_right)}'
        )
    
class Bullet(CorePhysics):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self):
        pass