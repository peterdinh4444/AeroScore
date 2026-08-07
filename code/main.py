import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # sprite groups 
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprite setup 
        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        self.plane = Plane(self.all_sprites)

        # obstacle timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 500)


    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, True):
            pygame.quit()
            sys.exit()


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

            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.collisions()
            

            pygame.display.update()
            self.clock.tick(FRAMERATE)


    


if __name__ == "__main__":
    game = Game()
    game.run()