import pygame
import random
import time
from Features import Functions

pygame.init()
pygame.mixer.init()
screen = None
NOTI = None
event_var = None

# Game loop
game_state = "quit"

# Volume slider variables
slider_x = 450
slider_y = 150 
slider_width = 200  
slider_height = 8   
knob_radius = 12    

# Load images
def load():
    global mg3_menu_image, mg3_question_image, mg3_instruction_image, mg3_base_image
    global mge_statsbar_image, Inside_menu_image, menubtn 
    global success_sound, fail_sound
    mg3_menu_image = pygame.image.load("Assets/Images/MG3-Menu.png").convert()
    mg3_question_image = Functions.mainbtnlist[0]
    mg3_instruction_image = pygame.image.load("Assets/Images/MG3-Instructions.png").convert()
    mg3_base_image = pygame.image.load("Assets/Images/MG3-Base.png").convert()
    menubtn = Functions.mainbtnlist[1]
    Inside_menu_image = pygame.image.load("Assets/Images/MG3_Menu2.png").convert_alpha()

    # Load sounds
    success_sound = pygame.mixer.Sound("Assets/Audio/success.mp3")
    fail_sound = pygame.mixer.Sound("Assets/Audio/fail.mp3")
    Functions.play_music("MG3_bgm")

# Words
words = []
word_limit = (150, 200)
with open("mg3_words.txt", "r") as f:
    txt = f.read()
    words = txt.split(", ")

# High score functions
def load_high_score():
    try:
        with open("mg3_highscore.txt", "r") as f:
            return float(f.read())
    except:
        return 0.0

def save_high_score(score):
    with open("mg3_highscore.txt", "w") as f:
        f.write(f"{score:.2f}")

font = pygame.font.SysFont('Assets/Fonts/PressStart2P.ttf', 28, bold=True)
floating_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 30)  
custom_font = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 32)

# UI Rects
question_button_rect = pygame.Rect(920, 120, 80, 80)
back_button_rect = pygame.Rect(460, 400, 120, 50)
start_button_rect = pygame.Rect(450, 350, 150, 60)
retry_button_rect = pygame.Rect(450, 460, 120, 50)
menu_button_base_screen = pygame.Rect(920, 20, 80, 80) 
restart_button_rect = pygame.Rect(380, 300, 270, 80)
quit_button_rect = pygame.Rect(380, 400, 270, 80)
resume_button_rect = pygame.Rect(380, 195, 270, 80)

# Set Energy etc
total_energy_spent = 0
total_money_earned = 0

def draw_timer_box(elapsed_time):
    pygame.draw.rect(screen, (0, 128, 0), (500, 10, 140, 40))
    timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, (255, 255, 255))
    screen.blit(timer_text, (510, 20))

