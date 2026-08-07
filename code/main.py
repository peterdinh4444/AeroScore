import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from os.path import join, dirname, abspath

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # sprite groups 
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprite initialization
        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        self.plane = Plane(self.all_sprites)

        # obstacle timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 500)

        # text
        BASE_DIR = dirname(dirname(abspath(__file__)))
        self.font = pygame.font.Font(join(BASE_DIR, 'graphics', 'font', 'BD_Cartoon_Shout.ttf'), 30)
        self.score = 0

        # menu
        self.menu_surf = pygame.image.load(join(BASE_DIR, 'graphics', 'ui', 'menu.png'))
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        self.active = True
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask):
            self.active = False

    def display_score(self):
        if self.active:
            x = 100
            y = 100
        else:
            y  = WINDOW_HEIGHT / 2 + self.menu_rect.height
            x = WINDOW_WIDTH / 2


        self.score = pygame.time.get_ticks()//1000
        score_surf = self.font.render(f'Score: {self.score}', True, 'black')
        score_rect = score_surf.get_rect(center = (x,y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()


        while True: 
            dt = time.time() - last_time
            last_time = time.time()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.plane.jump()
                if event.type == self.obstacle_timer:
                    Obstacle([self.all_sprites, self.collision_sprites])
                if event.type == pygame.KEYDOWN and not self.active:
                    if event.key == pygame.K_SPACE:
                        self.active = True

            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            
            if self.active: 
                self.collisions()
            else: 
                self.display_surface.blit(self.menu_surf, self.menu_rect)
            
            pygame.display.update()
            self.clock.tick(FRAMERATE)


    


if __name__ == "__main__":
    game = Game()
    game.run()