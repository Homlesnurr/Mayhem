from __future__ import annotations
import pygame
import numpy as np
import config
from src.ui import SpaceshipSprite, BulletSprite, ObstacleSprite, FueldropSprite, StatSprite
from config import PhysicsConfig


class PhysicsEngine:
    '''
    Container for every element where physics are required.
    '''
    def __init__(self):
        self._solids = pygame.sprite.Group()
        self._players = pygame.sprite.Group()
        self._stats = pygame.sprite.Group()
        self._spaceships = pygame.sprite.Group()
        self._bullets = pygame.sprite.Group()
        self.respawn_overseer = FuelRespawnOverseer()
        self.collision_handler = CollisionHandler(self)

    def add_solid(self, solid):
        self._solids.add(solid)

    def add_player(self, player: Player):
        self._players.add(player)
        self._stats.add(player.stats)
        self.add_spaceship(player.ship)

    def add_spaceship(self, ship: Spaceship):
        self._spaceships.add(ship)

    def add_bullet(self, bullet: Bullet):
        self._bullets.add(bullet)
    
    def draw(self, surface):
        self._solids.draw(surface)
        self._spaceships.draw(surface)
        self._stats.draw(surface)
        self._bullets.draw(surface)
    
    def update(self):
        for ship in self._spaceships:
            self.collision_handler.check_ship_collisions(ship)
            self.collision_handler.check_bullet_collisions(ship)
            self.collision_handler.check_solid_collisions(ship)
        self.collision_handler.check_bullet_solid_collisions()
        self.respawn_overseer.update(self)             
        self._solids.update()
        self._bullets.update()
        self._players.update()
        self._spaceships.update()

class CollisionHandler:
    """
    Class for handling collisions between different objects. Uses pygames collision functions to check for collisions.
    """
    def __init__(self, physics_engine: PhysicsEngine):
        self.physics_engine = physics_engine
    
    def check_ship_collisions(self, ship: Spaceship):
            # Check for ship collisions
            collided_ships = pygame.sprite.spritecollide(ship, [s for s in self.physics_engine._spaceships if s is not ship], False, pygame.sprite.collide_mask)
            if collided_ships:
                for c_ship in [*collided_ships, ship]:
                    for player in self.physics_engine._players:
                        if c_ship._owner == player._name:
                            player.kill_ship(self.physics_engine)
    
    def check_bullet_collisions(self, ship: Spaceship):
        hits = pygame.sprite.spritecollide(ship, [b for b in self.physics_engine._bullets if b._owner != ship._owner], False, pygame.sprite.collide_mask)
        if hits:
            for hit in hits:
                if isinstance(hit, Bullet):
                    for player in self.physics_engine._players:
                        if ship._owner == player._name:
                            player.kill_ship(self.physics_engine)
                        if hit._owner == player._name:
                            player.give_points(10)
                    hit.kill()
                else:
                    for player in self.physics_engine._players:
                        if hit._owner == player._name:
                            player.kill_ship(self.physics_engine)
    def check_solid_collisions(self, ship: Spaceship):
        collided_solids = pygame.sprite.spritecollide(ship, self.physics_engine._solids, False, pygame.sprite.collide_mask)
        if collided_solids:
            for collision in collided_solids:
                if isinstance(collision, Fueldrop):
                    ship._fuel = min(PhysicsConfig.starting_fuel + 0.5 * PhysicsConfig.starting_fuel, PhysicsConfig.starting_fuel)
                    collision.destroy(self.physics_engine.respawn_overseer)
                else:
                    for player in self.physics_engine._players:
                        if ship._owner == player._name:
                            player.kill_ship(self.physics_engine)
    def check_bullet_solid_collisions(self):
        pygame.sprite.groupcollide(self.physics_engine._bullets, self.physics_engine._solids, True, False, pygame.sprite.collide_mask)
    

class FuelRespawnOverseer:
    """
    class for handling fuel respawns. when a fueldrop is destroyed, it gets added to the respawn list with a respawn time. This class checks the list and respawns the fueldrop when the time is right.
    """
    def __init__(self):
        self._fuel_respawns = []
    
    def push_respawn(self, position: tuple[int,int]):
        self._fuel_respawns.append({
            'position': position,
            'respawn_time': pygame.time.get_ticks() + PhysicsConfig.barrel_respawn_time
        })

    def update(self, physics_engine: PhysicsEngine):
        curr_time = pygame.time.get_ticks() 
        for respawn in self._fuel_respawns[:]:
            if curr_time >= respawn['respawn_time']:
                physics_engine.add_solid(Fueldrop(respawn['position'][0], respawn['position'][1]))
                self._fuel_respawns.remove(respawn)

    

