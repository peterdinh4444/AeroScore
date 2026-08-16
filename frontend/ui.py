from settings import * 
import pygame
from os.path import join

class UI:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font(join(BASE_DIR, 'graphics', 'font', 'BD_Cartoon_Shout.ttf'), 30)
        self.menu_surf = pygame.image.load(join(BASE_DIR, 'graphics', 'ui', 'menu.png'))
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/1.3))


    def display_menu(self):
        self.display_surface.blit(self.menu_surf, self.menu_rect)

    def display_score(self, score, game_state):
        if game_state == "playing":
            x, y = 100, 100
            score_surf = self.font.render(f'Score: {score}', True, 'black')
        elif game_state == "entering_name":
            x, y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
            score_surf = self.font.render(f'Your Score: {score}', True, 'black')
        elif game_state == "submitted":
            x, y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + self.menu_rect.height
            score_surf = self.font.render(f'Your Score: {score}', True, 'coral1')

        score_rect = score_surf.get_rect(center = (x,y))
        self.display_surface.blit(score_surf, score_rect)


    def display_name_input(self, name_input):
        box_rect = pygame.Rect(0, 0, 300, 50)
        box_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + self.menu_rect.height)
        pygame.draw.rect(self.display_surface, 'white', box_rect)
        pygame.draw.rect(self.display_surface, 'black', box_rect, 2)

        prompt_font = pygame.font.Font(join(BASE_DIR, 'graphics', 'font', 'BD_Cartoon_Shout.ttf'), 18)
        prompt_surf = prompt_font.render("Enter name and press return:", True, 'black')
        prompt_rect = prompt_surf.get_rect(midbottom=(box_rect.centerx, box_rect.top - 10))
        self.display_surface.blit(prompt_surf, prompt_rect)

        text_surf = self.font.render(name_input, True, 'black')
        text_rect = text_surf.get_rect(center=box_rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def display_leaderboard(self, leaderboard_data):
        start_y = 100
        title_surf = self.font.render("Top Ten Scores", True, 'black')
        self.display_surface.blit(title_surf, title_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, start_y)))

        for i, entry in enumerate(leaderboard_data[:10]):
            ranking_text = f"{i+1}. {entry['player_name']} - {entry['player_score']}"
            row_surf = self.font.render(ranking_text, True, 'black')
            
            if i+1 == 1: row_surf = self.font.render(ranking_text, True, 'gold')
            elif i+1 == 2: row_surf = self.font.render(ranking_text, True, 'silver')
            elif i+1 == 3: row_surf = self.font.render(ranking_text, True, 'saddlebrown')
            
            row_rect = row_surf.get_rect(topleft=(WINDOW_WIDTH / 2 - 170, start_y + 20 + i * 35))
            self.display_surface.blit(row_surf, row_rect)
