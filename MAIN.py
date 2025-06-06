import pygame
import json
import time
import random
import os
from MG3.MG_3 import run_MG3
from Features import Functions, MiniGame1, MiniGame4

# === SETUP ===
pygame.init()
pygame.mixer.init()
floating_texts = [] 

# === SCREEN ===
WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Money, No Life")
clock = pygame.time.Clock()

# === FONTS ===
font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 20)
small_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 14)
FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 26)
xlarge_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 38)
large_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 32)
middle_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 26)
xsmall_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 8)

# === MUSIC ===
pygame.mixer.music.load("Assets/Audio/background.mp3")
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
bg_img = pygame.transform.scale(pygame.image.load("Assets/Images/Assets/Images/main.png").convert(), (WIDTH, HEIGHT))
map_img = pygame.image.load("Assets/Images/final_map.png").convert()
MAP_WIDTH, MAP_HEIGHT = ((800, 800))

# === TILEMAP BLOCKING ===
def load_tilemap(filename):
    tilemap = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(char) for char in line.strip()]
            tilemap.append(row)
    return tilemap

tilemap = load_tilemap("map_tiled.txt")
blocking_tiles = [1, 2]
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

Functions.initialize_stats()
vm_level = [0, 0]   # Vending machine level for Mini Game 4
vm_income = [[1, 2, 3], [5, 6, 7]]
vm_buyingprices = [[300, 400, 500], [800, 900, 1000]]
VM1, VM2 = pygame.USEREVENT + 1, pygame.USEREVENT + 2
NOTI = Functions.Notifications(screen, vm_buyingprices, vm_income)
INVENTORY = Functions.Inventory(screen, clock)
mg_var_dict = {}
store_var_dict = {'mg_state': "mainpage", 'prev_state': None, 'dragging': None}
mg_var_dict = {}
mg1_var_dict = {'mg_state': "mainpage", 'time_passed': 0, 'msg': None, 'new_plate': True, 
                'plates': 0, 'stains': None, 'dragging': None, 'prev_state': None,
                'Lfont': large_font, 'Mfont': middle_font, 'XLfont': xlarge_font, 'fade': None}
mg4_var_dict = {'mg_state': "mainpage", 'vm_level': vm_level, 'vm_income': vm_income, 
                'VM_EVENT': [VM1, VM2], 'Sfont': small_font, 'XSfont': xsmall_font, 
                'prev_state': None, 'dragging': None, 'noti': NOTI}

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
sprite_width, sprite_height = 32, 64
def get_sprite(x, y):
    spritesheet = pygame.image.load("Assets/Sprites/spritesheet.png").convert_alpha()
    uppersurf = pygame.Surface((sprite_width, sprite_height/2), pygame.SRCALPHA).convert_alpha()
    uppersurf.blit(spritesheet, (0,0), (x*sprite_width, y*sprite_height, sprite_width, sprite_height/2))
    lowersurf = pygame.Surface((sprite_width, sprite_height/2), pygame.SRCALPHA).convert_alpha()
    lowersurf.blit(spritesheet, (0,0), (x*sprite_width, y*sprite_height+sprite_height/2, sprite_width, sprite_height/2))
    return [uppersurf, lowersurf]


def load_player_images(character):
    if character == "female": y = 0
    elif character == "male": y = 1
    return {"idle": {"w": get_sprite(3, y), "s": get_sprite(0, y), 
                     "a": get_sprite(1, y), "d": get_sprite(2, y)},
            "walk": {"w": [get_sprite(8, y), get_sprite(9, y)],
                     "s": [get_sprite(4, y), get_sprite(5, y)],
                     "a": [get_sprite(6, y), get_sprite(1, y)],
                     "d": [get_sprite(7, y), get_sprite(2, y)]}}

