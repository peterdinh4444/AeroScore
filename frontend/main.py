import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from os.path import join
from api_client import submit_score, get_leaderboard

class Game:
    def __init__(self):
        pygame.init()
        self.active = True
        self.game_state = "playing" # playing, entering_name, submitted
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # sprite groups and initialization
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        self.plane = Plane(self.all_sprites)

        # obstacle timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 500)

        # text
        self.font = pygame.font.Font(join(BASE_DIR, 'graphics', 'font', 'BD_Cartoon_Shout.ttf'), 30)
        self.score = 0
        self.time_offset = 0

        # menu
        self.menu_surf = pygame.image.load(join(BASE_DIR, 'graphics', 'ui', 'menu.png'))
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/1.3))

        # music
        self.jump_sound = pygame.mixer.Sound(join(BASE_DIR, 'sounds', 'jump.wav'))
        self.jump_sound.set_volume(0.1)
        self.background_sound = pygame.mixer.Sound(join(BASE_DIR, 'sounds', 'music.wav'))
        self.background_sound.set_volume(0.05)
        self.background_sound.play(loops = -1)

        # leaderboard handling
        self.name_input = ""
        self.leaderboard_data = []
        self.score_submitted = False
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask):
            self.plane.kill()
            self.active = False
            self.game_state = "entering_name"
            self.name_input = ""
            self.score_submitted = False

    def clear_obstacles(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.sprite_type == 'obstacle':
                sprite.kill()

    def display_score(self):
        if self.game_state == "playing":
            x = 100
            y = 100
            self.score = (pygame.time.get_ticks() - self.time_offset) // 1000
            score_surf = self.font.render(f'Score: {self.score}', True, 'black')
        elif self.game_state == "entering_name":
            y = WINDOW_HEIGHT / 2
            x = WINDOW_WIDTH / 2
            score_surf = self.font.render(f'Your Score: {self.score}', True, 'black')
        elif self.game_state == "submitted":
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height
            x = WINDOW_WIDTH / 2
            score_surf = self.font.render(f'Your Score: {self.score}', True, 'coral1')


        
        score_rect = score_surf.get_rect(center = (x,y))
        self.display_surface.blit(score_surf, score_rect)

    def confirm_name_input(self):
        name = self.name_input.strip()
        if len(name) == 0:
            name = "Anonymous"
        if len(name) <= MAX_NAME_LENGTH:
            submit_score(name, self.score)
            self.leaderboard_data = get_leaderboard()
            self.game_state = "submitted"

    def display_name_input(self):
        box_rect = pygame.Rect(0, 0, 300, 50)
        box_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + self.menu_rect.height)
        pygame.draw.rect(self.display_surface, 'white', box_rect)
        pygame.draw.rect(self.display_surface, 'black', box_rect, 2)

        prompt_font = pygame.font.Font(join(BASE_DIR, 'graphics', 'font', 'BD_Cartoon_Shout.ttf'), 20)
        prompt_surf = prompt_font.render("Enter name, press Enter:", True, 'black')
        prompt_rect = prompt_surf.get_rect(midbottom=(box_rect.centerx, box_rect.top - 10))
        self.display_surface.blit(prompt_surf, prompt_rect)

        text_surf = self.font.render(self.name_input, True, 'black')
        text_rect = text_surf.get_rect(center=box_rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def display_leaderboard(self):
        if self.active:
            return
        start_y = 100
        title_surf = self.font.render("Top Ten Scores", True, 'black')
        self.display_surface.blit(title_surf, title_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, start_y)))

        for i, entry in enumerate(self.leaderboard_data[:10]):
            ranking_text = f"{i+1}. {entry['player_name']} - {entry['player_score']}"
            row_surf = self.font.render(ranking_text, True, 'black')
            
            if i+1 == 1: row_surf = self.font.render(ranking_text, True, 'gold')
            elif i+1 == 2: row_surf = self.font.render(ranking_text, True, 'silver')
            elif i+1 == 3: row_surf = self.font.render(ranking_text, True, 'saddlebrown')
            
            row_rect = row_surf.get_rect(topleft=(WINDOW_WIDTH / 2 - 150, start_y + 20 + i * 35))
            self.display_surface.blit(row_surf, row_rect)

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
            self.display_score()
            
            if self.game_state == "playing": 
                self.collisions()
            elif self.game_state == "entering_name": 
                
                self.display_name_input()
            elif self.game_state == "submitted":
                self.display_leaderboard()
                self.display_surface.blit(self.menu_surf, self.menu_rect)
                
            
            pygame.display.update()
            self.clock.tick(FRAMERATE)


    


if __name__ == "__main__":
    game = Game()
    game.run()