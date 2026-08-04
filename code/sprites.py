import pygame
from settings import *
from os.path import join, dirname, abspath


BASE_DIR = dirname(dirname(abspath(__file__)))
scale_factor = 0
class BG(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        bg_path = join(BASE_DIR, 'graphics', 'environment', 'background.png')
        bg_image = pygame.image.load(bg_path).convert()

        # image scaling 
        global scale_factor
        scale_factor = WINDOW_HEIGHT/bg_image.get_height()
        full_width = int(bg_image.get_width() * scale_factor)
        full_height = int(bg_image.get_height() * scale_factor)


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

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        ground_path = join(BASE_DIR, 'graphics', 'environment', 'ground.png')
        ground_surf = pygame.image.load(ground_path).convert_alpha()

        full_width = int(scale_factor * ground_surf.get_width())
        full_height = int(scale_factor * ground_surf.get_height())

        full_size_image = pygame.transform.scale(ground_surf, (full_width, full_height))

        self.image = pygame.Surface((full_width, full_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.image.blit(full_size_image, (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)


    def update(self,dt):
        self.pos.x -= 360 * dt
        
        if self.rect.centerx<=0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

