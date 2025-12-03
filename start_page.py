import pygame
import os
from settings import *

pygame.init()

# --- Screen setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER: Linear Protocol")
clock = pygame.time.Clock()

FONT = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)

# --- Load animated menu background (Level 1 Day) ---
bg_frames = []
bg_folder = os.path.join("assets", "backgrounds", "level1", "Day")

for file in sorted(os.listdir(bg_folder)):
    if file.endswith(".png"):
        img = pygame.image.load(os.path.join(bg_folder, file)).convert()
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_frames.append(img)

bg_index = 0

# --- Start Page Loop ---
running = True
while running:
    dt = clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # --- Animate background ---
    bg_index += 0.08
    if bg_index >= len(bg_frames):
        bg_index = 0

    screen.blit(bg_frames[int(bg_index)], (0, 0))

    # --- START text ---
    start_text = FONT.render("START", True, (255, 180, 255))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

    # Hover effect
    if start_rect.collidepoint(mouse_pos):
        start_text = FONT.render("START", True, (0, 255, 255))

        if mouse_click:
            print("Start Game clicked!")
            # CALL YOUR LEVEL 1 FUNCTION HERE:
            # level1()

            pygame.time.delay(200)

    screen.blit(start_text, start_rect)

    pygame.display.update()
