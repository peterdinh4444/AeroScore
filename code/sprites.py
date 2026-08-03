import pygame
from settings import *
from os.path import join, dirname, abspath


BASE_DIR = dirname(dirname(abspath(__file__)))

class BG(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        bg_path = join(BASE_DIR, 'graphics', 'environment', 'background.png')
        bg_image = pygame.image.load(bg_path).convert()

        # image scaling 
        bg_height = bg_image.get_height()
        bg_scale_factor = WINDOW_HEIGHT/bg_height
        full_width = bg_image.get_width() * bg_scale_factor
        full_height = bg_image.get_height() * bg_scale_factor

        full_size_image = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width*2, full_height))
        self.image.blit(full_size_image, (0,0))
        self.image.blit(full_size_image, (full_width, 0))
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        self.pos.x -= 300 * dt
        
        if self.rect.centerx<=0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)