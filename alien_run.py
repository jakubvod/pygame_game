from pathlib import Path
import pygame
import math
from random import randint, choice
import json

# Constants
FPS = 60
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
GROUND_HEIGHT = PLAYER_HEIGHT = 375

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load(abs_path / "graphics" / "player" / "alienPink_walk1.png").convert_alpha()
        player_walk_2 = pygame.image.load(abs_path / "graphics" / "player" / "alienPink_walk2.png").convert_alpha()
        self.player_jump = pygame.image.load(abs_path / "graphics" / "player" / "alienPink_jump.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0.0
        self.gravity = 0

        self.image = self.player_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom = (125, PLAYER_HEIGHT))

    def check_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= PLAYER_HEIGHT:
            self.gravity = -18

    def apply_gravity(self) -> None:
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= PLAYER_HEIGHT: self.rect.bottom = PLAYER_HEIGHT

    def animate(self) -> None:
        if self.rect.bottom < PLAYER_HEIGHT:
            # Jump
            self.image = self.player_jump

        else:
            # Walk
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self) -> None:
        self.animate()
        self.check_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.animation_index = 0.0
        self.animations: list[pygame.Surface] = []

        if name == "spider":
            self.animations.append(pygame.image.load(abs_path / "graphics" / "obstacles" / "spider_walk1.png").convert_alpha())
            self.animations.append(pygame.image.load(abs_path / "graphics" / "obstacles" / "spider_walk2.png").convert_alpha())
            self.image = self.animations[int(self.animation_index)]
            self.rect = self.image.get_rect(midbottom = (randint(1000,1400), PLAYER_HEIGHT))

        else: # fly
            self.animations.append(pygame.image.load(abs_path / "graphics" / "obstacles" / "fly.png").convert_alpha())
            self.animations.append(pygame.image.load(abs_path / "graphics" / "obstacles" / "fly_fly.png").convert_alpha())
            self.image = self.animations[int(self.animation_index)]
            self.rect = self.image.get_rect(midbottom = (randint(1000,1400), 250))
    
    def animate(self) -> None:
        self.animation_index += 0.1
        if self.animation_index >= len(self.animations): self.animation_index = 0
        self.image = self.animations[int(self.animation_index)]
    
    def destroy(self) -> None:
        if self.rect.right <= 0:
            self.kill()

    def update(self) -> None:
        self.animate()
        self.rect.x -= 6
        self.destroy()

def collision() -> bool:
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return True
    return False

def display_score() -> int:
    # Score
    time = int((pygame.time.get_ticks() - start_time) / 1000)
    surf = font.render(f"Score: {time}", False, (255, 255, 255))
    rect = surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.09))
    screen.blit(surf, rect)

    # Outline
    outline = rect.inflate(15, 15)
    pygame.draw.rect(screen, (255, 255, 255), outline, 3)

    return time

def load_highscore() -> int:
    with open(abs_path / "highscore.json", "r") as file:
        data = json.load(file)
        return data.get("highscore", 0)

def save_highscore(score: int) -> None:
    with open(abs_path / "highscore.json", "w") as file:
        json.dump({"highscore": score}, file)

def draw_background(sky, ground, ground_scroll: int, sky_scroll: int) -> tuple[int, int]:
    for i in range(0, tiles):
        screen.blit(sky, (i * sky.get_width() + sky_scroll, 0))

    for i in range(0, tiles):
        # Draw scrolling ground
        screen.blit(ground, (i * ground.get_width() + ground_scroll, GROUND_HEIGHT))
    
    sky_scroll -= 2
    ground_scroll -= 5

    # Reset scroll
    if abs(ground_scroll) > ground.get_width():
        ground_scroll = 0
    if abs(sky_scroll) > sky.get_width():
        sky_scroll = 0
    return ground_scroll, sky_scroll

def draw_intro() -> None:
    alien_intro = pygame.transform.rotozoom((pygame.image.load(abs_path / "graphics" / "player" / "alienPink.png").convert_alpha()), 0, 2)
    alien_intro_rect = alien_intro.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.44))

    intro_font = font_big.render(f"Alien Run", False, (255, 255, 255))
    intro_font_rec = intro_font.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.68))

    intro_font_2 = font.render(f"Press SPACE to start", False, (255, 255, 255))
    intro_font_2_rec = intro_font_2.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.74))

    screen.blit(alien_intro, alien_intro_rect)
    screen.blit(intro_font, intro_font_rec)
    screen.blit(intro_font_2, intro_font_2_rec)

def draw_death(highscore: int) -> None:
    game_over = font_big.render("GAME OVER", False, (255, 255, 255))
    game_over_rect = game_over.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4))

    result = font.render(f"Your score: {score}", False, (255, 255, 255))
    result_rect = result.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    highscore = font.render(f"Highscore: {highscore}", False, (255, 255, 255))
    highscore_rect = highscore.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.55))

    restart = font_big.render("PRESS SPACE TO RESTART", False, (255, 255, 255))
    restart_rect = restart.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9))

    screen.blit(game_over, game_over_rect)
    screen.blit(result, result_rect)
    screen.blit(highscore, highscore_rect)
    screen.blit(restart, restart_rect)
    outline = restart_rect.inflate(15, 15)
    pygame.draw.rect(screen, (255, 255, 255), outline, 3)


# Initialization
abs_path = Path(__file__).parent
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Run")
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
highscore = load_highscore()

# Font
font = pygame.font.Font(abs_path / "font" / "joystix_monospace.otf", 20)
font_big = pygame.font.Font(abs_path / "font" / "joystix_monospace.otf", 40)


# Background
sky_background = pygame.image.load(abs_path / "graphics" / "background" / "bg2.png").convert()

ground = pygame.image.load(abs_path / "graphics" / "background" / "ground_cropped.png").convert()
tiles = math.ceil(SCREEN_WIDTH / ground.get_width()) + 1 # One additional buffer for scrolling
ground_scroll = 0
sky_scroll = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1700)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["spider", "spider", "fly"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks() # Reset timer after death
    
    if game_active:
        # Scroll background 
        ground_scroll, sky_scroll = draw_background(sky_background, ground, ground_scroll, sky_scroll)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = display_score()

        if collision():
            game_active = False
        
        

    else:
        screen.fill((0, 51, 102))

        if score == 0:  # Intro screen
            draw_intro()

        else: # Death screen
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            draw_death(highscore)

    pygame.display.update()
    clock.tick(FPS)