from __future__ import annotations
import pygame
import numpy as np
import config
from src.ui import SpaceshipSprite, Map, BulletSprite
#temp const
dt = 1/config.FPS
starting_fuel = 100
rotation_speed = 2
consume_fuel_rate = 10
bullet_speed = 350


class PhysicsEngine:
    def __init__(self):
        self.spaceships = []
        self.bullets = pygame.sprite.Group()

    def add_spaceship(self, ship: Spaceship):
        self.spaceships.append(ship)
    
    def remove_spaceship(self, ship: Spaceship):
        self.spaceships.remove(ship)
    
    def update(self):
        # må legge til group update for alle objects senere
        self.bullets.update()
        for spaceship in self.spaceships:
            spaceship.update()

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

    def reset_accel(self):
        self.acceleration[1] = 5 # Gravity
        self.acceleration[0] = 0
        
    def update(self):
        pass


class Spaceship(CorePhysics):
    def __init__(self, x: int, y: int, player_tag: str):
        super().__init__(x, y)
        self.player_tag = player_tag
        self.fuel = starting_fuel
        self.shoot_cd = 0
        self.thrusting = False
        self.rotate_left = False
        self.rotate_right = False
        self.sprite = SpaceshipSprite((x,y))

    def thrust(self):
        self.thrusting = True
        
    def rotate(self, dir: str):
        if dir == 'l' or dir =='left':
            self.rotate_left = True
        elif dir == 'r' or dir == 'right':
            self.rotate_right = True

    def fire_bullet(self):
        if self.shoot_cd > 0:
            return
        self.shoot_cd = 0.3
        bullet_vel_x = -bullet_speed * np.sin(np.deg2rad(self.angle))
        bullet_vel_y = -bullet_speed * np.cos(np.deg2rad(self.angle))
        bullet_velocity = [bullet_vel_x, bullet_vel_y]
        self.bullet = Bullet(self.position[0],
                        self.position[1],
                        bullet_velocity,
                        self.angle)
    
    def apply_physics(self):
        self.reset_accel()
        
        # rotation
        if self.rotate_left and self.rotate_right:
            pass
        elif self.rotate_left:
            self.angle = (self.angle + rotation_speed)
        elif self.rotate_right:
            self.angle = (self.angle - rotation_speed)
        
        # thrust
        if self.fuel <= 0:
            self.fuel = 0
            self.thrusting = False
        elif self.thrusting:
            self.acceleration[0] += -20 * np.sin(np.deg2rad(self.angle))
            self.acceleration[1] += -20 * np.cos(np.deg2rad(self.angle))
            self.fuel -= consume_fuel_rate * dt

        # update velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        #max velocity
        if self.velocity[0] != max(-1000, min(1000, self.velocity[0])):
            self.velocity[0] = max(-1000, min(1000, self.velocity[0]))
            self.acceleration[0] == 0
        if self.velocity[1] != max(-1000, min(1000, self.velocity[1])):
            self.velocity[1] = max(-1000, min(1000, self.velocity[1]))
            self.acceleration[1] == 0

        # update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def update(self):
        # update Spaceship
        self.apply_physics()
        self.sprite.update(self.position, self.angle)
        self.shoot_cd -= dt
        self.thrusting = False
        self.rotate_left = False
        self.rotate_right = False

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
    def __init__(self, x, y, v, angle):
        super().__init__(x, y) #position from spaceship, velocity from spaceship angle and bullet speed cons
        self.position = np.array([x, y])
        self.velocity = np.array(v)
        self.angle = angle

        #rectangle laser bullet
        self.sprite = BulletSprite(self.velocity, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect

    def update(self):
        self.position = self.position + self.velocity * dt
        self.sprite.update(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect

        #add lifetime for bullet later



        #abel fikse at vises på skjermen