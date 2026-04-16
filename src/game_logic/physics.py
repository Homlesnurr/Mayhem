from __future__ import annotations
import pygame
import numpy as np
import config
from src.ui import SpaceshipSprite, Map, BulletSprite, ObstacleSprite, FueldropSprite
#temp const
dt = 1/config.FPS
starting_fuel = 100
rotation_speed = 2
consume_fuel_rate = 10
bullet_speed = 500


class PhysicsEngine:
    '''
    Container for every element where physics are required.
    '''
    def __init__(self):
        self.solid = pygame.sprite.Group()
        self.spaceships = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

    def add_solid(self, solid: Map):
        self.solid.add(solid)

    def add_spaceship(self, ship: Spaceship):
        self.spaceships.add(ship)

    def add_bullet(self, bullet: Bullet):
        self.bullets.add(bullet)
    
    def draw(self, surface):
        self.solid.draw(surface)
        self.spaceships.draw(surface)
        self.bullets.draw(surface)
    
    def update(self):
        # må legge til group update for alle objects senere
        self.solid.update()
        self.bullets.update(self)
        self.spaceships.update(self)

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
        self.acceleration[1] = 3 # Gravity
        self.acceleration[0] = 0
        
    def update(self):
        pass


class Spaceship(CorePhysics):
    '''
    Spaceship class, stores all data pertaining to the spaceship.
    '''
    def __init__(self, player_tag: str):
        if player_tag == 'Player 1':
            x = 100
            y = 100
        else:
            x = config.screen_dimensions[0] - 100
            y = 100
        super().__init__(x, y)
        self.player_tag = player_tag
        self.fuel = starting_fuel
        self.shoot_cd = 0
        self.thrusting = False
        self.rotate_left = False
        self.rotate_right = False
        self.sprite = SpaceshipSprite((x,y))
        self.image = self.sprite.image
        self.rect = self.sprite.rect

    def thrust(self):
        self.thrusting = True
        
    def rotate(self, dir: str):
        if dir == 'l' or dir =='left':
            self.rotate_left = True
        elif dir == 'r' or dir == 'right':
            self.rotate_right = True

    def fire_bullet(self, physics_engine: PhysicsEngine):
        if self.shoot_cd > 0:
            return
        self.shoot_cd = 0.3
        bullet_vel_x = -bullet_speed * np.sin(np.deg2rad(self.angle))
        bullet_vel_y = -bullet_speed * np.cos(np.deg2rad(self.angle))
        bullet_velocity = [bullet_vel_x, bullet_vel_y]
        self.bullet = Bullet(self.position[0],
                        self.position[1],
                        bullet_velocity,
                        self.angle,
                        self)
        physics_engine.add_bullet(self.bullet)
                        
    
    def apply_physics(self, physics_engine: PhysicsEngine):
        self.reset_accel()
        bullets_hit = pygame.sprite.spritecollide(self.sprite, physics_engine.bullets, False, pygame.sprite.collide_mask)
        for bullet in bullets_hit:
            if bullet.owner.player_tag != self.player_tag:
                physics_engine.add_spaceship(Spaceship(self.player_tag))
                bullet.kill()
                self.kill()
                return
        if pygame.sprite.spritecollide(self.sprite, physics_engine.solid, False, pygame.sprite.collide_mask):
            physics_engine.add_spaceship(Spaceship(self.player_tag))
            self.kill()
            return

        collided_ships = pygame.sprite.spritecollide(self.sprite, physics_engine.spaceships, False, pygame.sprite.collide_mask)
        for ship in collided_ships:
            if ship != self:
                physics_engine.add_spaceship(Spaceship(self.player_tag))
                physics_engine.add_spaceship(Spaceship(ship.player_tag))
                ship.kill()
                self.kill()
                return

        
        
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
            self.acceleration[0] += -12 * np.sin(np.deg2rad(self.angle))
            self.acceleration[1] += -12 * np.cos(np.deg2rad(self.angle))
            self.fuel -= consume_fuel_rate * dt

        # update velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        #max velocity
        if self.velocity[0] != max(-250, min(250, self.velocity[0])):
            self.velocity[0] = max(-250, min(250, self.velocity[0]))
            self.acceleration[0] == 0
        if self.velocity[1] != max(-250, min(250, self.velocity[1])):
            self.velocity[1] = max(-250, min(250, self.velocity[1]))
            self.acceleration[1] == 0


        # update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def update(self, physics_engine: PhysicsEngine):

        # update Spaceship
        self.apply_physics(physics_engine)
        self.image, self.rect = self.sprite.update(self.position, self.angle)
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
    '''
    Bullet class, creates a bullet belonging to one player. Collisions will only apply to spaceships other than the one shooting.
    '''
    def __init__(self, x, y, v, angle, owner: Spaceship):
        super().__init__(x, y) #position from spaceship, velocity from spaceship angle and bullet speed cons
        self.position = np.array([x, y])
        self.velocity = np.array(v)
        self.angle = angle
        self.owner = owner
        self.lifetime = 5

        #rectangle laser bullet
        self.sprite = BulletSprite(self.velocity, self.angle, owner.player_tag)
        self.image = self.sprite.image
        self.rect = self.sprite.rect

    def update(self, physics_engine: PhysicsEngine):
        if self.lifetime <= 0:
            self.kill()
        if pygame.sprite.spritecollide(self.sprite, physics_engine.solid, False, pygame.sprite.collide_mask):
            self.kill()
            return
        self.lifetime -= dt
        self.position = self.position + self.velocity * dt
        self.sprite.update(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect


class Obstacle(pygame.sprite.Sprite):
    '''
    Obstacle class, creates an obstacle that can be collided with. Obstacles are solid and cannot be passed through.
    '''
    def __init__(self, x, y):
        super().__init__()
        self.position = np.array([x, y])
        self.angle = 0.0
        self.sprite = ObstacleSprite(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect

    def rotation(self):
        self.angle = (self.angle + rotation_speed/2) % 360
    def update(self):
        self.rotation()
        self.sprite.update(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect

class Fueldrop(pygame.sprite.Sprite):
    """
    Fueldrop class, creates a obstacle that can be collided with and refills fuel when collided with.
    """
    def __init__(self, x, y):
        super().__init__()
        self.position = np.array([x, y])
        self.angle = 0.0
        self.sprite = FueldropSprite(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect
    
    def rotation(self):
        self.angle = (self.angle + rotation_speed/8) % 360

    def update(self):
        self.rotation()
        self.sprite.update(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect
    