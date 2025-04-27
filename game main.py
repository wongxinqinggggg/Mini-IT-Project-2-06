import pygame
import time
from Features import MiniGame1, MiniGame4

# === Setup ===
pygame.init()
pygame.mixer.init()

# === Music ===
pygame.mixer.music.load("Assets/Audio/background.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# === Screen and Fonts ===
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Money, No Life")

large_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 32)
middle_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 25)
font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 20)
small_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 14)

# === Colors ===
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
HIGHLIGHT = (255, 215, 0)
GREEN = (0, 255, 0)
TICK_COLOR = (0, 200, 0)
WARNING_COLOR = (255, 0, 0)
BUTTON_COLOR = (220, 220, 220)
WHITE = (255, 255, 255)

# === Load Images ===
bg_img = pygame.transform.scale(pygame.image.load("Assets/Images/main.png").convert(), (WIDTH, HEIGHT))
map_img = pygame.transform.scale(pygame.image.load("Assets/Images/final_map.png").convert(), (WIDTH, HEIGHT))

# === Game Variables ===
player_name = ''
selected_character = None
MAXHP, MAXMP = 1000, 1000
hp, mp = 123, 456
active_input = False
warning_message = ''
game_state = "intro" 
mg_state = None
show_intro_message = True  # False — intro message will display
typing_done = False        # Added this flag to control when typing is done
dragging = False
running = True

# Cursor blinking
cursor_visible = True
cursor_timer = 0
cursor_interval = 500  # milliseconds

# === UI Elements ===
male_box = pygame.Rect(250, 330, 40, 40)
female_box = pygame.Rect(500, 330, 40, 40)
start_button = pygame.Rect(295, 455, 210, 60)

# === Intro Message ===
intro_message = (
    f"WELCOME  {player_name}In this game, you need money to survive. "
    "Explore different rooms to work and earn cash. To restore your energy, "
    "you can either buy food or drinks, which is faster, or go back home to sleep, "
    "which takes more time. So plan wisely, keep your energy up, and make the most of your day!"
)

# Typing effect parameters
typed_message = ""
typing_index = 0
typing_speed = 50  # Milliseconds between each character

# === Function to render wrapped text ===
def draw_text_box(surface, message, font, color, box_rect, padding=10, line_height=20):
    words = message.split(' ')
    lines = []
    line = ''

    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < box_rect.width - 2 * padding:  line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    pygame.draw.rect(surface, WHITE, box_rect)
    pygame.draw.rect(surface, BLACK, box_rect, 3)

    for i, l in enumerate(lines):
        line_surface = font.render(l.strip(), True, color)
        surface.blit(line_surface, (box_rect.x + padding, box_rect.y + padding + i * line_height))

# === Function to update hp and mp ===
def update_stats(hpchange, mpchange):
    global hp, mp

    if hpchange: hp = min(max(hp + hpchange, 0), MAXHP)
    if mpchange: mp = min(max(mp + mpchange, 0), MAXMP)

# === Function to display hp and mp ===
def display_stats(hp, mp):
    statsbar = pygame.image.load("Assets/Images/MAIN_Statsbar.png").convert_alpha()

    hpsurf = large_font.render(hp.zfill(4), False, 'Black')
    hprect = pygame.Rect(95, 30, 100, 50)
    mpsurf = large_font.render(mp.zfill(4), False, 'Black')
    mprect = pygame.Rect(95, 105, 100, 50)
    screen.blit(statsbar, (0,0))

    screen.blit(hpsurf, hprect)
    screen.blit(mpsurf, mprect)

