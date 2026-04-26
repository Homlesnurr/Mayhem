'''
Config file with global variables. Authors: Abel Yttervik, Vincent Anuwat Van Duin
'''
from logging import config


screen_dimensions = (1200, 640)
fullscreen = False
FPS = 60
border = 10

class PhysicsConfig:
    """
    Config class for physics engine parameters
    """
    dt = 1/FPS
    starting_fuel = 100
    rotation_speed = 2
    consume_fuel_rate = 10
    bullet_speed = 500
    barrel_respawn_time = 5000
    gravity = 200
    thrust_power = 670
    max_velocity = 400
    velocity_damping = 0.99
    shoot_cooldown = 0.1