# === CAMERA ===
def get_camera_offset():
    camera_x = max(0, min(player_x - WIDTH // 2, MAP_WIDTH - WIDTH))
    camera_y = max(0, min(player_y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    return camera_x, camera_y

# Load and scale character images, and define their positions
def is_near(player_x, player_y, npc_x, npc_y, distance=50):
    npc_x += img.get_width()/2
    npc_y += img.get_height()/2
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

    popup_surface = pygame.Surface((box_width, box_height))
    popup_surface.set_alpha(230)
    popup_surface.fill(bg_color)
    pygame.draw.rect(popup_surface, border_color, popup_surface.get_rect(), 4)

    line_height = font.get_height() + line_spacing
    y_offset = padding
    for l in lines:
        if y_offset + line_height > box_height - padding - 40:
            break
        text_surf = font.render(l, True, color)
        popup_surface.blit(text_surf, (padding, y_offset))
        y_offset += line_height

    # Draw "ENTER" button
    button_width, button_height = 100, 30
    button_x = (box_width - button_width) // 2
    button_y = box_height - button_height - padding
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(popup_surface, (180, 180, 180), button_rect)
    pygame.draw.rect(popup_surface, border_color, button_rect, 2)

    text_surf = font.render("ENTER", True, color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    popup_surface.blit(text_surf, text_rect)

    screen.blit(popup_surface, (box_x, box_y))

    # Return absolute screen coordinates of the button
    return pygame.Rect(box_x + button_x, box_y + button_y, button_width, button_height)

characters = [
    {
        "img": pygame.transform.scale(pygame.image.load("Assets/Sprites/npc/restaurant.png"), (80, 80)),
        "x": 770,
        "y": 130,
        "description": "Welcome to the restaurant, where the scent of sizzling meals meets the sound of scrubbing dishes. "
                       "Ready to roll up your sleeves? Take on the washing challenge and earn some well-deserved money."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("Assets/Sprites/npc/grocerry.png"), (100, 100)),  
        "x": 600,
        "y": 660,
        "description": "Bustling with customers and chaos. But today, you are not shopping — you are working. "
                       "Step behind the counter and become the cashier of the day."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("Assets/Sprites/npc/cyber_cafe.png"), (80, 80)),
        "x": 90,
        "y": 665,
        "description": "This is the teenagers' zone, and the only way to win here is to type like lightning. "
                       "Put your speed and accuracy to the test and rake in digital dough with each correct keystroke."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("Assets/Sprites/npc/Food_stall.png"), (65, 65)),
        "x": 750,
        "y": 353,
        "description": "Ready to bring you back to life. Choose your meal, sit back, and recover the energy you need to keep going. "
                       "After all, a hardworking spirit needs fuel to thrive."
    },
    {
        "img": pygame.transform.scale(pygame.image.load("Assets/Sprites/npc/lazapee.png"), (80, 80)),
        "x": 60,
        "y": 170,
        "description": "This is not just another shop — it is a gateway to passive income. "
                       "Invest wisely, and your money will work while you rest. "
                       "In this town, fortune favors the bold... and the smart."
    }
]

# === NPC ===
npc_img = pygame.image.load("Assets/Sprites/female/female_idle_left.png").convert_alpha()
npc_img = pygame.transform.scale(npc_img, (80, 80))
class NPC:
    def __init__(self, x, y, dialogue):
        self.x = x
        self.y = y
        self.dialogue = dialogue
        self.current_line = 0
        self.talking = False
        self.last_change = time.time()
        self.direction = "idle"
    def is_near_player(self, px, py):
        return ((self.x - px)**2 + (self.y - py)**2)**0.5 < 60
    def draw(self, surface, camera_x, camera_y):
        surface.blit(npc_img, (self.x - camera_x, self.y - camera_y))
        if self.is_near_player(player_x, player_y) and not self.talking:
            screen.blit(FONT.render("PRESS E", True, WHITE), (self.x - camera_x, self.y - camera_y - 25))
    def move_random(self):
        if time.time() - self.last_change > 2:
            self.direction = random.choice(["w", "a", "s", "d", "idle"])
            self.last_change = time.time()
        if self.direction == "w": self.y -= 1
        if self.direction == "a": self.x -= 1
        if self.direction == "s": self.y += 1
        if self.direction == "d": self.x += 1

# === Obstacles and buildings ===
buildingsurflist = Functions.get_sprite(224, 160, pygame.image.load("Assets/Images/Buildingsheet.png").convert_alpha())
obstaclesurflist = Functions.get_sprite(96, 64, pygame.image.load("Assets/Images/Obstaclesheet.png").convert_alpha())
obstaclelist = [(1, 0, 0, 0), (18, 0, 0, 0), (40, 2, 0, 0), (57, 10.2, 0, 0), (57, 6.73, 0, 0), 
                (57, 3.3, 0, 0), (57, 0, 0, 0), (61.5, 10.2, 0, 0), (61.5, 6.73, 0, 0), 
                (61.5, 3.3, 0, 0), (61.5, 0, 0, 0), (26.5, 6, 0, 0), (16.5, 10, 0, 0), 
                (38, 10, 0, 0), (31.5, 17, 0, 0), (3, 19, 0, 0), (12, 19, 0, 0), (10.5, 24, 0, 0), 
                (55, 23, 0, 0), (4, 32, 0, 0), (57, 33, 0, 0), (34, 38, 0, 0), (26, 38, 0, 0), 
                (57, 42, 0, 0), (44.5, 3, 0, 0), (16, 24, 0, 0), (46, 40, 1, 0), (40.5, 23.5, 1, 0.7),
                (18, 37.3, 2, 0)]
buildinglist = [(2.5, 3.2), (47.4, 1.5), (19.9, 17.15), (42, 18.15), (4.85, 35.5), (37.8, 34.54)]

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

# === GAME LOOP ===
dialogue_lines = ["Hi! Welcome to the store!", "DON'T COME BACK", "BYE", "[MENU]"]
npc = NPC(300, 300 , dialogue_lines)
menu_options = ["🛒 Shop", "📜 Quest"]
selected_option = 0

# 初始位置
player_x = 500
player_y = 400
moving = False
player_speed = 1.5
player_direction = "s"
walk_frame = 0
walk_timer = 0
walk_delay = 200
player_imgs = load_player_images("male")

statemanager = None
class StateManager():
    def __init__(self, state, var_dict):
        self.state, self.var_dict = state, var_dict

    def eventhandler(self, E):
        self.state.eventhandler(self.var_dict['mg_state'], E)

    def update(self):
        global game_state, statemanager, vm_level 
        self.state.update(self.var_dict['mg_state'], self.var_dict)
        if self.var_dict.get('vm_level'): vm_level = self.var_dict['vm_level']
        if not self.var_dict['mg_state']:
            game_state = "game"
            statemanager, self, Functions.displaystat = None, None, True
            Functions.play_music("background")

    def draw(self):
        self.state.draw(screen, self.var_dict['mg_state'])
        Functions.display_stats(screen)
        NOTI.displayicon(vm_level, xsmall_font)
        if self.var_dict.get('fade'): screen.blit(self.var_dict['fade'], (0, 0))

clock = pygame.time.Clock()
while running:
    dt = clock.tick(60)
    screen.fill(WHITE)
    cursor_timer += dt

    if not pygame.mixer.music.get_volume(): pygame.mixer.music.pause()
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
        player_speed = speedlist[1] if Functions.sprinttime > 0 else speedlist[0]

        camera_x, camera_y = get_camera_offset()
        screen.fill((0, 0, 0))
        screen.blit(map_img, (0 - camera_x, 0 - camera_y))  # Apply camera offset # Apply camera offset here

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

        # 更新NPC和绘制玩家
        npc.move_random()
        npc.draw(screen, camera_x, camera_y)
        move_distance = player_speed

        # Player movement 
        keys = pygame.key.get_pressed()
        moving = False
        new_x, new_y = player_x, player_y  # New position after moving
        
        if ((keys[pygame.K_w] and keys[pygame.K_s]) or 
            (keys[pygame.K_a] and keys[pygame.K_d])): 
            moving = False
        else:
            # Calculate distance for diagonal movement so that total displacement is = speed 
            if ((keys[pygame.K_w] or keys[pygame.K_s]) and 
                (keys[pygame.K_a] or keys[pygame.K_d])):
                move_distance = ((player_speed**2)/2)**0.5  

            if keys[pygame.K_w]:
                new_y -= move_distance
                player_direction = "w"
            elif keys[pygame.K_s]:
                new_y += move_distance
                player_direction = "s"
            if keys[pygame.K_a]:
                new_x -= move_distance
                player_direction = "a"
            elif keys[pygame.K_d]:
                new_x += move_distance
                player_direction = "d"

        # 创建玩家的目标矩形，用来检查碰撞
        if player_x != new_x:
            player_rect = pygame.Rect(new_x, player_y, sprite_width, sprite_height/2)
            for rect in collision_rects:
                if player_rect.colliderect(rect):
                    x_distance = abs(player_x + sprite_width/2 - rect.center[0]) - (sprite_width/2 + rect.width/2)
                    if not x_distance: new_x = player_x  # Stop movement on collision
                    else: 
                        if keys[pygame.K_a]: new_x = player_x - x_distance
                        elif keys[pygame.K_d]: new_x = player_x + x_distance
                    break
                        
        if player_y != new_y:
            player_rect = pygame.Rect(player_x, new_y, sprite_width, sprite_height/2)
            for rect in collision_rects:
                if player_rect.colliderect(rect):
                    y_distance = abs(player_y + sprite_height/4 - rect.center[1]) - (sprite_height/4 + rect.height/2)
                    if not y_distance: new_y = player_y  # Stop movement on collision
                    else: 
                        if keys[pygame.K_w]: new_y = player_y - y_distance
                        elif keys[pygame.K_s]: new_y = player_y + y_distance
                    break
                    
        # 如果没有发生碰撞，更新玩家位置, 更新动画帧
        if (player_x != new_x) or (player_y != new_y): 
            moving = True
            player_x, player_y = new_x, new_y
            if pygame.time.get_ticks() - walk_timer > walk_delay:
                walk_frame += 1
                if walk_frame >= len(player_imgs["walk"][player_direction]): walk_frame = 0
                walk_timer = pygame.time.get_ticks()
        
        else: walk_frame = 0

        current_img = player_imgs["walk"][player_direction][walk_frame] if moving else player_imgs["idle"][player_direction]
        screen.blit(current_img[1], (player_x - camera_x, player_y - camera_y))

        for i in range(len(buildinglist)): 
            xpos, ypos = buildinglist[i][0]*TILE_SIZE - camera_x, buildinglist[i][1]*TILE_SIZE - camera_y
            if (-224 <= xpos <= WIDTH) and (-160 <= ypos <= HEIGHT):
                screen.blit(buildingsurflist[i], (xpos, ypos))

        for x, y, surfid, scale in obstaclelist:
            surf = obstaclesurflist[surfid]
            xpos, ypos = x*TILE_SIZE - camera_x, y*TILE_SIZE - camera_y
            if (-96 <= xpos <= WIDTH) and (-64 <= ypos <= HEIGHT):
                if scale: surf = pygame.transform.scale_by(surf, scale)
                screen.blit(surf, (xpos, ypos))

        upper_rect = pygame.Rect(0, 0, sprite_width, sprite_height/2)
        upper_rect.bottomleft = (player_x - camera_x, player_y - camera_y)
        screen.blit(current_img[0], upper_rect)

        if npc.talking:
            pygame.draw.rect(screen, (0, 0, 0), (50, HEIGHT - 160, WIDTH - 100, 110))
            pygame.draw.rect(screen, (255, 255, 255), (50, HEIGHT - 160, WIDTH - 100, 110), 3)
            current_line = npc.dialogue[npc.current_line]
            if current_line == "[MENU]":
                for i, opt in enumerate(menu_options):
                    color = (255, 255, 0) if i == selected_option else WHITE
                    txt = BIG_FONT.render(opt, True, color)
                    screen.blit(txt, (80 + i * 150, HEIGHT - 120))
            else:
                screen.blit(FONT.render(current_line, True, WHITE), (60, HEIGHT - 130))

        # Only show popup for the first nearby character
        popup_button_rect = None
        for character in characters:
            screen.blit(character["img"], (character["x"] - camera_x, character["y"] - camera_y))
            if is_near(player_x, player_y, character["x"], character["y"]):
                popup_button_rect = draw_popup(screen, character["description"], small_font)
                break  # Only one popup at a time

        inventoryrect = INVENTORY.bag.get_rect(center = (940, 500)) 
        screen.blit(INVENTORY.bag, inventoryrect)        # PLACEHOLDER
        Functions.display_stats(screen)
        NOTI.displayicon(vm_level, xsmall_font)
        Functions.draw_floating_texts(screen)

    elif game_state == "inventory":
        INVENTORY.draw(xsmall_font, font)
        Functions.display_stats(screen)
        NOTI.displayicon(vm_level, xsmall_font)

    # == Lanching Mini Game  ==
    if statemanager: statemanager.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
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
            elif game_state == "game":
                if show_intro_message and typing_done: show_intro_message = False
                if popup_button_rect and popup_button_rect.collidepoint(event.pos):
                    print("ENTER button clicked!")
                    pygame.mixer.music.stop()
        
                    # PAUSE MAIN GAME LOOP while MG3 runs
                    pygame.mixer.music.stop()

                    # Create a new screen surface for MG3 and pass it
                    mg3_screen = pygame.display.set_mode((1024, 576))
                    result = run_MG3(mg3_screen)

                    # After MG3 finishes, re-create the main screen
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    # Recreate screen and pass it into MG3
                    pygame.display.set_mode((WIDTH, HEIGHT))
        
                    if result:
                        energy -= result["energy_spent"]
                        money += result["money_earned"]
                        Functions.add_floating_text(f"-{result['energy_spent']}", 250, 28, (128, 128, 128))
                        Functions.add_floating_text(f"+{result['money_earned']}", 250, 110, (128, 128, 128))

                        Functions.play_music("background")

                        # Force a redraw after MG3 ends
                        pygame.display.set_mode((WIDTH, HEIGHT))
                if inventoryrect.collidepoint(event.pos):
                    game_state = "inventory"

        elif event.type == pygame.KEYDOWN:
            if game_state == "intro":
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 30:
                    player_name += event.unicode
            elif game_state == "game":
                if event.key == pygame.K_RETURN and show_intro_message and typing_done:
                    show_intro_message = False
                if event.key == pygame.K_e and npc.is_near_player(player_x, player_y):
                    npc.talking = True
                    npc.current_line = 0
                    selected_option = 0
                if npc.talking:
                    if npc.dialogue[npc.current_line] == "[MENU]":
                        if event.key == pygame.K_LEFT:
                            selected_option = (selected_option - 1) % len(menu_options)
                        elif event.key == pygame.K_RIGHT:
                            selected_option = (selected_option + 1) % len(menu_options)
                        elif event.key == pygame.K_RETURN:
                            print(f"You selected: {menu_options[selected_option]}")
                            npc.talking = False
                    else:
                        if event.key == pygame.K_SPACE:
                            npc.current_line += 1
                            if npc.current_line >= len(npc.dialogue):
                                npc.talking = False
                        if event.key == pygame.K_ESCAPE:
                            npc.talking = False

                # Placeholder for launching minigames
                elif event.key == pygame.K_p:
                    statemanager = StateManager(Store.STORE(WIDTH, HEIGHT, INVENTORY), store_var_dict.copy())
                    game_state = "store"
                    
                elif event.key == pygame.K_1: 
                    statemanager = StateManager(MiniGame1.MG1(WIDTH, HEIGHT, clock), mg1_var_dict.copy())
                    game_state = "mg1"
                    break

                # Placeholder for launching minigames
                elif event.key == pygame.K_4: 
                    statemanager = StateManager(MiniGame4.MG4(WIDTH, HEIGHT, vm_buyingprices), mg4_var_dict.copy())
                    game_state = "mg4"
                    break

        # == EVENTS for passive income from Mini Game 4 ==
        elif event.type == VM1: Functions.update_stats(mpchange=vm_income[0][vm_level[0] - 1])
        elif event.type == VM2: Functions.update_stats(mpchange=vm_income[1][vm_level[1] - 1])
        
        if statemanager: statemanager.eventhandler(event)
        elif game_state == "game": INVENTORY.eventhandler(event, False)
        elif game_state == "inventory": game_state = "game" if INVENTORY.eventhandler(event) else "inventory"
        NOTI.updatetip(vm_level, event)

    if statemanager: statemanager.update()
    INVENTORY.update()

    pygame.display.flip()

pygame.quit()
