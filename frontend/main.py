import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from ui import UI
from os.path import join
from api_client import submit_score, get_leaderboard

class Game:
    def __init__(self):
        pygame.init()
        self.active = True
        self.game_state = "playing" # playing, entering_name, submitted
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.ui = UI(self.display_surface)
        self.clock = pygame.time.Clock()

        # sprite and group initialization
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        self.plane = Plane(self.all_sprites)

        # obstacle timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 500)

        # score
        self.score = 0
        self.time_offset = 0

        # music
        self.jump_sound = pygame.mixer.Sound(join(BASE_DIR, 'sounds', 'jump.wav'))
        self.jump_sound.set_volume(0.1)
        self.background_sound = pygame.mixer.Sound(join(BASE_DIR, 'sounds', 'music.wav'))
        self.background_sound.set_volume(0.05)
        self.background_sound.play(loops = -1)

        # leaderboard handling
        self.name_input = ""
        self.leaderboard_data = []

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask):
            self.plane.kill()
            self.active = False
            self.game_state = "entering_name"
            self.name_input = ""


    def clear_obstacles(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.sprite_type == 'obstacle':
                sprite.kill()

    def confirm_name_input(self):
        name = self.name_input.strip()
        if len(name) == 0:
            name = "Anonymous"
        if len(name) <= MAX_NAME_LENGTH:
            submit_score(name, self.score)
            self.leaderboard_data = get_leaderboard()
            self.game_state = "submitted"


    def run(self):
        last_time = time.time()


        while True: 
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                # QUIT GAME
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # MOUSE CLICKS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "playing":
                        self.jump_sound.play()
                        self.plane.jump()
                    elif self.game_state == "submitted":
                        self.clear_obstacles()
                        self.plane = Plane(self.all_sprites)
                        self.active = True
                        self.time_offset = pygame.time.get_ticks()
                        self.game_state = "playing"
                # OBSTACLE CREATION
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites])
                # NAME SUBMISSION
                if event.type == pygame.KEYDOWN and self.game_state == "entering_name":
                    if event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif event.key == pygame.K_RETURN: 
                        self.confirm_name_input()
                    # checks input for only letters&num and proper input length
                    elif event.unicode.isalnum() and len(self.name_input) < MAX_NAME_LENGTH:
                        self.name_input += event.unicode
            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.ui.display_score(self.score, self.game_state)
            
            if self.game_state == "playing": 
                self.score = (pygame.time.get_ticks() - self.time_offset) // 1000
                self.collisions()
            elif self.game_state == "entering_name": 
                self.ui.display_name_input(self.name_input)
            elif self.game_state == "submitted":
                self.ui.display_leaderboard(self.leaderboard_data)
                self.ui.display_menu()
                            
            pygame.display.update()
            self.clock.tick(FRAMERATE)



if __name__ == "__main__":
    game = Game()
    game.run()