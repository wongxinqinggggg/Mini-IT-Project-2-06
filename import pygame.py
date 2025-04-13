import pygame

pygame.init()

# Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Money, No Life")

# Load background images
bg_img = pygame.image.load("main.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

map_img = pygame.image.load("map.png").convert()
map_img = pygame.transform.scale(map_img, (WIDTH, HEIGHT))

# Font and colors
font = pygame.font.Font("PressStart2P.ttf", 20)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
HIGHLIGHT = (255, 215, 0)
GREEN = (0, 255, 0)
TICK_COLOR = (0, 200, 0)

# Game state
player_name = ''
selected_character = None
active = False
warning_message = ''
game_state = "intro"
running = True

while running:
    if game_state == "intro":
        screen.blit(bg_img, (0, 0))

        # Player name text
        name_surface = font.render(player_name if player_name else "Enter Your Name", True, BLACK if player_name else GRAY)
        screen.blit(name_surface, (230, 215))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Character boxes (adjusted)
        male_box = pygame.Rect(270, 395, 40, 40)
        female_box = pygame.Rect(490, 395, 40, 40)

        pygame.draw.rect(screen, BLACK, male_box, 3)
        pygame.draw.rect(screen, BLACK, female_box, 3)

        # Tick and highlight
        if selected_character == 'male':
            pygame.draw.rect(screen, HIGHLIGHT, male_box, 3)
            pygame.draw.line(screen, TICK_COLOR, (275, 415), (285, 425), 3)
            pygame.draw.line(screen, TICK_COLOR, (285, 425), (300, 400), 3)

        elif selected_character == 'female':
            pygame.draw.rect(screen, HIGHLIGHT, female_box, 3)
            pygame.draw.line(screen, TICK_COLOR, (495, 415), (505, 425), 3)
            pygame.draw.line(screen, TICK_COLOR, (505, 425), (520, 400), 3)

        # Start button (centered)
        start_button = pygame.Rect(295, 485, 210, 60)
        pygame.draw.rect(screen, (220, 220, 220), start_button)
        pygame.draw.rect(screen, BLACK, start_button, 4)

        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (start_button.x + 60, start_button.y + 15))

        # Highlight if ready
        if player_name and selected_character:
            pygame.draw.rect(screen, HIGHLIGHT, start_button, 4)

        if warning_message:
            warning_text = font.render(warning_message, True, (255, 0, 0))
            screen.blit(warning_text, (150, 560))

    elif game_state == "game":
        screen.blit(map_img, (0, 0))
        welcome_text = font.render(f"Welcome, {player_name}!", True, BLACK)
        screen.blit(welcome_text, (250, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if game_state == "intro":
                active = True

                if male_box.collidepoint(mouse_x, mouse_y):
                    selected_character = 'male'

                if female_box.collidepoint(mouse_x, mouse_y):
                    selected_character = 'female'

                if start_button.collidepoint(mouse_x, mouse_y):
                    if player_name and selected_character:
                        game_state = "game"
                        warning_message = ''
                    else:
                        warning_message = "Enter name and choose a character!"

        if game_state == "intro" and event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif len(player_name) < 30:
                player_name += event.unicode

    pygame.display.flip()

pygame.quit()