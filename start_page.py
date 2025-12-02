import pygame
import os
from settings import *

pygame.init()

# --- Screen setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER: Linear Protocol")
clock = pygame.time.Clock()

# --- Load menu background ---
menu_bg = pygame.image.load(os.path.join("assets", "backgrounds", "menubg.jpg")).convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Load individual buttons ---
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 70

start_btn_img = pygame.image.load("assets/ui/start.png").convert_alpha()
start_btn_img = pygame.transform.scale(start_btn_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

score_btn_img = pygame.image.load("assets/ui/score.png").convert_alpha()
score_btn_img = pygame.transform.scale(score_btn_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

exit_btn_img = pygame.image.load("assets/ui/exit.png").convert_alpha()
exit_btn_img = pygame.transform.scale(exit_btn_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

# --- Button rectangles (for positioning & hover) ---
start_rect = start_btn_img.get_rect(center=(SCREEN_WIDTH//2, 300))
score_rect = score_btn_img.get_rect(center=(SCREEN_WIDTH//2, 400))
exit_rect  = exit_btn_img.get_rect(center=(SCREEN_WIDTH//2, 500))

# --- Start Page Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Draw background ---
    screen.blit(menu_bg, (0, 0))

    # --- Draw buttons with hover effect ---
    # Start
    if start_rect.collidepoint(mouse_pos):
        screen.blit(start_btn_img, (start_rect.x + 5, start_rect.y))  # move 5px right
        if mouse_click:
            print("Start Game clicked!")  # Replace with Level 1 function
    else:
        screen.blit(start_btn_img, start_rect)

    # Score
    if score_rect.collidepoint(mouse_pos):
        screen.blit(score_btn_img, (score_rect.x + 5, score_rect.y))
        if mouse_click:
            print("Score clicked!")  # Placeholder
    else:
        screen.blit(score_btn_img, score_rect)

    # Exit
    if exit_rect.collidepoint(mouse_pos):
        screen.blit(exit_btn_img, (exit_rect.x + 5, exit_rect.y))
        if mouse_click:
            running = False
    else:
        screen.blit(exit_btn_img, exit_rect)

    pygame.display.update()

pygame.quit()
