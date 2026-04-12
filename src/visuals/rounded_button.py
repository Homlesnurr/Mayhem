import pygame
import config
from typing import Callable
from src.visuals import SpriteBase

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