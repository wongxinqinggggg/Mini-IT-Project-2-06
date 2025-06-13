import pygame
import random
from Features import Functions

pygame.init()
pygame.mixer.init()
screen = None
clock = None
NOTI = None
event_var = None
inside_menu_active = False

# Volume control variables
slider_x = 450
slider_y = 150 
slider_width = 200  
slider_height = 8   
knob_radius = 12       
dragging = False    

def run_game(screen):
    global inside_menu_active, volume, dragging, clock
    
    volume = pygame.mixer.music.get_volume()
    font = pygame.font.Font(None, 48)
    input_text = ""
    current_receipt = None
    correct_amount = 0

    def load_and_scale(path):
        try:
            return pygame.transform.scale(pygame.image.load(path).convert(), (1024, 576))
        except:
            return pygame.Surface((1024, 576))
    
    # Game data
    receipt_answers = {
        0: 3.50, 1: 8.00, 2: 6.00, 3: 7.50, 4: 8.30,
        5: 45.10, 6: 15.20, 7: 66.00, 8: 1.30, 9: 9.00
    }

    # Load images
    menu_img = load_and_scale("Assets/Images/MG2-Menu.png")
    instruction_img = load_and_scale("Assets/Images/MG2-Instructions.png")
    success_img = load_and_scale("Assets/Images/MG2-Success.png")
    fail_img = load_and_scale("Assets/Images/MG2-Fail.png")
    Inside_menu_image = pygame.image.load("Assets/Images/MG3_Menu2.png").convert_alpha()
    Menu_image = Functions.mainbtnlist[1]
    receipt_imgs = pygame.image.load("Assets/Images/MG2-Game.png").convert_alpha()
    receipt_imgslist = Functions.get_sprite(1024, 576, receipt_imgs)
    
    # Load sounds
    Functions.play_music("MG2_bgm")

    # Game state
    minigame_state = "menu"
    current_receipt = None
    order_left = 5
    time_left = 30
    input_text = ""
    correct_amount = 0
    paused = False
    poor_message = False
    game_screen_snapshot = None

    # Button areas
    return_button = pygame.Rect(20, 20, 120, 50)
    menu_button_rect = pygame.Rect(920, 20, 80, 80)
    resume_button_rect = pygame.Rect(390, 195, 270, 80)
    restart_button_rect = pygame.Rect(380, 300, 270, 80)
    quit_button_rect = pygame.Rect(380, 400, 270, 80)
    
    # Timer event
    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 1000)
        
    def inside_menu_screen():
        nonlocal paused, game_screen_snapshot
        global dragging, volume, inside_menu_active
        
        while inside_menu_active:
            # Draw the saved game screen snapshot
            if game_screen_snapshot:
                screen.blit(game_screen_snapshot, (0, 0))
            
            # Add dark overlay
            overlay = pygame.Surface((1024, 576), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Draw menu
            screen.blit(Inside_menu_image, (250, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    knob_x = slider_x + int(volume * slider_width)
                    if ((mouse_pos[0] - knob_x) ** 2 + (mouse_pos[1] - (slider_y + slider_height // 2))** 2 <= knob_radius ** 2):
                        dragging = True
                    
                    elif resume_button_rect.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        paused = False
                        inside_menu_active = False
                        return "resume"
                        
                    elif restart_button_rect.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        inside_menu_active = False
                        return "restart"
                        
                    elif quit_button_rect.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        inside_menu_active = False
                        return "quit"
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    
                elif event.type == pygame.MOUSEMOTION and dragging:
                    mouse_x, _ = event.pos
                    new_volume = (mouse_x - slider_x) / slider_width
                    volume = max(0, min(1, new_volume))
                    pygame.mixer.music.set_volume(volume)

                Functions.check_event(event, event_var) # Check for VM and pet event

            # Draw volume control
            pygame.draw.rect(screen, (0, 0, 0), (slider_x, slider_y, slider_width, slider_height))
            knob_x = slider_x + int(volume * slider_width)
            pygame.draw.circle(screen, (0, 0, 0), (knob_x, slider_y + slider_height // 2), knob_radius)

            SLASH_FONT = pygame.font.SysFont('Arial', 80)
            if not volume:
                slash_symbol = SLASH_FONT.render("\\", True, (0, 0, 0))
                screen.blit(slash_symbol, (slider_x + slider_width - 248, slider_y - 45))

            pygame.display.flip()

    def reset_minigame():
        nonlocal order_left, time_left, input_text, current_receipt, correct_amount
        order_left = 5
        time_left = 30
        input_text = ""
        idx = random.randint(0, 9)
        current_receipt = receipt_imgslist[idx]
        correct_amount = receipt_answers[idx]
        Functions.play_music("MG2_bgm")

    running_minigame = True
    while running_minigame:
        clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_minigame = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if minigame_state == "menu":
                    if 400 <= mouse_pos[0] <= 600 and 300 <= mouse_pos[1] <= 480:
                        Functions.playsound("btnclicked")
                        if Functions.energy >= 20:
                            reset_minigame()
                            minigame_state = "playing"
                            Functions.update_stats(hpchange=-20)
                            Functions.add_floating_text("-20", "hp", (255, 0, 0))
                            poor_message = False
                        else:
                            poor_message = True
                    elif 900 <= mouse_pos[0] <= 1000 and 100 <= mouse_pos[1] <= 160:
                        Functions.playsound("btnclicked")
                        minigame_state = "instruction"
                    elif return_button.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        running_minigame = False
                    elif menu_button_rect.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        game_screen_snapshot = screen.copy()
                        inside_menu_active = True

                elif minigame_state == "instruction":
                    if menu_button_rect.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        game_screen_snapshot = screen.copy()
                        inside_menu_active = True
                    else:
                        minigame_state = "menu"

                elif minigame_state == "playing":
                    if menu_button_rect.collidepoint(mouse_pos):
                        Functions.playsound("btnclicked")
                        game_screen_snapshot = screen.copy()
                        paused = True
                        inside_menu_active = True
                        pygame.time.set_timer(TIMER_EVENT, 0)

            elif event.type == pygame.KEYDOWN and minigame_state == "playing" and not paused:
                if event.key == pygame.K_RETURN:
                    try:
                        if abs(float(input_text) - correct_amount) < 0.01:
                            order_left -= 1
                            if order_left == 0:
                                minigame_state = "success"
                                Functions.playsound("success")
                                Functions.update_stats(mpchange=50)
                                Functions.add_floating_text("+50", "mp", (0, 255, 0))
                            else:
                                idx = random.randint(0, 9)
                                current_receipt = receipt_imgslist[idx]
                                correct_amount = receipt_answers[idx]
                                input_text = ""
                        else:
                            minigame_state = "fail"
                            Functions.playsound("fail")
                    except:
                        minigame_state = "fail"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    if len(input_text) < 6:
                        input_text += event.unicode

            if event.type == TIMER_EVENT and minigame_state == "playing" and not paused:
                time_left -= 1
                if time_left <= 0:
                    minigame_state = "fail"
                    Functions.playsound("fail")

            Functions.check_event(event, event_var) # Check for VM and pet event

        # Handle menu results
        if inside_menu_active:
            result = inside_menu_screen()
            if result == "quit":
                running_minigame = False
            elif result == "restart":
                reset_minigame()
                minigame_state = "menu"
                paused = False
            elif result == "resume":
                paused = False
                if minigame_state == "playing":
                    pygame.time.set_timer(TIMER_EVENT, 1000)

        # Draw game state
        if minigame_state == "menu":
            screen.blit(menu_img, (0, 0))
            screen.blit(Menu_image, (920, 20))
            
            if poor_message:
                poor_font = pygame.font.Font(None, 60)
                poor_text = poor_font.render("You are too tired! (Need at least 20 energy)", True, (0, 0, 0))
                screen.blit(poor_text, (150, 250))
            
        elif minigame_state == "instruction":
            screen.blit(instruction_img, (0, 0))
            screen.blit(Menu_image, (920, 20))
            
        elif minigame_state == "playing":
            if not paused:
                screen.blit(current_receipt, (0, 0))
                screen.blit(font.render(f"Orders Left: {order_left}", True, (0, 0, 0)), (40, 40))
                screen.blit(font.render(f"Time: {time_left}", True, (0, 0, 0)), (750, 40))

                input_surface = font.render(input_text, True, (0, 0, 0))
                input_rect = input_surface.get_rect(center=(700, 175))
                pygame.draw.rect(screen, (200, 200, 200), input_rect.inflate(20, 20))
                screen.blit(input_surface, input_rect)
                
                screen.blit(Menu_image, (920, 20))

        elif minigame_state == "success":
            screen.blit(success_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(2000)
            running_minigame = False
            
        elif minigame_state == "fail":
            screen.blit(fail_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(2000)
            running_minigame = False
        
        if minigame_state != "playing" and minigame_state != "instruction":
            Functions.display_stats(screen)
            NOTI.displayicon(event_var['vm_level'], event_var['pet_npc'], event_var['xsmall_font'], event_var['is_night'])
        Functions.draw_floating_texts(screen)
        pygame.display.flip()
