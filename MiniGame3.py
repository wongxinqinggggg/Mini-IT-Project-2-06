import pygame
import random
import time

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("Minigame 3")
floating_texts = [] 
post_game_floating_texts = []
inside_menu_active = False

# Volume slider variables
slider_x = 450
slider_y = 150 
slider_width = 200  
slider_height = 8   
knob_radius = 12    
volume = 0.5        
dragging = False    

# Load images
full_map_image = pygame.image.load("MiniGame3/Asset/Images/final_map.png").convert()
mg3_menu_image = pygame.image.load("MiniGame3/Asset/Images/MG3-Menu.png").convert()
mg3_question_image = pygame.image.load("MiniGame3/Asset/Images/MG-Elements_1.png").convert_alpha()
mg3_instruction_image = pygame.image.load("MiniGame3/Asset/Images/MG3-Instructions.png").convert()
mg3_base_image = pygame.image.load("MiniGame3/Asset/Images/MG3-Base.png").convert()
mge_statsbar_image = pygame.image.load("MiniGame3/Asset/Images/MGE_Statsbar.png").convert_alpha()
Menu_image = pygame.image.load("MiniGame3/Asset/Images/Menu-button.png").convert_alpha()
Inside_menu_image = pygame.image.load("MiniGame3/Asset/Images/Menu-2.png").convert_alpha()


# Load sounds
success_sound = pygame.mixer.Sound("MiniGame3/Asset/Audio/success.mp3")
fail_sound = pygame.mixer.Sound("MiniGame3/Asset/Audio/fail.mp3")
button_click = pygame.mixer.Sound("MiniGame3/Asset/Audio/button_click.mp3")
pygame.mixer.music.load("MiniGame3/Asset/Audio/Minigame3_bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Paragraphs
paragraphs = [
    "The sun was setting behind the hills, painting the sky in shades of orange and pink. Birds flew back to their nests while the air grew cooler. It was the perfect time for a quiet walk through the park.",
    "In a world where information flows freely and instantaneously, it's more important than ever to distinguish fact from fiction. Misinformation can spread like wildfire, affecting public opinion and societal stability. A balanced approach to media literacy and critical thinking is crucial.",
    "The library was quiet except for the soft rustle of pages turning. Rows of books stretched across the room, each filled with knowledge and adventure. A young girl sat at a corner table, her eyes glued to a story about dragons and hidden treasure.",
    "A dog barked in the distance as the wind rustled the trees. Leaves danced across the sidewalk, crunching under every step. Autumn had truly arrived.",
    "He tied his shoes, grabbed his backpack, and headed out the door. School was only a few blocks away, but he enjoyed the fresh morning air during the walk.",
    "Exploring the depths of the ocean is as challenging as exploring outer space, with its vast, uncharted territories and hidden ecosystems. Deep-sea expeditions reveal species and phenomena that remain largely unknown, highlighting the mysteries of our planet's most inaccessible environments.",
    "At the edge of the forest stood an old cabin, half-covered in ivy. No one had lived there in years, but something about it still felt alive. Leaves rustled in the wind, and every now and then, a bird landed on the roof. It was quiet, but not empty.",
    "She took a deep breath and stepped on stage. Her heart was racing, but she remembered all her lines. The spotlight was bright, and the audience waited in silence.",
    "The boy threw a stone into the lake and watched the ripples spread. It was a calm day, with clouds drifting slowly above. Everything felt peaceful and quiet.",
    "The human brain is one of the most complex and least understood organs in the body, with over 100 billion neurons communicating through trillions of synapses. Despite decades of research, many aspects of brain function remain a mystery, fueling ongoing investigations into neurological disorders."
]

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

# Floating text
def add_floating_text(text, x, y, color):
    floating_texts.append({"text": text, "x": x, "y": y, "start_time": pygame.time.get_ticks(), "color": color})

def draw_floating_texts():
    current_time = pygame.time.get_ticks()
    texts_to_remove = []
    for ft in floating_texts[:]:
        elapsed = (current_time - ft["start_time"]) / 1000
        if elapsed > 1.5:
            texts_to_remove.append(ft)
            continue

        offset_y = int(30 * elapsed)
        alpha = max(255 - int(255 * (elapsed / 1.5)), 0)

        # Create the text surface
        text_surface = floating_font.render(ft["text"], True, ft["color"])
        text_surface.set_alpha(alpha)

        # Create an outline by drawing black text slightly shifted
        outline_color = (50, 50, 50)  
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    outline_surface = floating_font.render(ft["text"], True, outline_color)
                    outline_surface.set_alpha(alpha)
                    screen.blit(outline_surface, (ft["x"] + dx, ft["y"] - offset_y + dy))
    
        screen.blit(text_surface, (ft["x"], ft["y"] - offset_y))

    for ft in texts_to_remove:
        floating_texts.remove(ft)

font = pygame.font.SysFont('PressStart2P.ttf', 28, bold=True)
floating_font = pygame.font.Font("PressStart2P.ttf", 30)  

# UI Rects
question_button_rect = pygame.Rect(710, 100, 315,294)
exit_button_rect = pygame.Rect(30, 30, 100, 50)
back_button_rect = pygame.Rect(460, 400, 120, 50)
start_button_rect = pygame.Rect(450, 350, 150, 60)
retry_button_rect = pygame.Rect(450, 460, 120, 50)
menu_button_rect = pygame.Rect(720, 0, 301, 576)
restart_button_rect = pygame.Rect(450, 520, 120, 50)
quit_button_rect = pygame.Rect(450, 580, 120, 50)
resume_button_rect = pygame.Rect(450, 200, 120, 50)


# Set Energy etc
energy = 120
money = 100
total_energy_spent = 0
total_money_earned = 0

def draw_timer_box(elapsed_time):
    pygame.draw.rect(screen, (0, 128, 0), (870, 10, 140, 40))
    timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, (255, 255, 255))
    screen.blit(timer_text, (880, 20))

