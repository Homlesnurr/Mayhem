from __future__ import annotations
import pygame
from src.visuals import SpaceshipSprite
#temp const
dt = 0.01
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
        # update velocity
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        #max velocity
        self.velocity[0] = max(-5, min(5, self.velocity[0]))
        self.velocity[1] = max(-5, min(5, self.velocity[1]))

        # update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def gravity(self):
        self.acceleration[1] += 9.81 * dt

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
        
        #apply gravity
        self.gravity()
        
        #rotation
        if self.rotate_left:
            self.angle = (self.angle - rotation_speed * dt) % 360
        if self.rotate_right:
            self.angle = (self.angle + rotation_speed * dt) % 360
        
        #thrust
        if self.thrusting and self.fuel > 0:
            pass

    
class Bullet(CorePhysics):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self):
        pass