import pygame
import json
import time
import random
import os

# === SETUP ===
pygame.init()
pygame.mixer.init()

# === SCREEN ===
WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Money, No Life")

# === FONTS ===
font = pygame.font.Font("PressStart2P.ttf", 20)
small_font = pygame.font.Font("PressStart2P.ttf", 14)
FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 26)

# === MUSIC ===
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# === COLORS ===
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 215, 0)
TICK_COLOR = (0, 200, 0)
WARNING_COLOR = (255, 0, 0)
BUTTON_COLOR = (220, 220, 220)

# === IMAGES ===
bg_img = pygame.transform.scale(pygame.image.load("main.png").convert(), (WIDTH, HEIGHT))
map_img = pygame.image.load("final_map.png").convert()
main_element_img = pygame.image.load("main_element.png").convert_alpha()
MAP_WIDTH, MAP_HEIGHT = 800, 800

# === TILEMAP BLOCKING ===
def load_tilemap(filename):
    tilemap = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(char) for char in line.strip()]
            tilemap.append(row)
    return tilemap

tilemap = load_tilemap("map_tiled.txt")
blocking_tiles = [1]
TILE_SIZE = 16
collision_rects = []
for y, row in enumerate(tilemap):
    for x, tile in enumerate(row):
        if tile in blocking_tiles:
            collision_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# === SAVE/LOAD ===
SAVE_FILE = "save_data.json"

def save_game(player_name, selected_character):
    data = {"player_name": player_name, "selected_character": selected_character}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return data
    else:
        print("No save file found. Starting a new game.")
        return None  

def reset_game():
    global warning_message
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        warning_message = "Save file deleted!"
    else:
        warning_message = "No save file to delete!"

# === GAME VARIABLES ===
player_name = ''
selected_character = None
active_input = False
warning_message = ''
game_state = "intro"
show_intro_message = True
typing_done = False
running = True
show_minigame_prompt = False
minigame_active = False
minigame_trigger_rect = pygame.Rect(690, 650, 50, 50)

# Numerical values for energy and money
value1 = 100  # Energy
value2 = 0    # Money

# CURSOR
cursor_visible = True
cursor_timer = 0
cursor_interval = 500

# UI ELEMENTS
male_box = pygame.Rect(330, 325, 40, 40)
female_box = pygame.Rect(650, 325, 40, 40)
start_button = pygame.Rect(100, 455, 200, 60)
continue_button = pygame.Rect(400, 455, 200, 60)
reset_button = pygame.Rect(700, 455, 200, 60)
typed_message = ""
typing_index = 0

# === PLAYER ===
character_paths = {"male": "male/", "female": "female/"}

def load_player_images(character_folder):
    path = character_paths[character_folder]
    return {
        "idle": {
            "w": pygame.image.load(path + f"{character_folder}_idle_up.png").convert_alpha(),
            "s": pygame.image.load(path + f"{character_folder}_idle_down.png").convert_alpha(),
            "a": pygame.image.load(path + f"{character_folder}_idle_left.png").convert_alpha(),
            "d": pygame.image.load(path + f"{character_folder}_idle_right.png").convert_alpha()
        },
        "walk": {
            "w": [
                pygame.image.load(path + f"{character_folder}_walk_up_1.png").convert_alpha(),
                pygame.image.load(path + f"{character_folder}_walk_up_2.png").convert_alpha()
            ],
            "s": [
                pygame.image.load(path + f"{character_folder}_walk_down_1.png").convert_alpha(),
                pygame.image.load(path + f"{character_folder}_walk_down_2.png").convert_alpha()
            ],
            "a": [
                pygame.image.load(path + f"{character_folder}_walk_left_1.png").convert_alpha(),
                pygame.image.load(path + f"{character_folder}_idle_left.png").convert_alpha()
            ],
            "d": [
                pygame.image.load(path + f"{character_folder}_walk_right_1.png").convert_alpha(),
                pygame.image.load(path + f"{character_folder}_idle_right.png").convert_alpha()
            ]
        }
    }

