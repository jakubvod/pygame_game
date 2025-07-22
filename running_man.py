from pathlib import Path
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(abs_path / "graphics" / "player" / "alienPink_walk1.png").convert_alpha()
        player_walk_2 = pygame.image.load(abs_path / "graphics" / "player" / "alienPink_walk2.png").convert_alpha()
        self.player_jump = pygame.image.load(abs_path / "graphics" / "player" / "alienPink_jump.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.gravity = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (125, 300))

    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -18

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            # Jump
            self.image = self.player_jump

        else:
            # Walk
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.animate()
        self.check_input()
        self.apply_gravity()


def display_score():
    # Score
    time = int((pygame.time.get_ticks() - start_time) / 1000)
    surf = font.render(f"Score: {time}", False, (0, 0, 0))
    rect = surf.get_rect(center = (350, 50))
    screen.blit(surf, rect)

    # Outline
    outline = rect.inflate(15, 15)
    pygame.draw.rect(screen, (0, 0, 0), outline, 3)

    return time


# Initialization
abs_path = Path(__file__).parent
pygame.init()
screen = pygame.display.set_mode((700, 450))
pygame.display.set_caption("Running Man")
clock = pygame.time.Clock()
game_active = True
start_time = 0

# Font
font = pygame.font.Font(abs_path / "font" / "joystix_monospace.otf", 20)


# Background
sky_background = pygame.image.load(abs_path / "graphics" / "background" / "backgroundEmpty.png").convert()
ground = pygame.image.load(abs_path / "graphics" / "background" / "ground.png").convert()

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
        # Draw Objects
        screen.blit(sky_background, (0, -284))
        screen.blit(ground, (0, 300))
        player.draw(screen)

        # Update 
        player.update()

        score = display_score()
    else:
        pass


    pygame.display.update()
    clock.tick(60)