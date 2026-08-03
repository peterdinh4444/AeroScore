import pygame, sys, time
from settings import *
from sprites import BG

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        #   sprite groups 
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprite setup 
        BG(self.all_sprites)



    def run(self):
        last_time = time.time()


        while True: 
            dt = time.time() - last_time
            last_time = time.time()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            

            pygame.display.update()
            self.clock.tick(FRAMERATE)


    


if __name__ == "__main__":
    game = Game()
    game.run()