from pathlib import Path
import pygame
import math
from random import randint

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


def display_score() -> int:
    # Score
    time = int((pygame.time.get_ticks() - start_time) / 1000)
    surf = font.render(f"Score: {time}", False, (255, 255, 255))
    rect = surf.get_rect(center = (SCREEN_WIDTH / 2, 50))
    screen.blit(surf, rect)

    # Outline
    outline = rect.inflate(15, 15)
    pygame.draw.rect(screen, (255, 255, 255), outline, 3)

    return time

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


# Initialization
abs_path = Path(__file__).parent
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Running Man")
clock = pygame.time.Clock()
game_active = True
start_time = 0

# Font
font = pygame.font.Font(abs_path / "font" / "joystix_monospace.otf", 20)


# Background
sky_background = pygame.image.load(abs_path / "graphics" / "background" / "bg2.png").convert()

ground = pygame.image.load(abs_path / "graphics" / "background" / "ground_cropped.png").convert()
tiles = math.ceil(SCREEN_WIDTH / ground.get_width()) + 1 # One additional buffer for scrolling
ground_scroll = 0
sky_scroll = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

enemies = pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    if game_active:
        # Scroll background 
        ground_scroll, sky_scroll = draw_background(sky_background, ground, ground_scroll, sky_scroll)

        player.draw(screen)
        player.update()
        score = display_score()
    else:
        pass


    pygame.display.update()
    clock.tick(FPS)