def wrap_text(text, font, max_width):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
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

def full_map_screen():
    global total_energy_spent, total_money_earned
    custom_font = pygame.font.Font("MiniGame3/Asset/Font/PressStart2P.ttf", 33)

    # Transfer final post-game floating texts
    if total_energy_spent > 0:
        add_floating_text(f"-{total_energy_spent}", 250, 28, (128, 128, 128))
        total_energy_spent = 0

    if total_money_earned > 0:
        add_floating_text(f"+{total_money_earned}", 250, 110, (128, 128, 128))
        total_money_earned = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                return "mg3_menu"

        screen.blit(full_map_image, (0, 0))
        screen.blit(mge_statsbar_image, (0, 0))

        energy_text = custom_font.render(f"{energy:>3}", True, (0, 0, 0)) 
        money_text = custom_font.render(f"{money:>3}", True, (0, 0, 0))
        screen.blit(energy_text, (120, 28))
        screen.blit(money_text, (123, 105))
        
        draw_floating_texts()
        pygame.display.flip()

def mg3_menu():
    global inside_menu_active  # Ensure inside_menu_active is accessed globally

    error_display_time = 0
    error_duration = 2

    while True:
        screen.fill((0, 0, 0))  # Clear screen for every loop iteration

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if question_button_rect.collidepoint(event.pos):
                    button_click.play()
                    return "instruction"
                elif exit_button_rect.collidepoint(event.pos):
                    button_click.play()
                    return "full_map"
                elif start_button_rect.collidepoint(event.pos):
                    if energy < 20:
                        button_click.play()
                        error_display_time = time.time()
                    else:
                        button_click.play()
                        return "mg3_base"
                elif menu_button_rect.collidepoint(event.pos):  # Menu button click event
                    button_click.play()
                    inside_menu_active = not inside_menu_active  # Toggle inside menu visibility
                    print(f"Inside menu active state toggled: {inside_menu_active}")  # Debug print

        # Show the background of the main menu
        screen.blit(mg3_menu_image, (0, 0))
        screen.blit(Menu_image, (720, 0))  # Menu button
        screen.blit(mg3_question_image, (710, 100))  # Question button

        # Display the inside menu if it's active
        if inside_menu_active:
            screen.blit(Inside_menu_image, (250, 50))  # Inside menu background
            inside_menu_screen()  # Inside menu options or interactions

        # Handle the error message if the energy is insufficient
        if time.time() - error_display_time < error_duration:
            error_font = pygame.font.SysFont(None, 36)
            error_text = error_font.render("Error: Insufficient HP", True, (255, 0, 0))
            screen.blit(error_text, (360, 450))
            
        pygame.display.flip()

