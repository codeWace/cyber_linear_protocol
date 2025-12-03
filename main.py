"""
CYBER: Linear Protocol
Author: Wajiha Tasaduq

All characters and backgrounds provided by Craftpix.net
License: https://craftpix.net/file-licenses/
See ASSETS_LICENSES.txt for full details.
"""

import pygame
import os

# --- Settings ---
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 324
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER: Linear Protocol")
clock = pygame.time.Clock()

FONT = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)

# --- Utility: Load Animation Frames ---
def load_frames(folder, scale=None):
    frames = []
    for file in sorted(os.listdir(folder)):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
            if scale:
                img = pygame.transform.scale(img, scale)
            frames.append(img)
    return frames

# --- PRELOAD ASSETS ---
bg_assets = {
    "level1": load_frames("assets/backgrounds/level1/Day", (576, 324)),
    "level2": load_frames("assets/backgrounds/level2/Day", (576, 324)),
    "level3": load_frames("assets/backgrounds/level3/Day", (576, 324)),
    "level4": load_frames("assets/backgrounds/level4/Day", (576, 324)),
}

# Reuse earlier backgrounds for levels 5–7
bg_assets["level5"] = bg_assets["level1"]
bg_assets["level6"] = bg_assets["level2"]
bg_assets["level7"] = bg_assets["level3"]

player_frames = load_frames("assets/player", (83, 83))
player2_frames = load_frames("assets/player/player2", (83, 83))

# --- MENU ---
menu_bg_frames = bg_assets["level1"]
menu_anim_index = 0

def main_menu():
    global menu_anim_index
    running = True

    while running:
        dt = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        menu_anim_index += 0.08
        if menu_anim_index >= len(menu_bg_frames):
            menu_anim_index = 0

        screen.blit(menu_bg_frames[int(menu_anim_index)], (0, 0))

        start_text = FONT.render("START", True, (255, 180, 255))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 5))

        if start_rect.collidepoint(mouse_pos):
            start_text = FONT.render("START", True, (0, 255, 255))
            if mouse_click:
                level1()

        screen.blit(start_text, start_rect)
        pygame.display.update()

# --- GENERIC LEVEL FUNCTION ---
def run_level(level_no, bg_frames, question, answer, next_level=None):
    bg_index = 0
    robo_index = 0
    p2_index = 0

    robo_rect = player_frames[0].get_rect(topleft=(100, 240))
    p2_rect = player2_frames[0].get_rect(topleft=(400, 240))

    speed = 2
    asking = False
    user_input = ""

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if asking and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip() == answer:
                        running = False
                    user_input = ""
                    asking = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if len(user_input) < 20:
                        user_input += event.unicode

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            robo_rect.x -= speed
        if keys[pygame.K_RIGHT]:
            robo_rect.x += speed

        if robo_rect.colliderect(p2_rect) and keys[pygame.K_e]:
            asking = True

        # --- Update Animations ---
        bg_index = (bg_index + 0.12) % len(bg_frames)
        robo_index = (robo_index + 0.15) % len(player_frames)
        p2_index = (p2_index + 0.15) % len(player2_frames)

        # --- Draw Everything ---
        screen.blit(bg_frames[int(bg_index)], (0, 0))
        screen.blit(player_frames[int(robo_index)], robo_rect)
        screen.blit(player2_frames[int(p2_index)], p2_rect)

        if robo_rect.colliderect(p2_rect):
            hint = FONT.render("PRESS E", True, (255, 255, 0))
            screen.blit(hint, (p2_rect.x - 10, p2_rect.y - 20))

        if asking:
            q_surf = FONT.render(question, True, (255, 0, 180))
            a_surf = FONT.render(">" + user_input, True, (0, 255, 255))
            screen.blit(q_surf, (SCREEN_WIDTH//2 - q_surf.get_width()//2, 50))
            screen.blit(a_surf, (SCREEN_WIDTH//2 - a_surf.get_width()//2, 80))

        pygame.display.update()

    if next_level:
        next_level()
    else:
        end_screen()

# --- LEVELS ---
def level1(): run_level(1, bg_assets["level1"], "2x + 3 = 7", "2", level2)
def level2(): run_level(2, bg_assets["level2"], "5x - 4 = 11", "3", level3)
def level3(): run_level(3, bg_assets["level3"], "3x + 6 = 15", "3", level4)
def level4(): run_level(4, bg_assets["level4"], "4x - 5 = 11", "4", level5)
def level5(): run_level(5, bg_assets["level5"], "6x + 2 = 20", "3", level6)
def level6(): run_level(6, bg_assets["level6"], "7x - 3 = 18", "3", level7)
def level7(): run_level(7, bg_assets["level7"], "8x + 4 = 36", "4", None)

# --- END SCREEN ---
def end_screen():
    bg = bg_assets["level1"]
    bg_i = 0
    timer = 0

    while True:
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        bg_i = (bg_i + 0.1) % len(bg)
        screen.blit(bg[int(bg_i)], (0, 0))

        timer += dt
        if int(timer * 2) % 2 == 0:
            text = FONT.render("YOU DID IT!", True, (255, 215, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.update()

# --- START ---
main_menu()