class CorePhysics(pygame.sprite.Sprite):
    """
    Base class for physics based objects: Velocity, acceleration and position updates. All objects that move inherits this.
    """
    def __init__(self,
                 pos: pygame.Vector2= None,
                 vel: pygame.Vector2= None,
                 acc: pygame.Vector2= None,
                 angle: float=0):
        super().__init__()
        self.position = pos if pos is not None else pygame.Vector2(0, 0)
        self.velocity = vel if vel is not None else pygame.Vector2(0, 0)
        self.acceleration = acc if acc is not None else pygame.Vector2(0, 0)
        self.angle = angle
        
    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, player_tag: str):
        super().__init__()
        self._name = player_tag
        self._score = 0
        self.stats = StatSprite(self)
        self.make_ship()
    
    def make_ship(self):
        self.ship = Spaceship(self._name)
    
    def take_points(self, points: int=5):
        self._score -= points

    def give_points(self, points: int=10):
        self._score += points

    def kill_ship(self, physics_engine: PhysicsEngine):
        self.take_points(5)
        self.ship.kill()
        self.make_ship()
        physics_engine.add_spaceship(self.ship)
    
    def update(self):
        self.stats.update(self.ship._fuel, self._score)

class Spaceship(CorePhysics):
    '''
    Spaceship class, stores all data pertaining to the spaceship.
    '''
    def __init__(self, player_tag: str):
        if player_tag == 'Player 1':
            x = 100
            y = 100
        elif player_tag == 'Player 2':
            x = config.screen_dimensions[0] - 100
            y = 100
        else:
            raise LookupError(f'Player: {player_tag}, not valid player tag')
        super().__init__(pygame.Vector2(x,y))
        self._owner = player_tag
        self._fuel = PhysicsConfig.starting_fuel
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
            self.angle = (self.angle + PhysicsConfig.rotation_speed)
        elif dir == 'r' or dir == 'right':
            self.angle = (self.angle - PhysicsConfig.rotation_speed)

    def fire_bullet(self, physics_engine: PhysicsEngine):
        if self.shoot_cd > 0:
            return
        self.shoot_cd = PhysicsConfig.shoot_cooldown
        bullet_vel = - PhysicsConfig.bullet_speed * pygame.Vector2(np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle)))
        self.bullet = Bullet(self.position, bullet_vel, self.angle, self._owner)
        physics_engine.add_bullet(self.bullet)
                        
    
    def apply_physics(self):
        # Gravity
        self.acceleration = pygame.Vector2(0, 200) # Gravity
        
        # thrust
        if self._fuel <= 0:
            self._fuel = 0
            self.thrusting = False
        elif self.thrusting:
            self.acceleration -= PhysicsConfig.thrust_power * pygame.Vector2(np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle)))
            self._fuel -= PhysicsConfig.consume_fuel_rate * PhysicsConfig.dt

        # update velocity
        self.velocity += self.acceleration * PhysicsConfig.dt

        #max velocity
        if self.velocity.magnitude() > PhysicsConfig.max_velocity:
            self.velocity = self.velocity.normalize() * PhysicsConfig.max_velocity
        self.velocity = self.velocity * PhysicsConfig.velocity_damping


        # update position
        self.position += self.velocity * PhysicsConfig.dt

    def update(self):

        # update Spaceship
        self.apply_physics()
        self.image, self.rect = self.sprite.update(self.position, self.angle)
        self.shoot_cd -= PhysicsConfig.dt
        self.thrusting = False
        self.rotate_left = False
        self.rotate_right = False
    
class Bullet(CorePhysics):
    '''
    Bullet class, creates a bullet belonging to one player. Collisions will only apply to spaceships other than the one shooting.
    '''
    def __init__(self, pos: pygame.Vector2, vel: pygame.Vector2, angle: float, owner: str):
        super().__init__() #position from spaceship, velocity from spaceship angle and bullet speed cons
        self._owner = owner
        self.position = pos.copy()
        self.velocity = vel.copy()
        self.angle = angle
        self.lifetime = 5

        #rectangle laser bullet
        self.sprite = BulletSprite(self.position, self.angle, self._owner)
        self.image = self.sprite.image
        self.rect = self.sprite.rect

    def update(self):
        if self.lifetime <= 0:
            self.kill()
        self.lifetime -= PhysicsConfig.dt
        self.position += self.velocity * PhysicsConfig.dt
        self.sprite.update(self.position)
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
        self.angle = (self.angle + PhysicsConfig.rotation_speed/2) % 360
        
    def update(self):
        self.rotation()
        self.sprite.update(self.angle)
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
        self.angle = (self.angle + PhysicsConfig.rotation_speed/8) % 360
    
    def destroy(self, fuel_respawn_overseer: FuelRespawnOverseer):
        self.kill()
        fuel_respawn_overseer.push_respawn(self.position.copy())

    def update(self):
        self.rotation()
        self.sprite.update(self.position, self.angle)
        self.image = self.sprite.image
        self.rect = self.sprite.rect