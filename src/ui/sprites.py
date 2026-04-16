import pygame
import config
from typing import Callable
from abc import ABC, abstractmethod

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
    def __init__(self, pos: list[int, int], angle: float, player_id: str):
        super().__init__()
        self.bullet_surf = pygame.Surface((6, 20), pygame.SRCALPHA)
        self.pos = pos
        self.image_base = self.bullet_surf
        self.image = self.image_base.copy()
        self.color = (255,0,0) if player_id == 'Player 1' else (0,255,0)
        self.rect = pygame.Surface.fill(self.bullet_surf, self.color)
        self.rect.center = self.pos
        self.rotate_sprite(angle)
    
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
    
    
    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def update(self,
               pos: list[int, int] = [config.screen_dimensions[0] // 2, config.screen_dimensions[1] // 2],
               angle: int | float = 0):
        self.rotate_sprite(angle)
        self.set_pos(pos)


class FueldropSprite(ObstacleSprite):
    def __init__(self, pos: list[int, int], angle: float):
        super().__init__(pos, angle)
        self.ship_sprite = ImageLoader('assets\\barrel.png', scale=0.6)
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


class Map(SpriteBase):
    '''
    Sprite for the background of the game screen.
    '''
    def __init__(self):
        super().__init__()
        border = 10 #7
        width = config.screen_dimensions[0]
        height = config.screen_dimensions[1]
        map_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Horizontal border
        pygame.draw.rect(map_surface, (167,167,167), (0, 0, width,border))
        pygame.draw.rect(map_surface, (167,167,167), (0, height-border, width, height))
        # Veritcal border
        pygame.draw.rect(map_surface, (167,167,167), (0, 0, border,height))
        pygame.draw.rect(map_surface, (167,167,167), (width-border, 0, width, height))
        
        self.image = map_surface
        self.rect = map_surface.get_rect()

    def update(self):
        pass

# draw bar for fuel taken from vincent Anuwat van Duin's second assignment in Objektorientert programmering
def draw_bar(screen, x, y, width, height, value, color):
    # Background bar
    pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height), border_radius=5)
    
    # Filled part
    fill_width = (value / 100) * width
    pygame.draw.rect(screen, color, (x, y, fill_width, height), border_radius=5)