def inside_menu_screen():
    global dragging, volume

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                return "quit"  

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                knob_x = slider_x + int(volume * slider_width)
                if (mouse_x - knob_x) ** 2 + (mouse_y - (slider_y + slider_height // 2)) ** 2 <= knob_radius ** 2:
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, _ = event.pos
                    new_volume = (mouse_x - slider_x) / slider_width
                    new_volume = max(0, min(1, new_volume))
                    volume = new_volume
                    pygame.mixer.music.set_volume(volume)

        screen.blit(Inside_menu_image, (250, 50))  

        # Draw the slider bar
        pygame.draw.rect(screen, (0, 0, 0), (slider_x, slider_y, slider_width, slider_height))

        # Draw the knob
        knob_x = slider_x + int(volume * slider_width)
        pygame.draw.circle(screen, (0, 0, 0), (knob_x, slider_y + slider_height // 2), knob_radius)
        pygame.display.flip()


def mg3_instruction():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    button_click.play()
                    return "mg3_menu"
        screen.blit(mg3_instruction_image, (0, 0))
        draw_floating_texts()
        pygame.display.flip()


def mg3_base():
    global energy, money, total_energy_spent, total_money_earned
    attempts = 1
    energy -= 20
    total_energy_spent += 20
    cursor_x = 100
    cursor_y = 300

    print("Entered mg3_base")

    paragraph = random.choice(paragraphs)
    user_input = ""
    typing_started = False
    remaining_time = 60.0
    result_shown = False
    clock = pygame.time.Clock()
    result_message = ""
    high_score = load_high_score()
    new_high = False
    wpm = 0
    exit_mg3_base_rect = pygame.Rect(30, 30, 100, 50)

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
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if result_shown and retry_button_rect.collidepoint(event.pos):
                    if energy >= 20:
                        button_click.play()
                        energy -= 20
                        attempts += 1
                        total_energy_spent += 20
                        paragraph = random.choice(paragraphs)
                        user_input = ""
                        typing_started = False
                        remaining_time = 60.0
                        result_shown = False
                        result_message = ""
                        success_sound.stop()
                        fail_sound.stop()
                    else:
                        button_click.play()
                        result_message = "Not enough energy to retry."
                if exit_mg3_base_rect.collidepoint(event.pos):
                    success_sound.stop()
                    fail_sound.stop()
                    button_click.play()
                    return "full_map"
            elif event.type == pygame.KEYDOWN and not result_shown:
                if not typing_started:
                    typing_started = True
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                elif event.unicode and event.unicode.isprintable():
                    user_input += event.unicode

        screen.blit(mg3_base_image, (0, 0))
        pygame.draw.rect(screen, (128, 0, 0), exit_mg3_base_rect)
        exit_text = font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (exit_mg3_base_rect.x + 25, exit_mg3_base_rect.y + 15))

        y = 150
        for line in wrap_text(paragraph, font, 800):
            screen.blit(font.render(line, True, (0, 0, 0)), (100, y))
            y += 30

        typed_lines = wrap_typed_text(user_input, font, 800)
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
            if (pygame.time.get_ticks() // 500) % 2 == 0:  # Blink every 500ms
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
                new_high = True
            money += 50
            total_money_earned += 50
            success_sound.play()

        if result_shown:
            pygame.draw.rect(screen, (0, 0, 0), (300, 250, 430, 100))
            screen.blit(font.render(result_message, True, (255, 255, 255)), (320, 270))
            screen.blit(font.render(f"High Score: {high_score:.2f} WPM", True, (255, 255, 0)), (320, 300))
            
            # Draw the retry button
            pygame.draw.rect(screen, (200, 0, 0), retry_button_rect)
            retry_text = font.render("Retry", True, (255, 255, 255))
            retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
            screen.blit(retry_text, retry_text_rect)
        
        pygame.display.flip()

# Game loop
game_state = "full_map"
while game_state != "quit":
    print("Current game state:", game_state)
    if game_state == "full_map":
        game_state = full_map_screen()
    elif game_state == "mg3_menu":
        game_state = mg3_menu()
    elif game_state == "instruction":
        game_state = mg3_instruction()
    elif game_state == "mg3_base":
        game_state = mg3_base()
    elif game_state == "inside_menu":
        game_state =  inside_menu_screen()