# === CAMERA ===
def get_camera_offset():
    camera_x = max(0, min(player_x - WIDTH // 2, MAP_WIDTH - WIDTH))
    camera_y = max(0, min(player_y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    return camera_x, camera_y

def is_near(player_x, player_y, npc_x, npc_y, distance=50):
    return abs(player_x - npc_x) < distance and abs(player_y - npc_y) < distance

def draw_popup(screen, message, font, color=(0, 0, 0), bg_color=(255, 255, 255), border_color=(0, 0, 0), padding=20, line_spacing=5):
    screen_width, screen_height = screen.get_size()
    box_margin = 40
    box_width = screen_width - 2 * box_margin
    box_height = 160
    box_x = box_margin
    box_y = screen_height - box_height - 20
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    # Wrap text
    words = message.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < box_width - 2 * padding:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + ' '
    lines.append(line.strip())

    # Transparent background surface
    popup_surface = pygame.Surface((box_width, box_height))
    popup_surface.set_alpha(230)  # Adjust transparency
    popup_surface.fill(bg_color)

    # Border
    pygame.draw.rect(popup_surface, border_color, popup_surface.get_rect(), 4)

    # Draw text
    line_height = font.get_height() + line_spacing
    y_offset = padding
    for l in lines:
        if y_offset + line_height > box_height - padding:
            break
        text_surf = font.render(l, True, color)
        popup_surface.blit(text_surf, (padding, y_offset))
        y_offset += line_height

    # Finally blit to main screen (overlapping everything)
    screen.blit(popup_surface, (box_x, box_y))

characters = [
    {
        "img": pygame.transform.scale(pygame.image.load("restaurant.png"), (80, 80)),
        "x": 770,
        "y": 130,
        "description": "Welcome to the restaurant, where the scent of sizzling meals meets the sound of scrubbing dishes. "
                       "Ready to roll up your sleeves? Take on the washing challenge and earn some well-deserved money."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("grocerry.png"), (100, 100)),  
        "x": 600,
        "y": 660,
        "description": "Bustling with customers and chaos. But today, you are not shopping — you are working. "
                       "Step behind the counter and become the cashier of the day."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("cyber_cafe.png"), (80, 80)),
        "x": 90,
        "y": 665,
        "description": "This is the teenagers' zone, and the only way to win here is to type like lightning. "
                       "Put your speed and accuracy to the test and rake in digital dough with each correct keystroke."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("Food_stall.png"), (65, 65)),
        "x": 750,
        "y": 353,
        "description": "Ready to bring you back to life. Choose your meal, sit back, and recover the energy you need to keep going. "
                       "After all, a hardworking spirit needs fuel to thrive."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("lazapee.png"), (80, 80)),
        "x": 60,
        "y": 170,
        "description": "This is not just another shop — it is a gateway to passive income. "
                       "Invest wisely, and your money will work while you rest. "
                       "In this town, fortune favors the bold... and the smart."
    }
]

# FUNCTION TO GENERATE INTRO MESSAGE
def generate_intro_message(name):
    return (
        f"WELCOME {name.upper()}! In this game, you need money to survive. "
        "Explore different rooms to work and earn cash. To restore your energy, "
        "you can either buy food or drinks, which is faster, or go back home to sleep, "
        "which takes more time. So plan wisely, keep your energy up, and make the most of your day!"
    )

# === RENDER WRAPPED TEXT ===
def draw_text_box(surface, message, font, color, box_rect, padding=10, line_height=20):
    words = message.split(' ')
    lines = []
    line = ''

    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < box_rect.width - 2 * padding:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    pygame.draw.rect(surface, WHITE, box_rect)
    pygame.draw.rect(surface, BLACK, box_rect, 3)

    for i, l in enumerate(lines):
        line_surface = font.render(l.strip(), True, color)
        surface.blit(line_surface, (box_rect.x + padding, box_rect.y + padding + i * line_height))

# === MINIGAME PROMPT ===
def draw_minigame_prompt():
    # Create a semi-transparent background
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    screen.blit(s, (0, 0))
    
    # Draw the prompt box
    prompt_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 80, 350, 100)
    pygame.draw.rect(screen, WHITE, prompt_rect)
    pygame.draw.rect(screen, BLACK, prompt_rect, 3)
    
    # Draw the buttons
    play_button = pygame.Rect(prompt_rect.x + 130, prompt_rect.y + 30, 80, 40)
    
    pygame.draw.rect(screen, BUTTON_COLOR, play_button)
    pygame.draw.rect(screen, BLACK, play_button, 2)
    screen.blit(font.render("PLAY", True, BLACK), (play_button.x + 0, play_button.y + 10))
  
    screen.blit(font.render("Start Minigame?", True, BLACK), (prompt_rect.x + 25, prompt_rect.y + 10))
    
    return play_button

