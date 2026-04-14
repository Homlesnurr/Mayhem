import pygame
import config
from typing import Callable
from abc import ABC, abstractmethod

class SpriteBase(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self):
        pass


class BulletSprite(SpriteBase):
    def __init__(self, pos: list[int, int], angle: float):
        super().__init__()
        self.bullet_surf = pygame.Surface((6, 20), pygame.SRCALPHA)
        self.pos = pos
        self.image_base = self.bullet_surf
        self.image = self.image_base.copy()
        self.rect = pygame.Surface.fill(self.bullet_surf, (255, 0, 0))
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
    def __init__(self, pos: list[int, int]):
        super().__init__()
        self.ship_sprite = ImageLoader('assets\\rocket_ship_blue.png', scale=0.7)
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


class RoundedButton(SpriteBase):
    '''
    Class for making rounded buttons.
    '''
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: tuple[int,int,int] = (255,255,255),
                 text: str = None,
                 click_func: Callable | None = None,
                 hover_func: Callable | None = None) -> None:
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
        self.hover_func = hover_func


    def update(self):
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(*pygame.mouse.get_pos(), 1,1)
        if mouse_sprite.rect.colliderect(self.rect):
            self.curr_color = self.hover_color
        else:
            self.curr_color = self.color
        pygame.draw.rect(self.image, self.curr_color, (0,0,*self.size), border_radius=5)
        self.image.blit(self.text_surface, self.text_rect)
        self.hovered=False


    def hover(self):
        self.hovered = True


    def click(self):
        if isinstance(self.click_func, Callable):
            self.click_func()
            return
        print('Unassigned button pressed.')


class ImageLoader(SpriteBase):
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
    def __init__(self):
        super().__init__()
        border = 10 #7
        width = config.screen_dimensions[0]
        height = config.screen_dimensions[1]
        map_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        background = ImageLoader('assets\\temp_background.jpeg', (width, height))
        map_surface.blit(background.image, (0,0))
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

    