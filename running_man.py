from pathlib import Path
import pygame

# Initialization

abs_path = Path(__file__).parent
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Running Man")
clock = pygame.time.Clock()

# Background

sky_background = pygame.image.load(abs_path / "graphics" / "backgroundEmpty.png").convert()
ground = pygame.image.load(abs_path / "graphics" / "ground.png").convert()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    # Draw background
    screen.blit(sky_background, (0, -284))
    screen.blit(ground, (0, 475))


    pygame.display.update()
    clock.tick(60)