# Initial positions
player_x = 500
player_y = 400
player_speed = 1.5
player_direction = "s"
walk_frame = 0
walk_timer = 0
walk_delay = 200
player_imgs = load_player_images("male")

clock = pygame.time.Clock()
while running:
    dt = clock.tick(60)
    screen.fill(WHITE)
    cursor_timer += dt
    if cursor_timer >= cursor_interval:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    if game_state == "intro":
        # Intro Screen Logic
        screen.blit(bg_img, (0, 0))
        name_color = BLACK if player_name else GRAY
        display_name = player_name if player_name else "ENTER YOUR NAME"
        if active_input and cursor_visible:
            display_name += "|"
        screen.blit(font.render(display_name, True, name_color), (380, 210))

        pygame.draw.rect(screen, BLACK, male_box, 3)
        pygame.draw.rect(screen, BLACK, female_box, 3)
        if selected_character == 'male':
            pygame.draw.rect(screen, HIGHLIGHT, male_box, 3)
            pygame.draw.line(screen, TICK_COLOR, (340, 345), (345, 355), 3)
            pygame.draw.line(screen, TICK_COLOR, (345, 355), (360, 335), 3)
        elif selected_character == 'female':
            pygame.draw.rect(screen, HIGHLIGHT, female_box, 3)
            pygame.draw.line(screen, TICK_COLOR, (660, 345), (665, 355), 3)
            pygame.draw.line(screen, TICK_COLOR, (665, 355), (680, 335), 3)

        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        pygame.draw.rect(screen, HIGHLIGHT if player_name and selected_character else BLACK, start_button, 4)
        screen.blit(font.render("Start", True, BLACK), (start_button.x + 55, start_button.y + 20))

        pygame.draw.rect(screen, BUTTON_COLOR, continue_button)
        pygame.draw.rect(screen, BLACK, continue_button, 4)
        screen.blit(font.render("Continue", True, BLACK), (continue_button.x + 25, continue_button.y + 20))

        pygame.draw.rect(screen, BUTTON_COLOR, reset_button)
        pygame.draw.rect(screen, BLACK, reset_button, 4)
        screen.blit(font.render("Reset", True, BLACK), (reset_button.x + 55, reset_button.y + 20))

        if warning_message:
            screen.blit(font.render(warning_message, True, WARNING_COLOR), (180, 530))

    elif game_state == "game":
        camera_x, camera_y = get_camera_offset()
        screen.fill((0, 0, 0))
        screen.blit(map_img, (0 - camera_x, 0 - camera_y))  # Apply camera offset
        
        # Draw main_element image
        screen.blit(main_element_img, (0, 0))
        
        # Draw the numerical values (energy and money)
        screen.blit(font.render(str(value1), True, BLACK), (80, 20))
        screen.blit(font.render(str(value2), True, BLACK), (80, 70))

        # Check if player is in the minigame trigger area
        player_rect = pygame.Rect(player_x, player_y, 32, 32)
        if player_rect.colliderect(minigame_trigger_rect):
            show_minigame_prompt = True
        else:
            show_minigame_prompt = False

        if show_minigame_prompt:
            play_button = draw_minigame_prompt()

        # EFFECT FOR INTRO MESSAGE
        if show_intro_message:
            if not typing_done:
                if typing_index < len(intro_message):
                    typed_message += intro_message[typing_index]
                    typing_index += 1
                else:
                    typing_done = True

            # DRAW MESSAGE BOX
            dialog_box_rect = pygame.Rect(110, 380, 800, 180)
            draw_text_box(screen, typed_message, small_font, BLACK, dialog_box_rect, padding=15, line_height=22)

        # Player movement 
        old_x, old_y = player_x, player_y
        keys = pygame.key.get_pressed()
        moving = False
        new_x, new_y = player_x, player_y  # New position after moving

        if keys[pygame.K_w]:
            new_y -= player_speed
            player_direction = "w"
            moving = True
        if keys[pygame.K_s]:
            new_y += player_speed
            player_direction = "s"
            moving = True
        if keys[pygame.K_a]:
            new_x -= player_speed
            player_direction = "a"
            moving = True
        if keys[pygame.K_d]:
            new_x += player_speed
            player_direction = "d"
            moving = True

        # Create player's target rectangle for collision checking
        player_rect = pygame.Rect(new_x, new_y, player_imgs["idle"][player_direction].get_width(), player_imgs["idle"][player_direction].get_height())
        for rect in collision_rects:
            if player_rect.colliderect(rect):
                moving = False  # Stop movement on collision
                break

        # Update player position if no collision
        if moving:
            player_x, player_y = new_x, new_y

        # Update animation frame
        if moving:
            if pygame.time.get_ticks() - walk_timer > walk_delay:
                walk_frame = (walk_frame + 1) % len(player_imgs["walk"][player_direction])
                walk_timer = pygame.time.get_ticks()
        else:
            walk_frame = 0

        # Update NPC and draw player
        current_img = player_imgs["walk"][player_direction][walk_frame] if moving else player_imgs["idle"][player_direction]
        screen.blit(current_img, (player_x - camera_x, player_y - camera_y))

        for character in characters:
            screen.blit(character["img"], (character["x"] - camera_x, character["y"] - camera_y))
            if is_near(player_x, player_y, character["x"], character["y"]):
                draw_popup(screen, character["description"], font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "intro":
                active_input = True
                if male_box.collidepoint(event.pos): selected_character = 'male'
                if female_box.collidepoint(event.pos): selected_character = 'female'
                if start_button.collidepoint(event.pos):
                    if start_button.collidepoint(event.pos):
                        if player_name and selected_character:
                            save_game(player_name, selected_character)
                    if player_name and selected_character:
                        intro_message = generate_intro_message(player_name)
                        show_intro_message = True
                        typing_done = False
                        typed_message = ""
                        typing_index = 0
                        player_imgs = load_player_images(selected_character)  # Load correct character assets
                        game_state = "game"
                    else:
                        warning_message = "Enter name and choose a character!"  # Only show this when conditions aren't met
                if continue_button.collidepoint(event.pos):
                    saved_data = load_game()
                    if saved_data:
                        player_name = saved_data["player_name"]
                        selected_character = saved_data["selected_character"]
                        game_state = "game"
                        warning_message = ''
                        show_intro_message = False
                        typing_done = False
                        typed_message = ""
                        typing_index = 0
                        player_imgs = load_player_images(selected_character)
                    else:
                        warning_message = "No saved game found!"
                if reset_button.collidepoint(event.pos): reset_game()
            elif game_state == "game" and show_intro_message and typing_done:
                show_intro_message = False
            elif game_state == "game" and show_minigame_prompt:
                mouse_pos = pygame.mouse.get_pos()
                play_button = draw_minigame_prompt()
                if play_button.collidepoint(mouse_pos):
                    minigame_active = True
                    show_minigame_prompt = False
                    # Decrease energy by 20 when PLAY button is clicked
                    value1 = max(0, value1 - 20)

        if event.type == pygame.KEYDOWN:
            if game_state == "intro":
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 30:
                    player_name += event.unicode

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = True  # 点击屏幕激活输入
                
            if event.type == pygame.KEYDOWN:
                if game_state == "intro":
                    # 处理退格键和字符输入
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif len(player_name) < 30:
                        player_name += event.unicode

    pygame.display.flip()

    # Run minigame if activated
    if minigame_active:
        # Save current display settings
        original_screen = screen
        original_caption = pygame.display.get_caption()
        # === MUSIC ===
        pygame.mixer.music.load("Minigame2_bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        try:
            # Initialize minigame
            minigame_screen = pygame.display.set_mode((1024, 576))
            pygame.display.set_caption("Supermarket Cashier Game")
            
            # Load images with error handling
            def load_and_scale(image_path):
                try:
                    return pygame.transform.scale(pygame.image.load(image_path).convert(), (1024, 576))
                except:
                    print(f"Error loading image: {image_path}")
                    return pygame.Surface((1024, 576))
            
            try:
                menu_img = load_and_scale("c:/Users/User/Desktop/MINI IT PROJECT/Mini-IT-Project-2-06/MG2/MG2-Menu.png")
                instruction_img = load_and_scale("c:/Users/User/Desktop/MINI IT PROJECT/Mini-IT-Project-2-06/MG2/MG2-Instructions.png")
                success_img = load_and_scale("c:/Users/User/Desktop/MINI IT PROJECT/Mini-IT-Project-2-06/MG2/MG2-Success.png")
                fail_img = load_and_scale("c:/Users/User/Desktop/MINI IT PROJECT/Mini-IT-Project-2-06/MG2/MG2-Fail.png")
                pause_button_img = pygame.image.load("main_element2.png").convert_alpha()
                pause_button_img = pygame.transform.scale(pause_button_img, (80, 80))
                
                receipt_imgs = []
                for i in range(1, 11):
                    try:
                        img = load_and_scale(f"c:/Users/User/Desktop/MINI IT PROJECT/Mini-IT-Project-2-06/MG2/MG2-Game{i}.png")
                        receipt_imgs.append(img)
                    except:
                        print(f"Error loading receipt image {i}")
                        receipt_imgs.append(pygame.Surface((1024, 576)))
            except Exception as e:
                print(f"Error loading minigame assets: {e}")
                # Create placeholders if loading fails
                menu_img = pygame.Surface((1024, 576))
                instruction_img = pygame.Surface((1024, 576))
                success_img = pygame.Surface((1024, 576))
                fail_img = pygame.Surface((1024, 576))
                pause_button_img = pygame.Surface((80, 80))
                pause_menu_img = pygame.Surface((400, 300))
                receipt_imgs = [pygame.Surface((1024, 576)) for _ in range(10)]
            
            # Minigame variables
            minigame_state = "menu"
            current_receipt = None
            order_left = 5
            time_left = 30
            input_text = ""
            correct_amount = 0
            paused = False
            pause_time = 0
            
            # Define buttons
            pause_button = pygame.Rect(1024 - 80, 15, 80, 80)  # Top-right corner
            resume_button = pygame.Rect(1024//2 - 150, 500//2, 300, 60)
            restart_button = pygame.Rect(1024//2 - 150, 500//2 + 80, 300, 60)
            quit_button = pygame.Rect(1024//2 - 150, 500//2 + 160, 300, 60)
            
            receipt_answers = {
                0: 3.50, 1: 8.00, 2: 6.00, 3: 7.50, 4: 8.30,
                5: 45.10, 6: 15.20, 7: 66.00, 8: 1.30, 9: 9.00
            }
            
            TIMER_EVENT = pygame.USEREVENT + 1
            pygame.time.set_timer(TIMER_EVENT, 1000)
            
            # Define return button
            return_button = pygame.Rect(20, 20, 120, 50)  # Positioned at top-left corner
            
            def reset_minigame():
                global order_left, time_left, input_text
                order_left = 5
                time_left = 30
                input_text = ""
                next_order()
            
            def next_order():
                global current_receipt, correct_amount, input_text
                idx = random.randint(0, 9)
                current_receipt = receipt_imgs[idx]
                correct_amount = receipt_answers[idx]
                input_text = ""
            
            # Minigame main loop
            running_minigame = True
            while running_minigame:
                dt = clock.tick(60)
                minigame_screen.fill((255, 255, 255))
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running_minigame = False
                        running = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if minigame_state == "menu":
                            # Start game button (400-600 x 300-480)
                            if 400 <= mouse_pos[0] <= 600 and 300 <= mouse_pos[1] <= 480:
                                reset_minigame()
                                minigame_state = "playing"
                            # Instructions button (924-1004 x 20-100)
                            elif 924 <= mouse_pos[0] <= 1004 and 20 <= mouse_pos[1] <= 100:
                                minigame_state = "instruction"
                            # Return button (20-120 x 20-60)
                            elif return_button.collidepoint(mouse_pos):
                                running_minigame = False
                        
                        elif minigame_state == "instruction":
                            # Click anywhere to return
                            minigame_state = "menu"
                        
                        elif minigame_state == "playing" and not paused:
                            # Pause button
                            if pause_button.collidepoint(mouse_pos):
                                paused = True
                                pause_time = time_left  # Save current time
                                pygame.time.set_timer(TIMER_EVENT, 0)  # Pause timer
                        
                        elif paused:
                            # Pause menu buttons
                            if resume_button.collidepoint(mouse_pos):
                                paused = False
                                time_left = pause_time  # Restore saved time
                                pygame.time.set_timer(TIMER_EVENT, 1000)  # Resume timer
                            elif restart_button.collidepoint(mouse_pos):
                                paused = False
                                reset_minigame()
                                minigame_state = "menu"
                                pygame.time.set_timer(TIMER_EVENT, 1000)
                            elif quit_button.collidepoint(mouse_pos):
                                running_minigame = False
                    
                    if event.type == pygame.KEYDOWN and minigame_state == "playing" and not paused:
                        if event.key == pygame.K_RETURN:
                            try:
                                if abs(float(input_text) - correct_amount) < 0.01:
                                    order_left -= 1
                                    if order_left == 0:
                                        minigame_state = "success"
                                        # === MUSIC ===
                                        pygame.mixer.music.load("success.mp3")
                                        pygame.mixer.music.set_volume(0.5)
                                        pygame.mixer.music.play(1)
                                        # Increase value2 by 50 when minigame is successful
                                        value2 += 50

                                    else:
                                        next_order()
                                else:
                                    minigame_state = "fail"
                                    pygame.mixer.music.load("fail.mp3")
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(1)
                            except:
                                minigame_state = "fail"
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if event.unicode.isdigit() or event.unicode == '.':
                                input_text += event.unicode
                    
                    if event.type == TIMER_EVENT and minigame_state == "playing" and not paused:
                        time_left -= 1
                        if time_left <= 0:
                            minigame_state = "fail"
                
                # Render minigame states
                if minigame_state == "menu":
                    minigame_screen.blit(menu_img, (0, 0))
                
                elif minigame_state == "instruction":
                    minigame_screen.blit(instruction_img, (0, 0))
                
                elif minigame_state == "playing":
                    minigame_screen.blit(current_receipt, (0, 0))
                    
                    # Draw pause button
                    minigame_screen.blit(pause_button_img, (pause_button.x, pause_button.y))
                    
                    # Display orders left
                    order_text = font.render(f"Orders Left: {order_left}", True, (0, 0, 0))
                    minigame_screen.blit(order_text, (20, 40))
                    
                    # Display time left
                    time_text = font.render(f"Time: {time_left}", True, (0, 0, 0))
                    minigame_screen.blit(time_text, (1024 - 250, 40))
                    
                    # Display input box
                    input_surface = font.render(input_text, True, (0, 0, 0))
                    input_rect = input_surface.get_rect(center=(1024//2, 576-50))
                    pygame.draw.rect(minigame_screen, (200, 200, 200), input_rect.inflate(20, 20))
                    minigame_screen.blit(input_surface, input_rect)
                    
                    # Draw pause menu if paused
                    if paused:
                        # Semi-transparent overlay
                        s = pygame.Surface((1024, 576), pygame.SRCALPHA)
                        s.fill((0, 0, 0, 128))
                        minigame_screen.blit(s, (0, 0))
                        
                        
                        # Draw buttons
                        pygame.draw.rect(minigame_screen, BUTTON_COLOR, resume_button)
                        pygame.draw.rect(minigame_screen, BLACK, resume_button, 2)
                        minigame_screen.blit(font.render("RESUME", True, BLACK), (resume_button.x + 100, resume_button.y + 20))
                        
                        pygame.draw.rect(minigame_screen, BUTTON_COLOR, restart_button)
                        pygame.draw.rect(minigame_screen, BLACK, restart_button, 2)
                        minigame_screen.blit(font.render("RESTART", True, BLACK), (restart_button.x + 100, restart_button.y + 20))
                        
                        pygame.draw.rect(minigame_screen, BUTTON_COLOR, quit_button)
                        pygame.draw.rect(minigame_screen, BLACK, quit_button, 2)
                        minigame_screen.blit(font.render("QUIT", True, BLACK), (quit_button.x + 120, quit_button.y + 20))
                
                elif minigame_state == "success":
                    minigame_screen.blit(success_img, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    running_minigame = False
                
                elif minigame_state == "fail":
                    minigame_screen.blit(fail_img, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    running_minigame = False
                
                pygame.display.update()
        
        finally:
            # Restore original game display
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption(original_caption[0])
            minigame_active = False
            pygame.time.set_timer(TIMER_EVENT, 0)  # Stop timer
            # Restore main game music
            pygame.mixer.music.load("background.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

pygame.quit()
