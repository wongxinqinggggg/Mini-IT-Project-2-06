import pygame
import json
import random
import os
from Features import Functions, MiniGame1, MiniGame2, MiniGame3, MiniGame4, Store, Bedroom

# === SETUP ===
pygame.init()
pygame.mixer.init()

# === SCREEN ===
WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Money, No Life")
clock = pygame.time.Clock()

# === FONTS ===
font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 20)
small_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 14)
FONT = pygame.font.SysFont("arial", 20)
xlarge_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 38)
large_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 32)
middle_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 26)
xsmall_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 8)

# === MUSIC ===
pygame.mixer.music.load("Assets/Audio/background.mp3")
money_sound = pygame.mixer.Sound("Assets/Audio/Cashier-Ka-Ching (u_byub5wd934).mp3")
button_click = pygame.mixer.Sound("Assets/Audio/button_click.mp3")
coin_sound = pygame.mixer.Sound("Assets/Audio/coinmusic.mp3")
fail_sound = pygame.mixer.Sound("Assets/Audio/fail.mp3")
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
bg_img = pygame.transform.scale(pygame.image.load("Assets/Images/main.png").convert(), (WIDTH, HEIGHT))
map_img = pygame.image.load("Assets/Images/final_map.png").convert()
NPC1 = pygame.image.load("Assets/Sprites/npc/adeline.png").convert_alpha()
NPC1list = Functions.get_sprite(48, 56, NPC1)
NPC2 = pygame.image.load("Assets/Sprites/npc/tralalelo_tralala.png").convert_alpha()
NPC2list = Functions.get_sprite(64, 51, NPC2)
NPC3 = pygame.image.load("Assets/Sprites/npc/boneca_ambalabu.png").convert_alpha()
NPC3list = Functions.get_sprite(32, 53, NPC3)
MAP_WIDTH, MAP_HEIGHT = ((800, 800))
npc_left1 = NPC1list[0]
npc_left2 = NPC1list[1]
npc_right1 = NPC1list[2]
npc_right2 = NPC1list[3]
npc_tralalelo_tralala_left = NPC2list[0]
npc_tralalelo_tralala_right = NPC2list[1]
npc_4d_img = NPC3list[0]
npc_4d_left1 = NPC3list[1]
npc_4d_right1 = NPC3list[2]
four_d_img = pygame.image.load("Assets/Images/Four_d.png").convert_alpha()
Pet = pygame.image.load("Assets/Sprites/npc/PET.png").convert_alpha()
Petlist = Functions.get_sprite(25, 42, Pet)
pet_img1 = Petlist[0]
pet_img2 = Petlist[1]
pet_img3 = Petlist[2]
pet_img4 = Petlist[3]
coin_img = pygame.image.load("Assets/Images/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (20, 20))

# === GAME VARIABLES ===
player_name = ''
selected_character = None
active_input = False
warning_message = ''
game_state = "intro"
show_intro_message = True
typing_done = False
four_d_state = 0
show_dialogue = False
pay_options = ["BUY", "BYE"]
reward_value = 0
reward_energy = 0
welcome_message = f"Welcome back, {player_name}"  
welcome_message = ""
welcome_message_start_time = 0
WELCOME_MESSAGE_DURATION = 3000 
waiting_for_enter = False    
closed_message = ""
closed_message_timer = 0
player_x = 380  # Initial X position
player_y = 450  # Initial Y position
speed = 2
player_speed = speed  # Player speed
player_direction = "s"  # Initial direction (facing down)
walk_frame = 0  # Current animation frame
walk_timer = 0  # Timer for animation updates
walk_delay = 200
money_drops = []  
money_drop_timer = 5
MONEY_DROP_INTERVAL = 15000 
MONEY_DROP_PROBABILITY = 0.3 
MONEY_DURATION = 15000 
BLINK_START = 5000
running = True

class AdelineNPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_range = (300, 570)
        self.height = 56
        self.direction = random.choice(["left", "right"])
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_delay = 200  
        self.talking = False
        self.active = True
        self.dialogue_state = 0  
        self.reward_given = False
        
    def update(self):
        if not self.active or self.talking: return

        if self.x < self.x_range[0]:
            self.x = self.x_range[0]
            self.direction = "right"
        elif self.x > self.x_range[1]:
            self.x = self.x_range[1]
            self.direction = "left"

        if random.random() < 0.01:  # 1%的几率改变方向
            self.direction = "left" if self.direction == "right" else "right"
            
        if self.direction == "left": self.x -= 1
        else: self.x += 1
            
        if pygame.time.get_ticks() - self.walk_timer > self.walk_delay:
            self.walk_frame = (self.walk_frame + 1) % 2
            self.walk_timer = pygame.time.get_ticks()
    
    def draw(self, surface, camera_x, camera_y):
        if not self.active: return
            
        # NPC
        if self.direction == "left": img = npc_left1 if self.walk_frame == 0 else npc_left2
        else: img = npc_right1 if self.walk_frame == 0 else npc_right2
            
        surface.blit(img, (self.x - camera_x, self.y - camera_y))
        
        if self.is_player_near() and not self.talking:
            text = FONT.render("Click Y to talk with ADELINE", True, WHITE)
            surface.blit(text, (self.x - camera_x - text.get_width()//2, self.y - camera_y - 30))
    
    def is_player_near(self):
        distance = ((self.x - player_x)**2 + (self.y - player_y)**2)**0.5
        return distance < 100
    
    def start_dialogue(self):
        global player_x, player_y, moving
        self.talking = True
        self.dialogue_state = 0
        moving = False 
    
    def end_dialogue(self):
        self.talking = False
        if self.dialogue_state == 2: self.active = False  # NPC Disappear
        if selected_color_option != 0: self.active = False    

class TralaleloTralalaNPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_range = [0, 800]
        self.height = 51
        self.direction = random.choice(["left", "right"])
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_delay = 200  
        self.talking = False
        self.active = True
        self.dialogue_state = 0  
        self.reward_given = False
        
    def update(self):
        if not self.active or self.talking:  return

        if self.x < self.x_range[0]:
            self.x = self.x_range[0]
            self.direction = "right"
        elif self.x > self.x_range[1]:
            self.x = self.x_range[1]
            self.direction = "left"

        if random.random() < 0.01:  # 1%的几率改变方向
            self.direction = "left" if self.direction == "right" else "right"
            
        if self.direction == "left": self.x -= 1
        else: self.x += 1
            
        if pygame.time.get_ticks() - self.walk_timer > self.walk_delay:
            self.walk_frame = (self.walk_frame + 1) % 2
            self.walk_timer = pygame.time.get_ticks()
    
    def draw(self, surface, camera_x, camera_y):
        if not self.active: return
            
        # NPC
        if self.direction == "left": img = npc_tralalelo_tralala_left
        else: img = npc_tralalelo_tralala_right
            
        surface.blit(img, (self.x - camera_x, self.y - camera_y))
        
        if self.is_player_near() and not self.talking:
            text = FONT.render("Click Y to talk with TRALALELO", True, WHITE)
            surface.blit(text, (self.x - camera_x - text.get_width()//2, self.y - camera_y - 30))
    
    def is_player_near(self):
        distance = ((self.x - player_x)**2 + (self.y - player_y)**2)**0.5
        return distance < 100
    
    def start_dialogue(self):
        global player_x, player_y, moving
        self.talking = True
        self.dialogue_state = 0
        moving = False 
    
    def end_dialogue(self):
        self.talking = False
        if self.dialogue_state == 2:   self.active = False  
        if selected_friend_option != 0: self.active = False

class FourDNPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 53
        self.direction = random.choice(["left", "right"])
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_delay = 200
        self.talking = False
        self.active = True
        self.dialogue_state = 0  # 0:Initial, 1:Checking & Buy, 2:Reward Display, 3:Not enough money, 4:Bye, 5:come again
        self.reward_money = 0
        self.reward_energy = 0
        self.selected_pay_option = 0
        self.dialogue_lines = [
            "Spend RM30 to buy a lottery ticket and receive a random reward",
            "Checking your wallet... Pls wait 3 seconds...",
            "Congratulations! Here's your reward:",
            "Sorry, you are too poor! Come to me when you have RM30",
            "See you next time...",
            "Come back anytime!"
        ]
        self.current_line = 0
        self.checked_wallet = False
        self.wallet_check_timer = 0
        self.wallet_check_duration = 3000  
        self.wallet_check_started = False
        self.sound_played_for_state_5 = False
        self.sound_played_for_state_3 = False

    def handle_input(self, event):        
        if event.type == pygame.KEYDOWN and self.talking:
            if self.dialogue_state == 0:  # BUY/BYE
                if event.key == pygame.K_LEFT:
                    self.selected_pay_option = 0  # BUY
                elif event.key == pygame.K_RIGHT:
                    self.selected_pay_option = 1  # BYE
                elif event.key == pygame.K_RETURN:  
                    if self.selected_pay_option == 0:  # BUY
                        self.dialogue_state = 1  # Checking
                        self.current_line = 1
                        self.checked_wallet = False
                        self.wallet_check_started = True
                        self.wallet_check_timer = pygame.time.get_ticks()
                    else:  # BYE
                        self.dialogue_state = 4
                        self.current_line = 4
                            
            elif event.key == pygame.K_SPACE:
                if self.dialogue_state == 2:      
                    Functions.update_stats(mpchange=self.reward_money, hpchange=self.reward_energy)   
                    self.dialogue_state = 5
                    self.current_line = 5
                elif self.dialogue_state in [3, 4, 5]:  
                    self.end_dialogue()

    def update(self):
        if not self.active: return

        if self.x < -5:
            self.x = -5
            self.direction = "right"
        elif self.x > 1020:
            self.x = 1020
            self.direction = "left"

        if random.random() < 0.01:
            self.direction = "left" if self.direction == "right" else "right"
            
        if self.direction == "left": self.x -= 1
        else: self.x += 1
            
        if pygame.time.get_ticks() - self.walk_timer > self.walk_delay:
            self.walk_frame = (self.walk_frame + 1) % 3
            self.walk_timer = pygame.time.get_ticks()

        if self.talking and self.dialogue_state == 1 and self.wallet_check_started and not self.checked_wallet:
            current_time = pygame.time.get_ticks()
            if current_time - self.wallet_check_timer >= self.wallet_check_duration:
                self.checked_wallet = True
                self.wallet_check_started = False

                if Functions.money >= 30:
                    Functions.update_stats(mpchange=-30)
                    self.reward_money = random.choice([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80])
                    self.reward_energy = random.choice([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80])
                    self.dialogue_state = 2
                    self.current_line = 2
                else:
                    self.dialogue_state = 3
                    self.current_line = 3
                
    def draw(self, surface, camera_x, camera_y):
        if not self.active: return
       
        # Draw NPC
        if self.direction == "left":
            if self.walk_frame == 0 or self.walk_frame == 2: img = npc_4d_img
            else: img = npc_4d_left1
        else:
            if self.walk_frame == 0 or self.walk_frame == 2: img = npc_4d_img
            else: img = npc_4d_right1
            
        surface.blit(img, (self.x - camera_x, self.y - camera_y))

        if self.is_player_near() and not self.talking:
            text = FONT.render("Click Y to talk with 4D Seller", True, WHITE)
            surface.blit(text, (self.x - camera_x - text.get_width()//2, self.y - camera_y - 30))

    def draw_dialogue(self, surface):
        if self.talking:
            pygame.draw.rect(surface, (0, 0, 0), (50, HEIGHT-200, WIDTH-100, 150))
            pygame.draw.rect(surface, WHITE, (50, HEIGHT-200, WIDTH-100, 150), 3)
            
            if self.dialogue_state == 0:  
                for i, option in enumerate(["BUY", "BYE"]):
                    color = HIGHLIGHT if i == self.selected_pay_option else WHITE
                    surface.blit(font.render(option, True, color), (100+i*200, HEIGHT-140))

            elif self.dialogue_state == 1:
                surface.blit(small_font.render("Checking your wallet...", True, WHITE), (70, HEIGHT-180))

            elif self.dialogue_state == 2:
                screen.blit(four_d_img, (WIDTH//2 - four_d_img.get_width()//2, HEIGHT//2 - four_d_img.get_height()//2))
                reward_text = f"Reward: Money +{self.reward_money}, Energy +{self.reward_energy}"
                surface.blit(font.render(reward_text, True, WHITE), (WIDTH//2-442, HEIGHT//2+four_d_img.get_height()//2+60))
                surface.blit(small_font.render("Press SPACE to collect", True, WHITE), (70, HEIGHT-90))

            elif self.dialogue_state == 3:
                surface.blit(small_font.render("Sorry, you are too poor! Come to me when you have RM30", True, WHITE), (70, HEIGHT-180))

            elif self.dialogue_state == 4:
                surface.blit(small_font.render("See you next time...", True, WHITE), (70, HEIGHT-180))

            elif self.dialogue_state == 5:
                surface.blit(small_font.render("Come back anytime!", True, WHITE), (70, HEIGHT-180))
    
    def is_player_near(self):
        distance = ((self.x - player_x)**2 + (self.y - player_y)**2)**0.5
        return distance < 100

    def start_dialogue(self):
        global player_x, player_y, moving
        self.talking = True
        self.dialogue_state = 0
        self.current_line = 0
        self.selected_pay_option = 0 
        self.reward_given = False 
        self.sound_played_for_state_5 = False
        self.sound_played_for_state_3 = False
        moving = False 
    
    def end_dialogue(self):
        self.talking = False
        self.dialogue_state = 0
        self.current_line = 0
        self.selected_pay_option = 0
        self.reward_given = False
        self.checked_wallet = False    

class PetNPC:
    def __init__(self, x=590, y=355):
        self.x = x
        self.y = y
        self.owned = False
        self.direction = "right"
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_delay = 200
        self.follow_speed = 3
        self.follow_distance = 42
        self.talking = False
        self.active = True
        self.dialogue_state = 0
        self.selected_option = 0
        self.pet_name = ""
        self.pet_hp = 888
        self.MAXHP = 999
        self.pet_hpchange, self.happy_hpchange = 5, 1
        self.hp_percentage = {'happy': 0.33, 'hungry': 0.2}
        self.name_input_active = False
        self.name_confirmed = False
        self.width = 25
        self.height = 42
        self.event = pygame.USEREVENT + 103  # This line was missing in the implementation
        self.pet_img1 = Petlist[0]
        self.pet_img2 = Petlist[1]
        self.pet_img3 = Petlist[2]
        self.pet_img4 = Petlist[3]
        self.collect_range = 60  
        self.collect_cooldown = 0  
        self.happy_timer = 0  
        self.is_happy = False

    def update(self, player_x, player_y, collision_rects, money_drops):
        if not self.owned or not self.pet_hp: return
        
        move_x = player_x - self.x
        move_y = player_y - self.y
        distance = (move_x**2 + move_y**2)**0.5
        
        if distance > self.follow_distance: 
            move_x = move_x / distance * self.follow_speed
            move_y = move_y / distance * self.follow_speed
            pet_rect = pygame.Rect(self.x + move_x, self.y, self.width, self.height)
            for rect in collision_rects:
                if pet_rect.colliderect(rect):
                    move_x = 0
                    break
            
            self.x += move_x
            if move_x <= 0: self.direction = "left"
            elif move_x > 0: self.direction = "right"
            
            pet_rect = pygame.Rect(self.x, self.y + move_y, self.width, self.height)
            for rect in collision_rects:
                if pet_rect.colliderect(rect):
                    move_y = 0
                    break
            
            self.y += move_y

            if not move_x and not move_y: self.walk_frame = 0 
            elif pygame.time.get_ticks() - self.walk_timer > self.walk_delay:
                self.walk_frame = (self.walk_frame + 1) % 4  # 现在有4帧动画
                self.walk_timer = pygame.time.get_ticks()  

        if self.owned:  # Only collect money after naming
            current_time = pygame.time.get_ticks()
            if current_time - self.collect_cooldown > 1000:  # 1 second cooldown
                for money in money_drops[:]:
                    distance = ((self.x - money["x"])**2 + (self.y - money["y"])**2)**0.5
                    if distance < self.collect_range:
                        # Collect money
                        Functions.update_stats(mpchange=money["value"])
                        # Changed this line to use 'mp' as the ID instead of coordinates
                        Functions.add_floating_text(f"+{money['value']}", 'mp', (0, 255, 0))
                        Functions.playsound("coin")  # Play collection sound
                        money_drops.remove(money)
                        self.collect_cooldown = current_time
                        self.is_happy = True
                        self.happy_timer = current_time
                        break
                
            # Happy state duration (2 seconds)
            if self.is_happy and current_time - self.happy_timer > 2000:
                self.is_happy = False

    def draw(self, surface, camera_x, camera_y):
        if not self.active: return
            
        if self.direction == "left":
            if self.walk_frame == 0 or self.walk_frame == 2: img = self.pet_img3
            else: img = self.pet_img4
        elif self.direction == "right":
            if self.walk_frame == 0 or self.walk_frame == 2: img = self.pet_img1
            else: img = self.pet_img2
            
        if self.is_happy:
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            heart = font.render("<3", True, (255, 0, 0))
            surface.blit(heart, (self.x - camera_x + img.get_width()//2 - heart.get_width()//2, self.y - camera_y - 20))

        surface.blit(img, (self.x - camera_x, self.y - camera_y))

        if self.is_player_near() and not self.talking and not self.owned:
            text = FONT.render("Press P to talk with PET", True, WHITE)
            surface.blit(text, (self.x - camera_x - text.get_width()//2, self.y - camera_y - 30))
                
    def is_player_near(self):
        distance = ((self.x - player_x)**2 + (self.y - player_y)**2)**0.5
        return distance < 100
    
    def start_dialogue(self):
        global player_x, player_y, moving
        if not self.owned:  
            self.talking = True
            self.dialogue_state = 0
            moving = False
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and self.talking:
            if self.dialogue_state == 0:  
                if event.key == pygame.K_LEFT:
                    self.selected_option = 0  
                elif event.key == pygame.K_RIGHT:
                    self.selected_option = 1  
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # YES
                        self.dialogue_state = 1  
                        self.name_input_active = True
                    else:  # NO
                        self.end_dialogue()
                        
            elif self.dialogue_state == 1:  
                if event.key == pygame.K_BACKSPACE:
                    self.pet_name = self.pet_name[:-1]
                elif event.key == pygame.K_RETURN and self.pet_name:  
                    self.name_input_active = False
                    self.dialogue_state = 2  
                elif len(self.pet_name) < 11 and event.unicode.isprintable():
                    self.pet_name += event.unicode
                    
            elif self.dialogue_state == 2:  
                if event.key == pygame.K_LEFT:
                    self.selected_option = 0  
                elif event.key == pygame.K_RIGHT:
                    self.selected_option = 1  
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  
                        self.owned = True
                        pygame.time.set_timer(self.event, 5000)
                        self.end_dialogue()
                    else:  
                        self.dialogue_state = 0
                        self.pet_name = ""
    
    def end_dialogue(self):
        self.talking = False
        self.name_input_active = False
        if not self.owned:
            self.dialogue_state = 0

popup_button_rect = None
mgid = None
Functions.initialize_stats()
Functions.load_sprite()
vm_level = [0, 0]   # Vending machine level for Mini Game 4
vm_income = [[1, 2, 3], [5, 6, 7]]
vmbuyingprices = [[300, 400, 500], [800, 900, 1000]]
vm_buyingprices = [[300, 400, 500], [800, 900, 1000]]
VM1, VM2 = pygame.USEREVENT + 101, pygame.USEREVENT + 102
VM_EVENT = [VM1, VM2]
MENU = Functions.Menu(WIDTH)
NOTI = Functions.Notifications(screen, vm_buyingprices, vm_income)
INVENTORY = Functions.Inventory(screen, clock)
adeline = AdelineNPC(300, 195)
tralalelo = TralaleloTralalaNPC(500, 750)
four_d_npc = FourDNPC(400, 460)
pet_npc = PetNPC()
color_options = ["TEAL", "MAUVE"]
selected_color_option = 0
friend_options = ["Sang Telur", "Tung Sahur"]
selected_friend_option = 0
menu_var_dict = {'mg_state': "menu", 'prev_state': "game", 'dragging': False}

mg1_var_dict = {'mg_state': "mainpage", 'time_passed': 0, 'msg': None, 'new_plate': True, 
                'plates': 0, 'stains': None, 'dragging': None, 'prev_state': None,
                'Lfont': large_font, 'Mfont': middle_font, 'XLfont': xlarge_font, 'fade': None}

mg4_var_dict = {'mg_state': "mainpage", 'vm_level': vm_level, 'vm_income': vm_income, 
                'VM_EVENT': VM_EVENT, 'Sfont': small_font, 'XSfont': xsmall_font, 
                'prev_state': None, 'dragging': None, 'noti': NOTI}

store_var_dict = {'mg_state': "mainpage", 'prev_state': None, 'dragging': None, 'Mfont': middle_font}

current_alpha = 0  # start fully day (no dark overlay)
max_alpha = 180    # max darkness (adjust to your liking)
transition_speed = 2  # alpha change speed per frame, adjust for smoothness
is_night = False
transitioning = False

# Create a semi-transparent black surface to simulate night
dark_overlay = pygame.Surface((1024, 576), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, current_alpha))  # Use RGBA tuple now

# Create a light mask with transparency
light_mask = pygame.Surface((200, 200), pygame.SRCALPHA)
rect = pygame.Rect(51, 50, 17, 10)
pygame.draw.rect(light_mask, (255, 255, 0, 255), rect)

# Position of the light 
lamp_post_positions = [(738, 183),   # near Restaurant
    (550, 436), # near House
    (92, 423),  # alone at left side
    (937, 338), # near Food stall
    (787, 738), # near Grocerry
    (259, 738), # near Cyber Cafe
    (247, 190), # near Lazapee
    (405, 638), # near Bench
]

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

# === Main Btn ===
inventoryrect = INVENTORY.bag.get_rect(center = (940, 500)) 
menubtn = Functions.mainbtnlist[1]
menubtnrect = menubtn.get_rect(center = (975, 50))

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

def save_game():
    inventories = save_inventories(INVENTORY.inventories)
    pet_corpse = save_pet(pet_npc)
    data = {"player_name": player_name, "selected_character": selected_character, 
            'energy': Functions.energy, 'money': Functions.money, 'vm_level': vm_level, 
            'baglvl': INVENTORY.baglvl,'inventories': inventories, 
            'sprinttime': Functions.sprinttime, 'displaynoti': NOTI.displaynoti, 
            'pet_name': pet_npc.pet_name, 'pet_hp': pet_npc.pet_hp, 'pet_corpse': pet_corpse}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def save_inventories(inventories):
    data = inventories.copy()
    for key in data.keys():
        for item in ['surf', 'rect', 'center', 'cellrect', 'lockrect']:
            data[key].pop(item)
    return data

def save_pet(pet):
    if pet.pet_hp: data = None
    else:  data = {'x': pet.x, 'y': pet.y, 'direction': pet.direction, 'walk_frame': pet.walk_frame}
    return data

def load_game():
    global warning_message
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return data
    else:
        warning_message = "No save file found. Starting a new game."
        return None 

def reset_game():
    global warning_message
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        warning_message = "Save file deleted!"
    else:
        warning_message = "No save file to delete!"

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
saving_box = pygame.Rect(0, 200, WIDTH, 200)

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

    idle_s, idle_a, idle_d, idle_w = get_sprite(0, y), get_sprite(1, y), get_sprite(2, y), get_sprite(3, y)
    walk_s1, walk_s2 = get_sprite(4, y), get_sprite(5, y)
    walk_a, walk_d = get_sprite(6, y), get_sprite(7, y)
    walk_w1, walk_w2 = get_sprite(8, y), get_sprite(9, y)

    return {
        # Walk (%4)
        "w": [idle_w, walk_w1, idle_w, walk_w2],
        "s": [idle_s, walk_s1, idle_s, walk_s2],
        "a": [idle_a, walk_a, idle_a, walk_a],  
        "d": [idle_d, walk_d, idle_d, walk_d],

        "idle": {
            "w": idle_w,
            "s": idle_s,
            "a": idle_a,
            "d": idle_d
        }
    }

def is_any_npc_talking():
    return (tralalelo.talking or adeline.talking or four_d_npc.talking or 
            (pet_npc.active and pet_npc.talking))

# === CAMERA ===
def get_camera_offset():
    camera_x = max(0, min(player_x - WIDTH // 2, MAP_WIDTH - WIDTH))
    camera_y = max(0, min(player_y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    return camera_x, camera_y

# Load and scale character images, and define their positions
def is_near(player_x, player_y, npc_x, npc_y, img, distance=50):
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

Characterssheet = pygame.image.load("Assets/Sprites/npc/characters.png").convert_alpha()
character  = Functions.get_sprite(42, 64, Characterssheet)
characters = [
    {
        "mg_state": "MG1", "img": character[0], "x": 790, "y": 135,
        "description": "Welcome to the restaurant, where the scent of sizzling meals meets the sound of scrubbing dishes. "
                       "Ready to roll up your sleeves? Take on the washing challenge and earn some well-deserved money."
    },
    {
        "mg_state": "MG2", "img": character[1], "x": 640, "y": 670,
        "description": "Bustling with customers and chaos. Today, you are not shopping — you are working! "
                       "Step behind the counter and become the cashier of the day."
    },
    {
        "mg_state": "MG3", "img": character[2], "x": 110, "y": 680,
        "description": "This is the teenagers' zone, and the only way to win here is to type like lightning. "
                       "Put your speed and accuracy to the test and rake in digital dough with each correct keystroke."
    },
    {
        "mg_state": "MG4", "img": character[3], "x": 70, "y": 180,
        "description": "This is not just shop — it is a gateway to passive income. "
                       "Invest wisely, and your money will grow while you rest."
    },
    {
        "mg_state": "STORE", "img": character[4], "x": 770, "y": 365,
        "description": "Ready to bring you back to life. Choose your meal, sit back, and recover the energy you need to keep going. "
                       "After all, a hardworking spirit needs fuel to thrive."
    },
    {
        "mg_state": "bedroom", "img": character[5], "x": 310, "y": 380,
        "description": "You've survived another day in the pixel world! Time to face your toughest quest yet: getting out of bed." 
                        " Sleep now to recharge your energy!"
    },
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
        NOTI.displayicon(vm_level, pet_npc, xsmall_font, is_night)
        if self.var_dict.get('fade'): screen.blit(self.var_dict['fade'], (0, 0))

DAY_LENGTH = 50000     # milliseconds for day
NIGHT_LENGTH = 30000 # milliseconds for night
last_switch_time = pygame.time.get_ticks()

# === GAME LOOP ===
while running:
    screen.fill(WHITE)
    dt = clock.tick(60)
    input_locked = show_intro_message or welcome_message != ""
    now = pygame.time.get_ticks()
    if is_night and now - last_switch_time > NIGHT_LENGTH:
        is_night = False
        transitioning = True
        last_switch_time = now
    elif not is_night and now - last_switch_time > DAY_LENGTH:
        is_night = True
        transitioning = True
        last_switch_time = now

    cursor_timer += dt
    if cursor_timer >= cursor_interval:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    if game_state == "intro":
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
        if now - money_drop_timer > MONEY_DROP_INTERVAL and random.random() < 0.3:
            money_drops.append({
                "x": random.randint(50, MAP_WIDTH-50),
                "y": random.randint(50, MAP_HEIGHT-50),
                "value": random.randint(1, 10),
                "time": now,
                "duration": MONEY_DURATION
            })
            money_drop_timer = now
    
        current_time = pygame.time.get_ticks()
        for money in money_drops[:]:
            if current_time - money["time"] > money["duration"]:
                money_drops.remove(money)
    
        player_speed = speed if Functions.sprinttime <= 0 else speed * 2
        camera_x, camera_y = get_camera_offset()
        screen.blit(map_img, (-camera_x, -camera_y))
            
        # Smoothly adjust alpha
        if transitioning:
            if is_night:
                current_alpha += transition_speed
                if current_alpha >= max_alpha:
                    current_alpha = max_alpha
                    transitioning = False
            else:
                current_alpha -= transition_speed
                if current_alpha <= 0:
                    current_alpha = 0
                    transitioning = False
        # Apply darkness overlay
        dark_overlay.fill((0, 0, 0, current_alpha))
        screen.blit(dark_overlay, (0, 0))

        # Draw light masks to simulate glowing lamp posts
        if is_night:
            for lx, ly in lamp_post_positions:
                light_mask.set_alpha(180)
                screen_x = lx - camera_x
                screen_y = ly - camera_y
                screen.blit(light_mask, (screen_x - 100, screen_y - 100))

        # Player movement logic
        old_x, old_y = player_x, player_y
        moving = False
        new_x, new_y = player_x, player_y

        if not input_locked and not is_any_npc_talking():
            keys = pygame.key.get_pressed()
            move_distance = player_speed 
        
            if not ((keys[pygame.K_w] and keys[pygame.K_s]) or (keys[pygame.K_a] and keys[pygame.K_d])):
                if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
                    move_distance = ((player_speed**2)/2)**0.5  # Calculate move s=distance for diagonal movement

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

        # Collision detection logic
        if new_x != player_x:
            player_rect = pygame.Rect(new_x, player_y, sprite_width, sprite_height/2)
            # Simplified collision check
            collision_found = False
            for rect in collision_rects:
                if player_rect.colliderect(rect):
                    x_distance = abs(player_x + sprite_width/2 - rect.center[0]) - (sprite_width/2 + rect.width/2)
                    if not x_distance: collision_found = True
                    elif keys[pygame.K_a]: new_x = player_x - x_distance
                    elif keys[pygame.K_d]: new_x = player_x + x_distance
                    break
            if not collision_found: player_x = new_x

        if new_y != player_y:
            player_rect = pygame.Rect(player_x, new_y, sprite_width, sprite_height/2)
            # Simplified collision check
            collision_found = False
            for rect in collision_rects:
                if player_rect.colliderect(rect):
                    y_distance = abs(player_y + sprite_height/4 - rect.center[1]) - (sprite_height/4 + rect.height/2)
                    if not y_distance: collision_found = True
                    elif keys[pygame.K_w]: new_y = player_y - y_distance
                    elif keys[pygame.K_s]: new_y = player_y + y_distance
                    break
            if not collision_found: player_y = new_y
        
        # Determine if the player is actually moving
        moving = (player_x != old_x) or (player_y != old_y)
        
        # Update animation frame
        if moving:
            if pygame.time.get_ticks() - walk_timer > walk_delay:
                walk_frame = (walk_frame + 1) % len(player_imgs[player_direction])
                walk_timer = pygame.time.get_ticks()
        else: walk_frame = 0

        # Choose the correct sprite based on state
        current_img = player_imgs[player_direction][walk_frame] if moving else player_imgs["idle"][player_direction]

        # --- DRAWING SEQUENCE STARTS HERE ---
        pet_npc.update(player_x, player_y, collision_rects, money_drops)
        pet_npc.draw(screen, camera_x, camera_y)

        
        if tralalelo.active and ((tralalelo.y + tralalelo.height) <= (player_y + sprite_height/2)): 
            tralalelo.draw(screen, camera_x, camera_y)

        if four_d_npc.active and ((four_d_npc.y + four_d_npc.height) <= (player_y + sprite_height/2)): 
            four_d_npc.draw(screen, camera_x, camera_y)

        if adeline.active and ((adeline.y + adeline.height) <= (player_y + sprite_height/2)): 
            adeline.draw(screen, camera_x, camera_y)

        for money in money_drops:
            time_left = money["duration"] - (current_time - money["time"])
            if time_left > BLINK_START or (time_left // 500) % 2 == 0:
                screen.blit(coin_img, (money["x"] - camera_x - coin_img.get_width()//2, money["y"] - camera_y - coin_img.get_height()//2))
                text = xsmall_font.render(str(money["value"]), True, WHITE)
                screen.blit(text, (money["x"] - camera_x - text.get_width()//2, money["y"] - camera_y - 25))

        # Draw player's lower half
        screen.blit(current_img[1], (player_x - camera_x, player_y - camera_y))
        
        # Draw buildings and obstacles now
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

        for character in characters:
            screen.blit(character["img"], (character["x"] - camera_x, character["y"] - camera_y))

        # Draw player's upper half
        upper_rect = pygame.Rect(0, 0, sprite_width, sprite_height/2)
        upper_rect.bottomleft = (player_x - camera_x, player_y - camera_y)
        screen.blit(current_img[0], upper_rect)

        popup_button_rect = None
        
        if tralalelo.active and ((tralalelo.y + tralalelo.height) > (player_y + sprite_height/2)): 
            tralalelo.draw(screen, camera_x, camera_y)

        if four_d_npc.active:
            four_d_npc.draw_dialogue(screen)
            if ((four_d_npc.y + four_d_npc.height) > (player_y + sprite_height/2)): 
                four_d_npc.draw(screen, camera_x, camera_y)

        if adeline.active and ((adeline.y + adeline.height) > (player_y + sprite_height/2)): 
            adeline.draw(screen, camera_x, camera_y)

        if tralalelo.active:
            tralalelo.update()
            if tralalelo.talking:
                pygame.draw.rect(screen, (0, 0, 0), (50, HEIGHT - 200, WIDTH - 100, 150))
                pygame.draw.rect(screen, WHITE, (50, HEIGHT - 200, WIDTH - 100, 150), 3)
                if tralalelo.dialogue_state == 0:
                    text = "Guess who are my friend!"
                    screen.blit(small_font.render(text, True, WHITE), (70, HEIGHT - 180))
                    for i, option in enumerate(friend_options):
                        friend = HIGHLIGHT if i == selected_friend_option else WHITE
                        screen.blit(small_font.render(option, True, friend), (100 + i * 200, HEIGHT - 140))
                        
                elif tralalelo.dialogue_state == 1:
                    if selected_friend_option == 0:
                        text = "You got it wrong... I thought we had a connection..."
                    else:
                        text = "Bingo! As your new bestie, I'm giving you 50 Money!"
                        if not tralalelo.reward_given:
                            Functions.update_stats(mpchange=50)
                            tralalelo.reward_given = True
                            money_sound.play()
                    screen.blit(small_font.render(text, True, WHITE), (70, HEIGHT - 160))
                elif tralalelo.dialogue_state == 2:
                    screen.blit(small_font.render("Thanks for chatting!", True, WHITE), (70, HEIGHT - 160))
    
        if four_d_npc.active:
            four_d_npc.update()
            if four_d_npc.talking:
                screen.blit(small_font.render(four_d_npc.dialogue_lines[four_d_npc.current_line], True, WHITE), (70, HEIGHT-180))
                if four_d_npc.dialogue_state == 5 and not four_d_npc.sound_played_for_state_5:
                    money_sound.play()
                    four_d_npc.sound_played_for_state_5 = True
                if four_d_npc.dialogue_state == 3 and not four_d_npc.sound_played_for_state_3:
                    fail_sound.play()
                    four_d_npc.sound_played_for_state_3 = True

        if adeline.active:
            adeline.update()
            if adeline.talking:
                pygame.draw.rect(screen, (0, 0, 0), (50, HEIGHT - 200, WIDTH - 100, 150))
                pygame.draw.rect(screen, WHITE, (50, HEIGHT - 200, WIDTH - 100, 150), 3)
                if adeline.dialogue_state == 0:
                    text = "Guess what's my favorite colour? It's a rare one!"
                    screen.blit(small_font.render(text, True, WHITE), (70, HEIGHT - 180))
                    for i, option in enumerate(color_options):
                        color = HIGHLIGHT if i == selected_color_option else WHITE
                        screen.blit(font.render(option, True, color), (100 + i * 200, HEIGHT - 140)) 

                elif adeline.dialogue_state == 1:
                    if selected_color_option == 0:
                        text = "You got it wrong... I thought we had a connection..."
                    else:
                        text = "Bingo! As your new bestie, I'm giving you 50 Energy!"
                        if not adeline.reward_given:
                            Functions.update_stats(hpchange=50)
                            adeline.reward_given = True
                            money_sound.play()
                    screen.blit(small_font.render(text, True, WHITE), (70, HEIGHT - 160))
                elif adeline.dialogue_state == 2:
                    screen.blit(small_font.render("Thanks for chatting!", True, WHITE), (70, HEIGHT - 160))       

        if pet_npc.talking:
            pygame.draw.rect(screen, (0, 0, 0), (50, HEIGHT-200, WIDTH-100, 150))
            pygame.draw.rect(screen, WHITE, (50, HEIGHT-200, WIDTH-100, 150), 3)
            if pet_npc.dialogue_state == 0:  
                text1 = small_font.render("Do you want it become your lovely pet?", True, WHITE)
                text2 = small_font.render("It will occasionally drop coins after adoption!", True, WHITE)
                screen.blit(text1, (70, HEIGHT-180))
                screen.blit(text2, (70, HEIGHT-140))
                for i, option in enumerate(["YES", "NO"]):
                    color = HIGHLIGHT if i == pet_npc.selected_option else WHITE
                    screen.blit(font.render(option, True, color), (100 + i * 200, HEIGHT-100))
                    
            elif pet_npc.dialogue_state == 1:  
                text = small_font.render("Name your pet:", True, WHITE)
                screen.blit(text, (70, HEIGHT-180))
                name_text = font.render(pet_npc.pet_name + ("|" if pet_npc.name_input_active and cursor_visible else ""), True, WHITE)
                screen.blit(name_text, (70, HEIGHT-150))
                hint = small_font.render("Press ENTER to confirm", True, WHITE)
                screen.blit(hint, (70, HEIGHT-120))
                
            elif pet_npc.dialogue_state == 2:  
                text = small_font.render(f"Hi, I'm {pet_npc.pet_name} now!", True, WHITE)
                screen.blit(text, (70, HEIGHT-180))
                for i, option in enumerate(["Hi! You are my pet now!", "RENAME"]):
                    color = HIGHLIGHT if i == pet_npc.selected_option else WHITE
                    screen.blit(small_font.render(option, True, color), (100 + i * 400, HEIGHT-140))

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

        elif welcome_message:
            now = pygame.time.get_ticks()
            if now - welcome_message_start_time <= WELCOME_MESSAGE_DURATION:
                text_surface = font.render(welcome_message, True, BLACK)
                text_rect = text_surface.get_rect(center=(500, 400))  
                bg_rect = text_rect.inflate(20, 20)  
                pygame.draw.rect(screen, (255, 255, 255), bg_rect)     
                pygame.draw.rect(screen, (0, 0, 0), bg_rect, 4)         
                screen.blit(text_surface, text_rect)
            else:
                welcome_message = ""

        elif closed_message:
            still_near_closed_shop = False
            for character in characters:
                if character["mg_state"] in ["MG1", "MG2", "MG4"]:
                    if is_near(player_x+sprite_width/2, player_y, character["x"], character["y"], character['img']):
                        still_near_closed_shop = True
                        break

            if still_near_closed_shop:
                msg_rect = pygame.Rect(30, 500, 900, 60)
                pygame.draw.rect(screen, WHITE, msg_rect)
                pygame.draw.rect(screen, BLACK, msg_rect, 3)
                msg_text = small_font.render(closed_message, True, BLACK)
                text_rect = msg_text.get_rect(center=msg_rect.center)
                screen.blit(msg_text, text_rect)
            else:
                closed_message = ""

         # Only show popup for the first nearby character
        for character in characters:
            mgid_candidate = character['mg_state']
            if is_near(player_x+sprite_width/2, player_y, character["x"], character["y"], character['img']):
                if is_night and mgid_candidate in ["MG1", "MG2", "MG4"]:
                    closed_message = "This place is closed for the night. Come back during the day!"
                    closed_message_timer = pygame.time.get_ticks()
                    mgid = None
                    popup_button_rect = None
                else:
                    mgid = mgid_candidate
                    closed_message = None
                    popup_button_rect = draw_popup(screen, character["description"], small_font)
                break 

        # Drawing UI element in game
        screen.blit(menubtn, menubtnrect) 
        screen.blit(INVENTORY.bag, inventoryrect)
        Functions.display_stats(screen)
        NOTI.displayicon(vm_level, pet_npc, xsmall_font, is_night)
        Functions.draw_floating_texts(screen)

    elif game_state == "inventory":
        INVENTORY.draw(xsmall_font, font)
        Functions.display_stats(screen)
        NOTI.displayicon(vm_level, pet_npc, xsmall_font, is_night)

    elif game_state == "menu":
        screen.blit(bg_img, (0, 0))
        MENU.draw(screen)

    elif game_state == "saving":
        screen.blit(bg_img, (0, 0))
        saving_timer += clock.get_time()
        pygame.draw.rect(screen, (200, 0, 0), saving_box, 200)
        i = int((saving_timer / 400) % 4)
        screen.blit(xlarge_font.render(f'SAVING GAME{"." * i}', True, 'Black'), (WIDTH/2 - 300, HEIGHT/2))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        if saving_timer >= 3500: running = False
        pygame.display.flip()
        continue

    elif game_state == "mg3":
        if MiniGame3.game_state == "quit":
            game_state = "game"
  
    if statemanager: statemanager.draw()

    for event in pygame.event.get():
        cursorclicked, cursorcollide = False, False
    
        if event.type == pygame.QUIT: running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "intro":
                active_input = True
                if male_box.collidepoint(event.pos): selected_character = 'male'
                elif female_box.collidepoint(event.pos): selected_character = 'female'
                elif start_button.collidepoint(event.pos):                            
                    if player_name and selected_character:
                        Functions.initialize_stats() 
                        vm_level, NOTI.displaynoti, Functions.sprinttime = [0,0], [True, True, False, False], 0
                        INVENTORY.load_inventories()
                        pet_npc = PetNPC()
                        pygame.time.set_timer(pet_npc.event, 0)
                        for vm_event in VM_EVENT: pygame.time.set_timer(vm_event, 0)
                        intro_message = generate_intro_message(player_name)
                        show_intro_message = True
                        typing_done = False
                        typed_message = ""
                        typing_index = 0
                        player_imgs = load_player_images(selected_character)  # Load correct character assets
                        game_state = "game"
                    else:
                        warning_message = "Enter name and choose a character!"  # Only show this when conditions aren't met

                elif continue_button.collidepoint(event.pos):
                    saved_data = load_game()
                    if saved_data:
                        Functions.initialize_stats(saved_data["energy"], saved_data["money"]) 
                        vm_level, Functions.sprinttime = saved_data['vm_level'], saved_data['sprinttime']
                        NOTI.displaynoti = saved_data['displaynoti']
                        INVENTORY.baglvl = saved_data['baglvl']
                        INVENTORY.load_inventories(saved_data['inventories'])
                        player_name = saved_data["player_name"]
                        selected_character = saved_data["selected_character"]
                        if saved_data["pet_name"]:
                            pet_npc.pet_name = saved_data["pet_name"]
                            pet_npc.pet_hp = saved_data["pet_hp"]
                            pet_npc.owned = True
                            pygame.time.set_timer(pet_npc.event, 5000)
                            if saved_data["pet_corpse"]:
                                pet_npc.x = saved_data["pet_corpse"]['x']
                                pet_npc.y = saved_data["pet_corpse"]['x']
                                pet_npc.direction = saved_data["pet_corpse"]['direction']
                                pet_npc.walk_frame = saved_data["pet_corpse"]['walk_frame']
                        for i in range(len(vm_level)):
                            if vm_level[i]:
                                pygame.time.set_timer(VM_EVENT[i], 1000)

                        game_state = "game"
                        warning_message = ''
                        show_intro_message = False
                        typing_done = False
                        typed_message = ""
                        typing_index = 0
                        player_imgs = load_player_images(selected_character)
                        welcome_message = f"Welcome back, {player_name}"
                        welcome_message_start_time = pygame.time.get_ticks()
                    else:
                        warning_message = "No saved game found!"
                        welcome_message = ""
                elif reset_button.collidepoint(event.pos): reset_game()

            elif game_state == "game":
                if show_intro_message and typing_done: show_intro_message = False

                if inventoryrect.collidepoint(event.pos):
                    cursorclicked = True
                    Functions.play_music("Playful-Days (MMAudio)")
                    game_state = "inventory"
                
                elif menubtnrect.collidepoint(event.pos):
                    cursorclicked = True
                    var_dict = menu_var_dict.copy()
                    game_state = "menu"

                elif popup_button_rect and popup_button_rect.collidepoint(event.pos):
                    if is_night and mgid in ["MG1", "MG2", "MG4"]:
                        closed_message = "This place is closed for the night. Come back during the day!"
                        closed_message_timer = pygame.time.get_ticks()

                    if mgid == "MG1":
                        statemanager = StateManager(MiniGame1.MG1(WIDTH, HEIGHT, MENU, clock), mg1_var_dict.copy())
                        game_state = "mg1"
                        break

                    elif mgid == "MG2":
                        game_state = "mg2"
                        Functions.play_music("MG2_bgm")
                        MiniGame2.screen, MiniGame2.clock, MiniGame2.NOTI = screen, clock, NOTI
                        MiniGame2.event_var = {'VM_EVENT': VM_EVENT, 'is_night': is_night, 'pet_npc': pet_npc,
                                               'mpchange': [vm_income[0][vm_level[0] - 1], vm_income[1][vm_level[1] - 1]],
                                               'vm_level': vm_level, 'xsmall_font': xsmall_font}
                        if MiniGame2.run_game(screen): running = False
                        else:
                            game_state = "game"
                            Functions.play_music("background")
                        
                        break

                    elif mgid == "MG3":
                        game_state = "mg3"
                        Functions.play_music("MG3_bgm")
                        MiniGame3.screen, MiniGame3.NOTI = screen, NOTI
                        MiniGame3.event_var = {'VM_EVENT': VM_EVENT, 'is_night': is_night, 'pet_npc': pet_npc,
                                               'mpchange': [vm_income[0][vm_level[0] - 1], vm_income[1][vm_level[1] - 1]],
                                               'vm_level': vm_level, 'xsmall_font': xsmall_font}
                        MiniGame3.load()
                        MiniGame3.game_state = "mg3_menu" 
                        while MiniGame3.game_state != "exit" and MiniGame3.game_state != "quit":
                            if MiniGame3.game_state == "mg3_menu":
                                MiniGame3.game_state = MiniGame3.mg3_menu()
                            elif MiniGame3.game_state == "instruction":
                                MiniGame3.game_state = MiniGame3.mg3_instruction()
                            elif MiniGame3.game_state == "mg3_base":
                                MiniGame3.game_state = MiniGame3.mg3_base()

                        if MiniGame3.game_state == "quit": running = False
                        else: 
                            game_state = "game"
                            Functions.play_music("background")
                            break  

                    elif mgid == "MG4": 
                        statemanager = StateManager(MiniGame4.MG4(MENU, vm_buyingprices), mg4_var_dict.copy())
                        game_state = "mg4"
                        break

                    elif mgid == "STORE":
                        statemanager = StateManager(Store.STORE(MENU, INVENTORY), store_var_dict.copy())
                        game_state = "store"
                        break 

                    elif mgid == "bedroom":
                        Functions.play_music("bedroom")
                        show_sleep_popup = True
                        Bedroom.screen, Bedroom.clock, Bedroom.NOTI = screen, clock, NOTI
                        Bedroom.event_var = {'VM_EVENT': VM_EVENT, 'is_night': is_night, 'pet_npc': pet_npc,
                                             'mpchange': [vm_income[0][vm_level[0] - 1], vm_income[1][vm_level[1] - 1]],
                                             'vm_level': vm_level, 'xsmall_font': xsmall_font}
                        Bedroom.load()
                        Bedroom.game_state = "bedroom"     
                        Bedroom.slept_once = False         
                        if Bedroom.run(): running = False
                        else: game_state = "game"
                        Functions.play_music("background")
                        break

            elif game_state == "inventory": 
                if INVENTORY.eventhandler(event):
                    Functions.play_music("background")
                    game_state = "game" 

            elif game_state == "menu":
                var_dict, cursorclicked = MENU.eventhandler(event, var_dict)
                if var_dict['mg_state'] == "game": game_state = "game"

                elif var_dict['mg_state'] == "restart": 
                    reset_game()
                    game_state = "intro"

                elif not var_dict['mg_state']: 
                    save_game()
                    saving_timer = 0
                    game_state = "saving"

            mouse_pos = pygame.mouse.get_pos()
            # NPC option selection
            if adeline.talking and adeline.dialogue_state == 0:
                for i, option in enumerate(color_options):
                    option_rect = pygame.Rect(100 + i * 200, HEIGHT - 140, 100, 30)
                    if option_rect.collidepoint(mouse_pos):
                        selected_color_option = i
                        adeline.dialogue_state = 1

            elif tralalelo.talking and tralalelo.dialogue_state == 0:
                for i, option in enumerate(friend_options):
                    option_rect = pygame.Rect(100 + i * 200, HEIGHT - 140, 100, 30)
                    if option_rect.collidepoint(mouse_pos):
                        selected_friend_option = i
                        tralalelo.dialogue_state = 1

        elif event.type == pygame.MOUSEMOTION:
            if game_state == "menu": var_dict, cursorcollide = MENU.eventhandler(event, var_dict)

            elif game_state == "game":
                if menubtnrect.collidepoint(event.pos) or inventoryrect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    cursorcollide = True

            elif game_state == "inventory": 
                INVENTORY.eventhandler(event)
                cursorcollide = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state == "menu": var_dict['dragging'] = False
            elif game_state == "inventory": INVENTORY.eventhandler(event)

        elif event.type == pygame.KEYDOWN:
            if input_locked:
                if event.key == pygame.K_RETURN:
                    button_click.play()
                    show_intro_message = False
                    welcome_message = ""  

            if game_state == "intro":
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 30:
                    player_name += event.unicode

            elif game_state == "game":
                if event.key == pygame.K_RETURN and show_intro_message and typing_done:
                    button_click.play()
                    show_intro_message = False

                # NPC
                if event.key == pygame.K_y and adeline.active and adeline.is_player_near() and not adeline.talking:  
                    adeline.start_dialogue()
                elif event.key == pygame.K_y and tralalelo.active and tralalelo.is_player_near() and not tralalelo.talking:  
                    tralalelo.start_dialogue()
                elif event.key == pygame.K_y and four_d_npc.active and four_d_npc.is_player_near() and not four_d_npc.talking:  
                    four_d_npc.start_dialogue()
                elif event.key == pygame.K_p and pet_npc.active and pet_npc.is_player_near() and not pet_npc.talking and not pet_npc.owned:
                    pet_npc.start_dialogue()
                elif pet_npc.talking:
                    pet_npc.handle_input(event)

                INVENTORY.eventhandler(event, pet_npc, False)

            elif game_state == "inventory": INVENTORY.eventhandler(event, pet_npc, False)

            # Dialogue navigation
            if adeline.talking and adeline.dialogue_state == 0:
                if event.key == pygame.K_LEFT:
                    selected_color_option = (selected_color_option - 1) % len(color_options)
                elif event.key == pygame.K_RIGHT:
                    selected_color_option = (selected_color_option + 1) % len(color_options)
                elif event.key == pygame.K_RETURN:
                    adeline.dialogue_state = 1

            elif tralalelo.talking and tralalelo.dialogue_state == 0:
                if event.key == pygame.K_LEFT:
                    selected_friend_option = (selected_friend_option - 1) % len(friend_options)
                elif event.key == pygame.K_RIGHT:
                    selected_friend_option = (selected_friend_option + 1) % len(friend_options)
                elif event.key == pygame.K_RETURN:
                    tralalelo.dialogue_state = 1
            
            if four_d_npc.talking:
                four_d_npc.handle_input(event)

            elif adeline.talking and event.key == pygame.K_SPACE:
                adeline.end_dialogue()

            elif tralalelo.talking and event.key == pygame.K_SPACE:
                tralalelo.end_dialogue()

            elif four_d_npc.talking and event.key == pygame.K_SPACE:
                four_d_npc.end_dialogue()

        elif event.type == VM1 and not is_night: Functions.update_stats(mpchange=vm_income[0][vm_level[0] - 1])
        elif event.type == VM2 and not is_night: Functions.update_stats(mpchange=vm_income[1][vm_level[1] - 1])

        elif event.type == pet_npc.event:
            if pet_npc.pet_hp:
                pet_npc.pet_hp = max(pet_npc.pet_hp-pet_npc.pet_hpchange, 0)
                if (pet_npc.pet_hp/pet_npc.MAXHP >= pet_npc.hp_percentage['happy']): 
                    Functions.update_stats(hpchange=pet_npc.happy_hpchange)
        
        if statemanager: statemanager.eventhandler(event)
        else: 
            if cursorclicked: Functions.playsound("btnclicked")
            if not cursorcollide: pygame.mouse.set_cursor()
        NOTI.updatetip(event)

    if statemanager: statemanager.update()
    elif game_state == "menu": MENU.update()
    elif (game_state == "game") or (game_state == "inventory"): INVENTORY.update(pet_npc)

    pygame.display.flip()
    
pygame.quit()
