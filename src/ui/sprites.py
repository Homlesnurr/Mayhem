from __future__ import annotations                                                                                                                                                                     
import pygame
import config
from typing import Callable
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING   

if TYPE_CHECKING:                                                                                                                                                                                      
    from game_logic.physics import Spaceship, Player   

class SpriteBase(pygame.sprite.Sprite, ABC):
    '''
    Base class for all sprites, requiring an update() function, and making them a pygame.sprite.Sprite.
    '''
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self):
        pass


class BulletSprite(SpriteBase):
    '''
    Sprite for bullet. Takes position and angle value to initialize location.

    update(pos, angle) to move the sprite.
    '''
    def __init__(self, pos: pygame.Vector2, angle: float, player_id: str):
        super().__init__()
        self.bullet_surf = pygame.Surface((6, 20), pygame.SRCALPHA)
        self.pos = pos
        self.color = (255,0,0) if player_id == 'Player 1' else (0,255,0)
        self.rect = pygame.Surface.fill(self.bullet_surf, self.color)
        self.image = pygame.transform.rotate(self.bullet_surf, angle)
        self.rect = self.image.get_rect(center = self.pos)
    
    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = (pos)

    def update(self, pos: pygame.Vector2):
        self.set_pos(pos)


class SpaceshipSprite(SpriteBase):
    '''
    Sprite for bullet. Takes position value to initialize location.

    update(pos, angle) to move the sprite.
    '''
    def __init__(self, pos: list[int, int]):
        super().__init__()
        self.ship_sprite = ImageLoader('assets\\rocket_ship_blue.png', scale=0.5)
        self.pos = pos
        self.image = self.ship_sprite.image
        self.image_base = self.image.copy()
        self.rect = self.image.get_rect(center = self.pos)
    
    def rotate_sprite(self, angle):
        self.image = pygame.transform.rotate(self.image_base, angle)
        self.rect = self.image.get_rect(center = self.pos)
        
    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = (pos)

    def update(self,
               pos: list[int, int] = [config.screen_dimensions[0] // 2, config.screen_dimensions[1] // 2],
               angle: int | float = 0):
        angle = self.rotate_sprite(angle)
        pos = self.set_pos(pos)
        return self.image, self.rect


class ObstacleSprite(SpriteBase):
    def __init__(self, pos: list[int, int], angle: float):
        super().__init__()

        self.width = 100
        self.height = 300

        self.obstacle_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.obstacle_surf.fill((167,167,167))
        
        self.pos = pos
        self.image_base = self.obstacle_surf
        self.image = self.image_base.copy()
       
        self.rect = self.image.get_rect(center = self.pos)

        self.angle = 0.0
        self.rotate_sprite(self.angle)
    

    def rotate_sprite(self, angle):
        self.image = pygame.transform.rotate(self.image_base, angle)
        self.rect = self.image.get_rect(center = self.pos)
    
    
    def update(self, angle: int | float = 0):
        self.rotate_sprite(angle)


class FueldropSprite(ObstacleSprite):
    def __init__(self, pos: list[int, int], angle: float):
        super().__init__(pos, angle)
        self.ship_sprite = ImageLoader('assets\\barrel.png', scale=0.4)
        self.pos = pos
        self.image = self.ship_sprite.image
        self.image_base = self.image.copy()
        self.rect = self.image.get_rect(center = self.pos)
        
    def rotate_sprite(self, angle):
        self.image = pygame.transform.rotate(self.image_base, angle)
        self.rect = self.image.get_rect(center = self.pos)
    
    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = (pos)
    
    def update(self,
               pos: list[int, int] = [config.screen_dimensions[0] // 2, config.screen_dimensions[1] // 2],
               angle: int | float = 0):
        self.rotate_sprite(angle)
        self.set_pos(pos)


class RoundedButton(SpriteBase):
    '''
    Class for making rounded buttons.

    Takes location of center, size, color and text. And has potential for adding functions to button
    '''
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: tuple[int,int,int] = (255,255,255),
                 text: str = None,
                 click_func: Callable | None = None,
                 hoverable: bool = True) -> None:
        super().__init__()
        self.color = color
        self.curr_color = color
        self.hover_color = (200,200,200)
        self.hovered = False
        self.dimensions = config.screen_dimensions
        self.pos = [x,y]
        self.size = [width, height]

        font = pygame.font.Font(None, int(width//7))
        self.text_surface = font.render(text, True, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center=(width//2,height//2))
        
        button_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(button_surface, self.curr_color, (0,0,*self.size), border_radius=5)
        button_surface.blit(self.text_surface, self.text_rect)
        button_rect = button_surface.get_rect(center = (x,y))

        self.image = button_surface
        self.rect = button_rect

        self.click_func = click_func
        self.hoverable = hoverable


    def update(self):
        pygame.draw.rect(self.image, self.curr_color, (0,0,*self.size), border_radius=5)
        self.image.blit(self.text_surface, self.text_rect)
        self.curr_color = self.color

    def hover(self):
        if self.hoverable:
            self.curr_color = self.hover_color


    def click(self):
        if isinstance(self.click_func, Callable):
            self.click_func()
            return
        print('Unassigned button pressed.')


class ImageLoader(SpriteBase):
    '''
    Loads image, and makes a self.image and self.rect, which is required for every pygame.sprite.Sprite.
    '''
    def __init__(self,
                 image_path: str = None,
                 size: tuple[int, int] = None,
                 scale: int = None):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path)
            if size:
                self.image = pygame.transform.smoothscale(self.image, size)
            elif scale:
                self.image = pygame.transform.smoothscale_by(self.image, scale)
            self.rect = self.image.get_rect()
        except:
            raise SyntaxError(f'Couldnt load image: {image_path}')
    
    def update(self):
        pass

class StatSprite(SpriteBase):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.surf_width = config.screen_dimensions[0]
        self.surf_height = config.screen_dimensions[1]
        self.surf = pygame.Surface((self.surf_width, self.surf_height), pygame.SRCALPHA)
        self.width = 300
        self.height = 50
        self.fuel_color = (0,255,0)
        self.empty_color = (67,67,67)
        if self.player._name == 'Player 1':
            self.x, self.y = config.border, config.border
        elif self.player._name == 'Player 2':
            self.x, self.y = config.screen_dimensions[0]-self.width - config.border, config.border

        fuel = self.width
        
        # Fuel bar
        if self.player._name == 'Player 1':
            pygame.draw.rect(self.surf, self.empty_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.surf, self.fuel_color, (self.x, self.y, fuel, self.height))
        elif self.player._name == 'Player 2':
            pygame.draw.rect(self.surf, self.empty_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.surf, self.fuel_color, (self.x + (self.width - fuel), self.y, self.width - (self.width - fuel), self.height))
        
        # Score
        font = pygame.font.Font(None, int(self.surf_width//12))
        self.text_surface = font.render(f'{0}', True, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + 2*self.height))        
        self.surf.blit(self.text_surface, self.text_rect)
        
        self.image = self.surf
        self.rect = self.surf.get_rect()

    def update(self, fuel, score):
        fuel = fuel * self.width / 100
        self.surf.fill((0,0,0,0))
        # Fuel bar
        if self.player._name == 'Player 1':
            pygame.draw.rect(self.surf, self.empty_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.surf, self.fuel_color, (self.x, self.y, fuel, self.height))
        elif self.player._name == 'Player 2':
            pygame.draw.rect(self.surf, self.empty_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.surf, self.fuel_color, (self.x + (self.width - fuel), self.y, fuel+1, self.height))
        
        # Score
        font = pygame.font.Font(None, int(self.surf_width//12))
        self.text_surface = font.render(f'{score}', True, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + 2*self.height))        
        self.surf.blit(self.text_surface, self.text_rect)
        self.image = self.surf
        self.rect = self.surf.get_rect()