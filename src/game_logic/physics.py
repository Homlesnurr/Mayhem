import pygame
#temp const
dt = 0.01
starting_fuel = 100

class Core_physics(pygame.sprite.Sprite):

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

    def update(self, dt):
        pass

class physics_engine:
    def __init__(self):
        self.spaceships = []

    def update(self):
        for spaceship in self.spaceships:
            spaceship.update()

class spaceship(Core_physics):
    def __init__(self, x, y, player_tag):
        super().__init__(x, y)
        self.player_tag = player_tag
        self.fuel = starting_fuel

        self.thrusting = False
        self.rotate_left = False
        self.rotate_right = False

    #add image/hitbox med rect? abel fikse trust    


    def update(self, dt):
        


        pass

class bullet(Core_physics):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self):
        pass