# === Main Loop ===
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    dt = clock.tick(60)

    # Pause music if muted
    if not pygame.mixer.music.get_volume(): pygame.mixer.music.pause()

    # Update cursor blinking
    cursor_timer += dt
    if cursor_timer >= cursor_interval:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    # === Intro State ===
    if game_state == "intro":
        screen.blit(bg_img, (0, 0))

        name_color = BLACK if player_name else GRAY
        display_name = player_name if player_name else "Enter Your Name"

        if active_input and cursor_visible: display_name += "|"

        name_surface = font.render(display_name, True, name_color)
        screen.blit(name_surface, (230, 215))

        # Character Selection Boxes
        pygame.draw.rect(screen, BLACK, male_box, 3)
        pygame.draw.rect(screen, BLACK, female_box, 3)

        if selected_character == 'male':
            pygame.draw.rect(screen, HIGHLIGHT, male_box, 3)
            pygame.draw.line(screen, TICK_COLOR, (260, 350), (270, 360), 3)
            pygame.draw.line(screen, TICK_COLOR, (270, 360), (285, 340), 3)

        elif selected_character == 'female':
            pygame.draw.rect(screen, HIGHLIGHT, female_box, 3)
            pygame.draw.line(screen, TICK_COLOR, (510, 350), (520, 360), 3)
            pygame.draw.line(screen, TICK_COLOR, (520, 360), (535, 340), 3)

        # Start Button
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        pygame.draw.rect(screen, BLACK, start_button, 4)

        if player_name and selected_character:  pygame.draw.rect(screen, HIGHLIGHT, start_button, 4)

        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (start_button.x + 60, start_button.y + 15))

        if warning_message:
            warning_text = font.render(warning_message, True, WARNING_COLOR)
            screen.blit(warning_text, (150, 560))

    elif game_state == "game":
        screen.blit(map_img, (0, 0))

        # Typing effect for intro message
        if show_intro_message:
            if not typing_done:
                if typing_index < len(intro_message):
                    typed_message += intro_message[typing_index]
                    typing_index += 1
                else: typing_done = True

            # Draw message box
            dialog_box_rect = pygame.Rect(30, 40, 740, 180)
            draw_text_box(screen, typed_message, small_font, BLACK, dialog_box_rect, padding=15, line_height=22)

    # == Lanching Mini game 1 ==
    elif game_state == "mg1":   
        MG1 = MiniGame1.MG1(screen, WIDTH, HEIGHT, mg_state)
        mg_state = MG1.getstate()

        if mg_state == "mainpage": display_stats(str(hp), str(mp))
        elif mg_state == "instruc": MG1.instruc(middle_font)

        elif mg_state == "newgame":
            if hp <= 10:
                msg = "Insufficient energy"
                xpos, ypos = 100, 480
                mg_state = "displaymsg"
                continue 

            update_stats(-10, None)
            plates = 0
            start_time, time_passed = time.time(), 0
            new_plate = True
            stains = pygame.sprite.Group()      # Initialize sprite group
            mg_state = "game"

        elif mg_state == "game":
            time_passed = (time.time() - start_time)
            plates, new_plate = MG1.game(plates, new_plate, (10 - time_passed), stains, large_font)
            mg_state = MG1.getstate()
            stains, win = MG1.checkcond()

        elif mg_state == "resume":
            start_time = time.time() - time_passed
            mg_state = "game"

        elif mg_state == "end":
            if win:
                update_stats(None, +10)
                msg = "You win!"
            else: msg = "You lose"

            xpos, ypos = 280, 480
            mg_state = "end"

        elif mg_state == "displaymsg": 
            MG1.displaymsg(msg, xpos, ypos, large_font)
            display_stats(str(hp), str(mp))

    # === Event Handling ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if game_state == "intro":
                active_input = True

                if male_box.collidepoint(mouse_x, mouse_y): selected_character = 'male'

                elif female_box.collidepoint(mouse_x, mouse_y):   selected_character = 'female'

                elif start_button.collidepoint(mouse_x, mouse_y):
                    if player_name and selected_character:
                        game_state = "game"
                        warning_message = ''
                        show_intro_message = True
                        typing_done = False
                        typed_message = ""
                        typing_index = 0
                    else:   warning_message = "Enter name and choose a character!"

            elif game_state == "game" and show_intro_message and typing_done:   show_intro_message = False

            elif game_state == "mg1":   
                dragging = MG1.eventhandler(mouse_x, mouse_y)
                mg_state = MG1.getstate()

                if mg_state == "game": stains, win = MG1.checkcond()
                elif not mg_state:    game_state = "game"

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if game_state == "mg1" and dragging: dragging = MG1.eventhandler(mouse_x, mouse_y, dragging)

        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state == "mg1":  dragging = False

        elif event.type == pygame.KEYDOWN:
            if game_state == "intro" and event.key == pygame.K_BACKSPACE: player_name = player_name[:-1]

            elif game_state == "intro" and len(player_name) < 30: player_name += event.unicode

            elif event.key == pygame.K_RETURN and game_state == "game" and show_intro_message and typing_done:
                show_intro_message = False
            
            # Placeholder for launching minigames
            elif event.key == pygame.K_1: 
                game_state = "mg1"
                mg_state = "mainpage"

    pygame.display.flip()

pygame.quit()