def wrap_text(text, font, max_width):
    temp = text.split()
    max_char = max_width//font.size('w')[0]
    print(max_char, max_width//font.size('i')[0])
    lines, current_line, words = [], "", []

    for word in temp: 
        if font.size(word)[0] >= max_width:
            words.extend(wrap_typed_text(word, font, max_width))
        else:
            words.append(word)
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line: lines.append(current_line)
    return lines

def wrap_typed_text(text, font, max_width):
    lines, current_line = [], ""
    for char in text:
        if font.size(current_line + char)[0] < max_width:
            current_line += char
        else:
            lines.append(current_line)
            current_line = char
    if current_line:
        lines.append(current_line)
    return lines

def create_new_paragraph():
    paragraph = ""
    while len(paragraph) < word_limit[0]:
        i = random.randint(0, len(words)-1)
        temp = paragraph + words[i] + " "
        if len(temp) <= word_limit[1]: paragraph = temp

    return paragraph

def full_map_screen():
    global total_energy_spent, total_money_earned

    # Transfer final post-game floating texts
    if total_energy_spent > 0:
        Functions.add_floating_text(f"-{total_energy_spent}", 'hp')
        total_energy_spent = 0

    if total_money_earned > 0:
        Functions.add_floating_text(f"+{total_money_earned}", 'mp')
        total_money_earned = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3: return "mg3_menu"
            Functions.check_event(event, event_var) # Check for VM and pet event

        Functions.display_stats(screen)
        NOTI.displayicon(event_var['vm_level'], event_var['pet_npc'], event_var['xsmall_font'], event_var['is_night'])
        Functions.draw_floating_texts(screen)
        pygame.display.flip()

def mg3_menu():
    inside_menu_active = False
    error_display_time = 0
    error_duration = 2
    result = None  

    while True:
        screen.fill((0, 0, 0))  

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if question_button_rect.collidepoint(event.pos):
                    Functions.playsound("btnclicked")
                    return "instruction"
                elif start_button_rect.collidepoint(event.pos):
                    if Functions.energy < 20:
                        Functions.playsound("btnclicked")
                        error_display_time = time.time()
                    else:
                        Functions.playsound("btnclicked")
                        return "mg3_base"
                elif menu_button_base_screen.collidepoint(event.pos):  
                    Functions.playsound("btnclicked")
                    inside_menu_active = not inside_menu_active  

            Functions.check_event(event, event_var) # Check for VM and pet event

        # Show the background of the main menu
        screen.blit(mg3_menu_image, (0, 0))
        screen.blit(menubtn, (920, 20))  
        screen.blit(mg3_question_image, (920, 120))  

        # Display the inside menu if it's active
        if inside_menu_active:
            result = inside_menu_screen()  
            inside_menu_active = False 
            if result == "resume": pass
            elif result == "restart": return "mg3_base"
            else: return result

        # Handle the error message if the energy is insufficient
        if time.time() - error_display_time < error_duration:
            error_font = pygame.font.SysFont(None, 36)
            error_text = error_font.render("Error: Insufficient HP", True, (255, 0, 0))
            screen.blit(error_text, (380, 450))

        Functions.display_stats(screen)
        NOTI.displayicon(event_var['vm_level'], event_var['pet_npc'], event_var['xsmall_font'], event_var['is_night'])
        pygame.display.flip()

def inside_menu_screen():
    dragging, volume = False, pygame.mixer.music.get_volume()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos

                if resume_button_rect.collidepoint(event.pos):
                    Functions.playsound("btnclicked")
                    return "resume"

                elif restart_button_rect.collidepoint(event.pos):
                    Functions.playsound("btnclicked")
                    return "restart"

                elif quit_button_rect.collidepoint(event.pos):
                    Functions.playsound("btnclicked")
                    return "exit"

                # Handle volume dragging
                knob_x = slider_x + int(volume * slider_width)
                if (mouse_x - knob_x) ** 2 + (mouse_y - (slider_y + slider_height // 2)) ** 2 <= knob_radius ** 2:
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, _ = event.pos
                new_volume = (mouse_x - slider_x) / slider_width
                volume = max(0, min(1, new_volume))
                pygame.mixer.music.set_volume(volume)

            Functions.check_event(event, event_var) # Check for VM and pet event

        screen.blit(Inside_menu_image, (250, 50))

        # Draw the volume slider
        pygame.draw.rect(screen, (0, 0, 0), (slider_x, slider_y, slider_width, slider_height))
        knob_x = slider_x + int(volume * slider_width)
        pygame.draw.circle(screen, (0, 0, 0), (knob_x, slider_y + slider_height // 2), knob_radius)

        SLASH_FONT = pygame.font.SysFont('Arial', 80)
        if not volume:
            slash_symbol = SLASH_FONT.render("\\", True, (0, 0, 0))
            screen.blit(slash_symbol, (slider_x + slider_width - 248, slider_y - 45))
        pygame.display.flip()

def mg3_instruction():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    Functions.playsound("btnclicked")
                    return "mg3_menu"
                
            Functions.check_event(event, event_var) # Check for VM and pet event

        screen.blit(mg3_instruction_image, (0, 0))
        Functions.draw_floating_texts(screen)
        pygame.display.flip()

def mg3_base():
    global total_energy_spent, total_money_earned
    attempts = 1
    Functions.update_stats(hpchange=-20)
    total_energy_spent += 20
    cursor_x = 100
    cursor_y = 300
    paragraph = create_new_paragraph()
    user_input = ""
    typing_started = False
    remaining_time = 60.0
    result_shown = False
    clock = pygame.time.Clock()
    result_message = ""
    high_score = load_high_score()
    wpm = 0

    while True:
        dt = clock.tick(60) / 1000
        if typing_started and not result_shown:
            remaining_time -= dt
            if remaining_time <= 0:
                remaining_time = 0
                result_message = "Time's up! Try again."
                fail_sound.play()
                result_shown = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if result_shown and retry_button_rect.collidepoint(event.pos):
                    if Functions.energy >= 20:
                        Functions.playsound("btnclicked")
                        Functions.update_stats(hpchange=-20)
                        attempts += 1
                        total_energy_spent += 20
                        paragraph = create_new_paragraph()
                        user_input = ""
                        typing_started = False
                        remaining_time = 60.0
                        result_shown = False
                        result_message = ""
                        success_sound.stop()
                        fail_sound.stop()
                    else:
                        Functions.playsound("btnclicked")
                        result_message = "Not enough energy to retry."

                elif menu_button_base_screen.collidepoint(event.pos):
                    Functions.playsound("btnclicked")
                    result = inside_menu_screen()
                    if result == "resume": continue

                    elif result == "restart":
                        if Functions.energy >= 20:
                            Functions.update_stats(hpchange=-20)
                            total_energy_spent += 20
                            paragraph = create_new_paragraph()
                            user_input = ""
                            typing_started = False
                            remaining_time = 60.0
                            result_shown = False
                            result_message = ""
                            success_sound.stop()
                            fail_sound.stop()
                        else:
                            result_message = "Not enough energy to restart."
                        continue

                    elif result == "exit":
                        success_sound.stop()
                        fail_sound.stop()
                        return "exit"
                    
                    return result

            elif event.type == pygame.KEYDOWN and not result_shown:
                if not typing_started: typing_started = True
                if event.key == pygame.K_BACKSPACE: user_input = user_input[:-1]
                elif event.unicode and event.unicode.isprintable():
                    if len(user_input) < 300: user_input += event.unicode

            Functions.check_event(event, event_var) # Check for VM and pet event

        screen.blit(mg3_base_image, (0, 0))
        screen.blit(menubtn, (920, 20))
        Functions.display_stats(screen)
        NOTI.displayicon(event_var['vm_level'], event_var['pet_npc'], event_var['xsmall_font'], event_var['is_night'])

        y = 200
        for line in wrap_text(paragraph, font, 800):
            screen.blit(font.render(line, True, (0, 0, 0)), (100, y))
            y += 30

        typed_lines = wrap_text(user_input, font, 800)
        y = 300
        for line in typed_lines:
            x_offset = 100
            for i, char in enumerate(line):
                global_index = sum(len(l) for l in typed_lines[:typed_lines.index(line)]) + i
                correct_char = paragraph[global_index] if global_index < len(paragraph) else ''
                color = (0, 0, 255) if char == correct_char else (255, 0, 0)
                screen.blit(font.render(char, True, color), (x_offset, y))
                x_offset += font.size(char)[0]
            y += 30

        if not result_shown:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + font.get_height()), 2)
            if typed_lines:
                last_line = typed_lines[-1]
                cursor_x = 100
                for char in last_line:
                    cursor_x += font.size(char)[0]
                cursor_y = 300 + (len(typed_lines) - 1) * 30
        else:
            cursor_x = 100
            cursor_y = 300
        pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + font.get_height()), 2)

        if typing_started and not result_shown:
            draw_timer_box(remaining_time)

        if not result_shown and user_input == paragraph:
            elapsed_time = 60.0 - remaining_time
            wpm = (len(user_input) / 5) * (60 / elapsed_time) if elapsed_time > 0 else 0
            result_message = f"Success! Your typing speed: {wpm:.2f} WPM"
            result_shown = True
            if wpm > high_score:
                save_high_score(wpm)
                high_score = wpm
            Functions.update_stats(mpchange=50)
            total_money_earned += 50
            success_sound.play()

        if result_shown:
            pygame.draw.rect(screen, (0, 0, 0), (300, 250, 430, 100))
            screen.blit(font.render(result_message, True, (255, 255, 255)), (320, 270))
            screen.blit(font.render(f"High Score: {high_score:.2f} WPM", True, (255, 255, 0)), (320, 300))

            pygame.draw.rect(screen, (200, 0, 0), retry_button_rect)
            retry_text = font.render("Retry", True, (255, 255, 255))
            retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
            screen.blit(retry_text, retry_text_rect)

        # Transfer final post-game floating texts
        if total_energy_spent > 0:
            Functions.add_floating_text(f"-{total_energy_spent}", 'hp')
            total_energy_spent = 0

        if total_money_earned > 0:
            Functions.add_floating_text(f"+{total_money_earned}", 'mp')
            total_money_earned = 0
        
        Functions.draw_floating_texts(screen)
        pygame.display.flip()
