import pygame
import os
import math

# --- Settings ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 770
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER: Linear Protocol")
clock = pygame.time.Clock()

# --- Load Menu Assets ---
menu_bg = pygame.image.load("assets/backgrounds/menubg.jpg").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
start_btn_img = pygame.image.load("assets/ui/start.png").convert_alpha()
start_btn_img = pygame.transform.scale(start_btn_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
score_btn_img = pygame.image.load("assets/ui/score.png").convert_alpha()
score_btn_img = pygame.transform.scale(score_btn_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
exit_btn_img = pygame.image.load("assets/ui/exit.png").convert_alpha()
exit_btn_img = pygame.transform.scale(exit_btn_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

start_rect = start_btn_img.get_rect(center=(SCREEN_WIDTH//2, 300))
score_rect = score_btn_img.get_rect(center=(SCREEN_WIDTH//2, 400))
exit_rect = exit_btn_img.get_rect(center=(SCREEN_WIDTH//2, 500))

# --- Generic Level Function ---
def run_level(level_number, bg_path, door_color, puzzle_question, puzzle_answer, next_level=None):
    # --- Load Level Assets ---
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Player frames
    player_frames = []
    player_folder = "assets/player"
    for file in sorted(os.listdir(player_folder)):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join(player_folder, file)).convert_alpha()
            img = pygame.transform.scale(img, (300, 300))
            player_frames.append(img)
    player_index = 0
    player_speed = 5
    player_anim_timer = 0
    player_rect = player_frames[0].get_rect(topleft=(SCREEN_WIDTH//2 - 55, SCREEN_HEIGHT - 255))

    # Portal frames
    portal_frames = []
    door_folder = f"assets/doors/{door_color}door"
    for file in sorted(os.listdir(door_folder)):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join(door_folder, file)).convert_alpha()
            img = pygame.transform.scale(img, (100, 150))
            portal_frames.append(img)
    portal_index = 0
    portal_anim_timer = 0
    portal_locked = True
    portal_rect = portal_frames[0].get_rect(topleft=(SCREEN_WIDTH//2 + 165, SCREEN_HEIGHT - 195))

    # Terminal frames
    terminal_frames = []
    terminal_color_folder = "pink" if door_color == "pink" else "blue"
    term_folder = f"assets/ui/terminals/{terminal_color_folder}"
    for file in sorted(os.listdir(term_folder)):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join(term_folder, file)).convert_alpha()
            img = pygame.transform.scale(img, (280, 280))
            terminal_frames.append(img)
    terminal_index = 0
    terminal_anim_timer = 0

    # Fonts
    terminal_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 11)
    terminal_color = (255, 0, 255) if terminal_color_folder == "pink" else (0, 255, 255)

    # Puzzle
    input_active = False
    user_input = ""
    displayed_question = ""
    question_timer = 0
    QUESTION_SPEED = 0.09

    float_timer = 0
    ANIM_SPEED = 0.2
    running_level = True

    while running_level:
        dt = clock.tick(FPS) / 1000
        float_timer += 0.05

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip() == puzzle_answer:
                        portal_locked = False
                        print(f"Correct! Level {level_number} portal unlocked!")
                    user_input = ""
                    input_active = False
                    displayed_question = ""
                    question_timer = 0
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    max_chars = 30
                    if len(user_input) < max_chars:
                        user_input += event.unicode

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += player_speed

        # Animate player
        player_anim_timer += ANIM_SPEED
        if player_anim_timer >= len(player_frames):
            player_anim_timer = 0
        player_index = int(player_anim_timer)

        # Animate portal
        portal_anim_timer += ANIM_SPEED
        if portal_anim_timer >= len(portal_frames):
            portal_anim_timer = 0
        portal_index = int(portal_anim_timer)

        # Animate terminal
        terminal_anim_timer += 0.15
        if terminal_anim_timer >= len(terminal_frames):
            terminal_anim_timer = 0
        terminal_index = int(terminal_anim_timer)

        # Portal interaction
        if player_rect.colliderect(portal_rect) and keys[pygame.K_e]:
            input_active = True

        if not portal_locked and player_rect.colliderect(portal_rect):
            running_level = False

        # --- Draw everything ---
        screen.blit(bg, (0, 0))
        screen.blit(portal_frames[portal_index], portal_rect)
        screen.blit(player_frames[player_index], player_rect)

        # Press E
        if player_rect.colliderect(portal_rect) and portal_locked:
            press_e_surf = terminal_font.render("PRESS E", True, terminal_color)
            screen.blit(press_e_surf,
                        (portal_rect.x + (portal_rect.width - press_e_surf.get_width()) // 2,
                         portal_rect.y - 25))

        # Terminal display
        if input_active:
            float_offset = math.sin(float_timer) * 6
            panel_x = SCREEN_WIDTH // 2 - terminal_frames[terminal_index].get_width() // 2
            panel_y = portal_rect.y - terminal_frames[terminal_index].get_height() - 20 + float_offset

            screen.blit(terminal_frames[terminal_index], (panel_x, panel_y))

            # Typing effect
            if question_timer < len(puzzle_question):
                question_timer += QUESTION_SPEED
                displayed_question = puzzle_question[:int(question_timer)]

            # Word-wrap
            max_width = terminal_frames[terminal_index].get_width() - 13
            words = displayed_question.split(" ")
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if terminal_font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            for i, line in enumerate(lines):
                text_surf = terminal_font.render(line.strip(), True, terminal_color)
                screen.blit(text_surf, (panel_x + 58, panel_y + 58 + i * 25))

            # User input below question
            input_surf = terminal_font.render(user_input, True, terminal_color)
            screen.blit(input_surf, (panel_x + 58, panel_y + terminal_frames[terminal_index].get_height() - 180))

        pygame.display.update()

    # Proceed to next level or end screen
    if next_level:
        next_level()
    else:
        end_screen()


# --- Level Wrappers ---
def level1(): run_level(1, "assets/backgrounds/level1bg.jpg", "pink", "Solve: 2x + 3 = 7", "2", level2)
def level2(): run_level(2, "assets/backgrounds/level2bg.jpg", "blue", "Solve: 5x - 4 = 11", "3", level3)
def level3(): run_level(3, "assets/backgrounds/level3bg.jpg", "pink", "Solve: 3x + 6 = 15", "3", level4)
def level4(): run_level(4, "assets/backgrounds/level4bg.jpg", "blue", "Solve: 4x - 5 = 11", "4", level5)
def level5(): run_level(5, "assets/backgrounds/level5bg.jpg", "pink", "Solve: 6x + 2 = 20", "3", level6)
def level6(): run_level(6, "assets/backgrounds/level6bg.jpg", "blue", "Solve: 7x - 3 = 18", "3", level7)
def level7(): run_level(7, "assets/backgrounds/level7bg.jpg", "pink", "Solve: 8x + 4 = 36", "4", None)


# --- End Screen ---
def end_screen():
    font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
    bg = pygame.image.load("assets/backgrounds/level1bg.jpg").convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    timer = 0
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(bg, (0, 0))

        timer += dt
        if int(timer*2) % 2 == 0:
            text_surf = font.render("YOU DID IT!", True, (255, 215, 0))
            screen.blit(text_surf, ((SCREEN_WIDTH - text_surf.get_width())//2,
                                     (SCREEN_HEIGHT - text_surf.get_height())//2))

        pygame.display.update()


# --- Main Menu Loop ---
running_menu = True
while running_menu:
    dt = clock.tick(FPS) / 1000
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_menu = False

    screen.blit(menu_bg, (0, 0))

    if start_rect.collidepoint(mouse_pos):
        screen.blit(start_btn_img, (start_rect.x + 5, start_rect.y))
        if mouse_click:
            running_menu = False
            level1()
    else:
        screen.blit(start_btn_img, start_rect)

    if score_rect.collidepoint(mouse_pos):
        screen.blit(score_btn_img, (score_rect.x + 5, score_rect.y))
        if mouse_click:
            print("Score clicked!")
    else:
        screen.blit(score_btn_img, score_rect)

    if exit_rect.collidepoint(mouse_pos):
        screen.blit(exit_btn_img, (exit_rect.x + 5, exit_rect.y))
        if mouse_click:
            running_menu = False
    else:
        screen.blit(exit_btn_img, exit_rect)

    pygame.display.update()

pygame.quit()
