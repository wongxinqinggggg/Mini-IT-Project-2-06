import pygame

MAXHP, MAXMP = 999999, 999999
displaystat = True
displaynoti = [True, True]
counter = 0
anglecounter = 0
alertcenter = [(51, 159), (91, 159)]
angles = [0, 0, 25, -25, 25, -25]
floating_texts = [] 
floating_texts_pos = {'hp': {'x': 300, 'y': 40}, 'mp': {'x': 300, 'y': 110}}

def update_stats(hp, mp, hpchange = None, mpchange = None):
    if hpchange:    hp = min(max(hp + hpchange, 0), MAXHP)
    if mpchange:    mp = min(max(mp + mpchange, 0), MAXMP)
    return hp, mp

# === Function to display hp and mp ===
def display_stats(S, hp, mp):    
    Lfont = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 32)
    if not displaystat: return
    statsbar = pygame.image.load("Assets/Images/MAIN_Statsbar.png").convert_alpha()
    hpsurf = Lfont.render(str(hp).zfill(6), False, 'Black')
    hprect = pygame.Rect(90, 30, 80, 50)
    mpsurf = Lfont.render(str(mp).zfill(6), False, 'Black')
    mprect = pygame.Rect(90, 105, 80, 50)
    S.blit(statsbar, (13, 13))
    S.blit(hpsurf, hprect)
    S.blit(mpsurf, mprect)

def display_notifications(S, mp, vm_level, vmbuyingprices):
    global counter, anglecounter
    if not displaystat: return
    elif not displaynoti[0] and not displaynoti[1]: return

    vm1noti = pygame.image.load("Assets/Images/VM1noti.png").convert_alpha()
    vm2noti = pygame.image.load("Assets/Images/VM2noti.png").convert_alpha()
    alertbtn = pygame.image.load("Assets/Images/MAIN_Alertbtn.png").convert_alpha()
    vmnotis = [{'surf': vm1noti, 'rect': vm1noti.get_rect(center=(38, 170))}, 
               {'surf': vm2noti, 'rect': vm2noti.get_rect(center=(78, 170))}]
    counter += 1
    if counter % 30 == 0:
        if anglecounter < (len(angles) - 1): anglecounter += 1
        else:anglecounter = 0
    notialert = pygame.transform.rotate(alertbtn, angles[anglecounter])

    for i in range(len(vm_level)):
        if displaynoti[i]:
            if not vm_level[i]:
                surf = pygame.transform.grayscale(vmnotis[i]['surf'])
            else: surf = vmnotis[i]['surf']

            S.blit(surf, vmnotis[i]['rect'])
            if vm_level[i] < 3 and mp >= vmbuyingprices[i][vm_level[i]]:
                S.blit(notialert, notialert.get_rect(center=(alertcenter[i])))
            elif vm_level[i]:
                pygame.draw.circle(S, 'Green', (alertcenter[i]), 6, 6)
                pygame.draw.circle(S, 'Black', (alertcenter[i]), 6, 1)

def add_floating_text(text, id, color):
    floating_texts.append({"text": text, "x": floating_texts_pos[id]['x'], "y": floating_texts_pos[id]['y'], "start_time": pygame.time.get_ticks(), "color": color})

def draw_floating_texts(S):
    floating_font=pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 26)
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

