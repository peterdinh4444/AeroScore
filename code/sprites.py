import pygame
from settings import *
from os.path import join, dirname, abspath
from random import choice, randint


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

        self.sprite_type = 'ground'

        ground_path = join(BASE_DIR, 'graphics', 'environment', 'ground.png')
        ground_surf = pygame.image.load(ground_path).convert_alpha()

        full_width = int(scale_factor * ground_surf.get_width())
        full_height = int(scale_factor * ground_surf.get_height())

        full_size_image = pygame.transform.scale(ground_surf, (full_width, full_height))

        self.image = pygame.Surface((full_width, full_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.image.blit(full_size_image, (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)


        # mask
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,dt):
        self.pos.x -= 360 * dt
        
        if self.rect.centerx<=0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # image
        self.import_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20, WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 3000
        self.direction = 0 

    def import_frames(self):
        self.frames = []
        for i in range(3):
            plane_path = join(BASE_DIR, 'graphics', 'plane', f'red{i}.png')
            plane_frame = pygame.image.load(plane_path).convert_alpha()

            full_width = scale_factor * plane_frame.get_width() / 2
            full_height = scale_factor * plane_frame.get_height() / 2

            scaled_frame = pygame.transform.scale(plane_frame, (full_width, full_height))
            self.frames.append(scaled_frame)

    def apply_gravity(self,dt):
        self.direction += self.gravity * dt 
        self.pos.y += self.direction * dt 
        self.rect.y = round(self.pos.y)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.pos.y = self.rect.top
            if self.direction<0: self.direction = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.pos.y = self.rect.top
            self.direction = 0
        
    def jump(self):
        self.direction = -1000

    def animate(self, dt):
        self.frame_index+=50 * dt
        if self.frame_index>=len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction*0.009, 1)
        self.image = rotated_plane

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()
        # mask
        self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.sprite_type = 'obstacle'

        orientation = choice(('up', 'down'))
        self.image = pygame.image.load(join(BASE_DIR, 'graphics', 'obstacles', f'{choice([0,1])}.png'))
        full_height = self.image.get_height() * 1.5
        full_width = self.image.get_width() * 1.5

        self.image = pygame.transform.scale(self.image, (full_width, full_height))

        x = WINDOW_WIDTH + randint(40,100)

        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(0,50)
            self.rect = self.image.get_rect(midbottom = (x,y))
        elif orientation == 'down': 
            y = randint(-50,0)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100: self.kill()


        
