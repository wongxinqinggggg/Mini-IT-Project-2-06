import pygame

MAXHP, MAXMP = 999999, 999999
floating_texts = [] 
floating_texts_pos = {'hp': {'x': 300, 'y': 40}, 'mp': {'x': 300, 'y': 110}}

def update_stats(hp, mp, hpchange = None, mpchange = None):
    if hpchange:    hp = min(max(hp + hpchange, 0), MAXHP)
    if mpchange:    mp = min(max(mp + mpchange, 0), MAXMP)
    return hp, mp

# === Function to display hp and mp ===
def display_stats(S, hp, mp, Lfont):    
    statsbar = pygame.image.load("Assets/Images/MAIN_Statsbar.png").convert_alpha()
    hpsurf = Lfont.render(str(hp).zfill(6), False, 'Black')
    hprect = pygame.Rect(90, 30, 80, 50)
    mpsurf = Lfont.render(str(mp).zfill(6), False, 'Black')
    mprect = pygame.Rect(90, 105, 80, 50)
    S.blit(statsbar, (13, 13))
    S.blit(hpsurf, hprect)
    S.blit(mpsurf, mprect)

def add_floating_text(text, id, color):
    floating_texts.append({"text": text, "x": floating_texts_pos[id]['x'], "y": floating_texts_pos[id]['y'], "start_time": pygame.time.get_ticks(), "color": color})

def draw_floating_texts(S, floating_font):
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
                    S.blit(outline_surface, (ft["x"] + dx, ft["y"] - offset_y + dy))
    
        S.blit(text_surface, (ft["x"], ft["y"] - offset_y))

    for ft in texts_to_remove:
        floating_texts.remove(ft)