class Menu():
    def __init__(self, W):
        self.audiobarxpos = [447, 649]
        self.menupage = pygame.image.load("Assets/Images/MENU_Menu.png").convert_alpha()
        self.resumebtn = pygame.image.load("Assets/Images/MENU_Resumebtn.png").convert_alpha()
        self.resumebtnrect = self.resumebtn.get_rect(center = (W/2, 235))
        self.restartbtn = pygame.image.load("Assets/Images/MENU_Restartbtn.png").convert_alpha()
        self.restartbtnrect = self.restartbtn.get_rect(center = (W/2, 335))
        self.quitbtn = pygame.image.load("Assets/Images/MENU_Quitbtn.png").convert_alpha()
        self.quitbtnrect = self.quitbtn.get_rect(center = (W/2, 435))
        self.audioslider = pygame.image.load("Assets/Images/MENU_Audioslider.png").convert_alpha()
        self.audiosliderrect = self.audioslider.get_rect(center = (0, 132))
        self.audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn1.png").convert_alpha()
        self.audiobtnrect = self.audiobtn.get_rect(center = (400, 132))

        self.btnrectlist = [self.resumebtnrect, self.restartbtnrect, self.quitbtnrect, 
                        self.audiobtnrect, self.audiosliderrect]
    
    def eventhandler(self, E, var_dict):
        cursor = False
        restartable = False if var_dict['prev_state'] == "mainpage" else True

        if E.type == pygame.MOUSEBUTTONDOWN:
            if self.resumebtnrect.collidepoint(E.pos): 
                        var_dict['mg_state'] = var_dict['prev_state']
                        var_dict['prev_state'] = None

            elif self.restartbtnrect.collidepoint(E.pos): 
                if not restartable: pass
                else: 
                    var_dict['mg_state'] = "restart"
                    var_dict['prev_state'] = None

            elif self.quitbtnrect.collidepoint(E.pos):
                pygame.mixer.music.unload()
                var_dict['mg_state'] = None

            elif self.audiobtnrect.collidepoint(E.pos): 
                # Toggle on and off the audio btn
                if pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                else: 
                    pygame.mixer.music.unpause()
                    # Set volume to .33 if its initially zero
                    if not pygame.mixer.music.get_volume(): pygame.mixer.music.set_volume(0.33)

            elif self.audiosliderrect.collidepoint(E.pos):
                var_dict['dragging'] = True     # To detect dragging of audio slider

            for rect in self.btnrectlist:
                if rect.collidepoint(E.pos):
                    playsound("btnclicked")
                    cursor = True
                    break

        elif E.type == pygame.MOUSEMOTION:
            if var_dict['dragging']:
                # Update volume by using position of mouse
                pygame.mixer.music.set_volume(min(max((E.pos[0] - self.audiobarxpos[0]) / (self.audiobarxpos[1] - self.audiobarxpos[0]), 0), 1))
                if not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()

            for rect in self.btnrectlist:
                if rect.collidepoint(E.pos):
                    if rect == self.restartbtnrect and not restartable: 
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                    else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    cursor = True
                    break

        return var_dict, cursor

    def update(self):
        # Get pos of audio slider based on volume
        audiosliderxpos = self.audiobarxpos[0] + pygame.mixer.music.get_volume() * (self.audiobarxpos[1] - self.audiobarxpos[0])
        self.audiosliderrect.center = (audiosliderxpos, 132)

        # Load audio btn if music playing, load muted btn otherwise
        if pygame.mixer.music.get_busy(): self.audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn1.png").convert_alpha()
        else: self.audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn2.png").convert_alpha()

    def draw(self, S):
        S.blit(self.menupage, (0,0))
        S.blit(self.resumebtn, self.resumebtnrect)
        S.blit(self.restartbtn, self.restartbtnrect)
        S.blit(self.quitbtn, self.quitbtnrect)
        S.blit(self.audiobtn, self.audiobtnrect)
        S.blit(self.audioslider, self.audiosliderrect)

def playsound(soundtype):
    btnclicked = pygame.mixer.Sound("Assets/Audio/button_click.mp3")
    success = pygame.mixer.Sound("Assets/Audio/success.mp3")
    fail = pygame.mixer.Sound("Assets/Audio/fail.mp3")
    transaction = pygame.mixer.Sound("Assets/Audio/Cashier-Ka-Ching (u_byub5wd934).mp3")

    if soundtype == "btnclicked":
        btnclicked.play()
    elif soundtype == "success":
        success.play(maxtime=2500)
    elif soundtype == "fail":
        fail.play()
    elif soundtype == "transaction":
        transaction.play(fade_ms=800)