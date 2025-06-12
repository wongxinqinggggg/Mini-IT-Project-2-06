import pygame
import random
from Features import Functions

pygame.init()
pygame.mixer.init()
screen = None
floating_texts = [] 
inside_menu_active = False
total_energy_spent = 0
total_money_earned = 0

# Volume control variables
slider_x = 450
slider_y = 150 
slider_width = 200  
slider_height = 8   
knob_radius = 12    
volume = 0.5        
dragging = False    

def add_floating_text(text, x, y, color):
    floating_texts.append({
        "text": text, 
        "x": x, 
        "y": y, 
        "start_time": pygame.time.get_ticks(), 
        "color": color
    })

def run_game(screen):
    global inside_menu_active, volume, dragging
    
    clock = pygame.time.Clock()
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

    receipt_imgs = [load_and_scale(f"Assets/Images/MG2-Game{i}.png") for i in range(1, 11)]

    # Load images
    menu_img = load_and_scale("Assets/Images/MG2-Menu.png")
    instruction_img = load_and_scale("Assets/Images/MG2-Instructions.png")
    success_img = load_and_scale("Assets/Images/MG2-Success.png")
    fail_img = load_and_scale("Assets/Images/MG2-Fail.png")
    mge_statsbar_image = pygame.image.load("Assets/Images/MAIN_Statsbar.png").convert_alpha()
    Inside_menu_image = pygame.image.load("Assets/Images/MG3_Menu2.png").convert_alpha()
    Menu_image = Functions.mainbtnlist[1]
    
    # Load sounds
    success_sound = pygame.mixer.Sound("Assets/Audio/success.mp3")
    fail_sound = pygame.mixer.Sound("Assets/Audio/fail.mp3")
    button_click = pygame.mixer.Sound("Assets/Audio/button_click.mp3")
    pygame.mixer.music.load("Assets/Audio/MG2_bgm.mp3")
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

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

    def draw_statsbar():
        stats_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 25)
        if minigame_state != "playing":
            screen.blit(mge_statsbar_image, (0, 0))
            energy_text = stats_font.render(f"{Functions.energy:06}", True, (0, 0, 0))
            money_text = stats_font.render(f"{Functions.money:06}", True, (0, 0, 0))
            screen.blit(energy_text, (80, 28))
            screen.blit(money_text, (80, 105))
        
        current_time = pygame.time.get_ticks()
        texts_to_remove = []
        for ft in floating_texts[:]:
            elapsed = (current_time - ft["start_time"]) / 1000
            if elapsed > 1.5:
                texts_to_remove.append(ft)
                continue

            offset_y = int(30 * elapsed)
            alpha = max(255 - int(255 * (elapsed / 1.5)), 0)
            text_surface = stats_font.render(ft["text"], True, ft["color"])
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, (ft["x"], ft["y"] - offset_y))

        for ft in texts_to_remove:
            floating_texts.remove(ft)
        
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
                        button_click.play()
                        paused = False
                        inside_menu_active = False
                        return "resume"
                        
                    elif restart_button_rect.collidepoint(mouse_pos):
                        button_click.play()
                        inside_menu_active = False
                        return "restart"
                        
                    elif quit_button_rect.collidepoint(mouse_pos):
                        button_click.play()
                        inside_menu_active = False
                        return "quit"
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    
                elif event.type == pygame.MOUSEMOTION and dragging:
                    mouse_x, _ = event.pos
                    new_volume = (mouse_x - slider_x) / slider_width
                    volume = max(0, min(1, new_volume))
                    pygame.mixer.music.set_volume(volume)

            # Draw volume control
            pygame.draw.rect(screen, (0, 0, 0), (slider_x, slider_y, slider_width, slider_height))
            knob_x = slider_x + int(volume * slider_width)
            pygame.draw.circle(screen, (0, 0, 0), (knob_x, slider_y + slider_height // 2), knob_radius)

            SLASH_FONT = pygame.font.SysFont('Arial', 80)
            if volume == 0:
                slash_symbol = SLASH_FONT.render("\\", True, (0, 0, 0))
                screen.blit(slash_symbol, (slider_x + slider_width - 248, slider_y - 45))

            pygame.display.flip()

    def reset_minigame():
        nonlocal order_left, time_left, input_text, current_receipt, correct_amount
        order_left = 5
        time_left = 30
        input_text = ""
        idx = random.randint(0, 9)
        current_receipt = receipt_imgs[idx]
        correct_amount = receipt_answers[idx]
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    running_minigame = True
    while running_minigame:
        dt = clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_minigame = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if minigame_state == "menu":
                    if 400 <= mouse_pos[0] <= 600 and 300 <= mouse_pos[1] <= 480:
                        button_click.play()
                        if Functions.money >= 200:
                            reset_minigame()
                            minigame_state = "playing"
                            Functions.update_stats(0, -200)
                            add_floating_text("-200", 250, 28, (255, 0, 0))
                            poor_message = False
                        else:
                            poor_message = True
                    elif 900 <= mouse_pos[0] <= 1000 and 100 <= mouse_pos[1] <= 160:
                        button_click.play()
                        minigame_state = "instruction"
                    elif return_button.collidepoint(mouse_pos):
                        button_click.play()
                        running_minigame = False
                    elif menu_button_rect.collidepoint(mouse_pos):
                        button_click.play()
                        game_screen_snapshot = screen.copy()
                        inside_menu_active = True

                elif minigame_state == "instruction":
                    if menu_button_rect.collidepoint(mouse_pos):
                        button_click.play()
                        game_screen_snapshot = screen.copy()
                        inside_menu_active = True
                    else:
                        minigame_state = "menu"

                elif minigame_state == "playing":
                    if menu_button_rect.collidepoint(mouse_pos):
                        button_click.play()
                        game_screen_snapshot = screen.copy()
                        paused = True
                        inside_menu_active = True
                        pause_time = time_left
                        pygame.time.set_timer(TIMER_EVENT, 0)

            if event.type == pygame.KEYDOWN and minigame_state == "playing" and not paused:
                if event.key == pygame.K_RETURN:
                    try:
                        if abs(float(input_text) - correct_amount) < 0.01:
                            order_left -= 1
                            if order_left == 0:
                                minigame_state = "success"
                                success_sound.play()
                                Functions.update_stats(0, 1000)
                                add_floating_text("+1000", 250, 110, (0, 255, 0))
                            else:
                                idx = random.randint(0, 9)
                                current_receipt = receipt_imgs[idx]
                                correct_amount = receipt_answers[idx]
                                input_text = ""
                        else:
                            minigame_state = "fail"
                            fail_sound.play()
                    except:
                        minigame_state = "fail"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    input_text += event.unicode

            if event.type == TIMER_EVENT and minigame_state == "playing" and not paused:
                time_left -= 1
                if time_left <= 0:
                    minigame_state = "fail"
                    fail_sound.play()

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
            screen.blit(Menu_image, (720, 0))
            
            if poor_message:
                poor_font = pygame.font.Font(None, 60)
                poor_text = poor_font.render("You are too poor! (Need at least $200)", True, (0, 0, 0))
                screen.blit(poor_text, (150, 250))
            
        elif minigame_state == "instruction":
            screen.blit(instruction_img, (0, 0))
            screen.blit(Menu_image, (720, 0))
            
        elif minigame_state == "playing":
            if not paused:
                screen.blit(current_receipt, (0, 0))
                screen.blit(font.render(f"Orders Left: {order_left}", True, (0, 0, 0)), (30, 40))
                screen.blit(font.render(f"Time: {time_left}", True, (0, 0, 0)), (774, 40))

                input_surface = font.render(input_text, True, (0, 0, 0))
                input_rect = input_surface.get_rect(center=(700, 175))
                pygame.draw.rect(screen, (200, 200, 200), input_rect.inflate(20, 20))
                screen.blit(input_surface, input_rect)
                
                screen.blit(Menu_image, (720, 0))

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
        
        draw_statsbar()
        pygame.display.flip()

    pygame.time.set_timer(TIMER_EVENT, 0)
    pygame.mixer.music.stop()
