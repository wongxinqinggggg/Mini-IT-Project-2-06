import pygame

MAXHP, MAXMP = 999999, 999999
displaystat = True
floating_texts = [] 
floating_texts_pos = {'hp': {'x': 300, 'y': 40}, 'mp': {'x': 300, 'y': 110}}

def initialize_stats(hp=9999, mp=9999):
    global energy, money, statsbar
    energy, money = hp, mp
    statsbar = pygame.image.load("Assets/Images/MAIN_Statsbar.png").convert_alpha()

def update_stats(hpchange = None, mpchange = None):
    global energy, money
    if hpchange: energy = min(max(energy + hpchange, 0), MAXHP)
    if mpchange: money = min(max(money + mpchange, 0), MAXMP)

# === Function to display energy and money ===
def display_stats(S):    
    Lfont = pygame.font.Font("Assets/Fonts/PressStart2P.ttf", 32)
    if not displaystat: return
    hpsurf = Lfont.render(str(energy).zfill(6), False, 'Black')
    hprect = pygame.Rect(90, 30, 80, 50)
    mpsurf = Lfont.render(str(money).zfill(6), False, 'Black')
    mprect = pygame.Rect(90, 105, 80, 50)
    S.blit(statsbar, (13, 13))
    S.blit(hpsurf, hprect)
    S.blit(mpsurf, mprect)

def add_floating_text(text, id, color=(128,128,128)):
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

def get_sprite(sprite_width, sprite_height, spritesheet):
    surflist = []
    for i in range(int(spritesheet.get_height()/sprite_height)):
        for j in range(int(spritesheet.get_width()/sprite_width)):
            surf = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA).convert_alpha()
            surf.blit(spritesheet, (0,0), (j*sprite_width, i*sprite_height, sprite_width, sprite_height))
            surflist.append(surf)
    return surflist

def load_sprite():
    global iconlist, mainbtnlist, menubtnlist, tbtnlist
    iconsheet = pygame.image.load("Assets/Images/Iconsheet.png").convert_alpha()
    abtnsheet = pygame.image.load("Assets/Images/Mainbtnsheet.png").convert_alpha()
    ebtnsheet = pygame.image.load("Assets/Images/Menubtnsheet.png").convert_alpha()
    tbtnsheet = pygame.image.load("Assets/Images/Transactionbtnsheet.png").convert_alpha()

    iconlist = get_sprite(30, 30, iconsheet)
    mainbtnlist = get_sprite(80, 80, abtnsheet)
    menubtnlist = get_sprite(271, 81, ebtnsheet)
    tbtnlist = get_sprite(76, 34, tbtnsheet)

def playsound(soundtype):
    if soundtype == "btnclicked":
        pygame.mixer.Sound("Assets/Audio/button_click.mp3").play()
    elif soundtype == "success":
        pygame.mixer.Sound("Assets/Audio/success.mp3").play(maxtime=2500)
    elif soundtype == "fail":
        pygame.mixer.Sound("Assets/Audio/fail.mp3").play()
    elif soundtype == "transaction":
        pygame.mixer.Sound("Assets/Audio/Cashier-Ka-Ching (u_byub5wd934).mp3").play(fade_ms=800)

class Menu():
    def __init__(self, W):
        self.muted = False
        self.audiobarxpos = [447, 649]
        self.menubtncenter = [(W/2, 235), (W/2, 335), (W/2, 435)]
        self.resumebtn, self.restartbtn, self.quitbtn = menubtnlist[0], menubtnlist[1], menubtnlist[2]
        self.resumebtnrect = self.resumebtn.get_rect(center = (W/2, 235))
        self.restartbtnrect = self.restartbtn.get_rect(center = (W/2, 335))
        self.quitbtnrect = self.quitbtn.get_rect(center = (W/2, 435))
        self.audiosliderrect = pygame.rect.Rect(0, 0, 20, 20)
        self.audiosliderrect.center = (0, 132)
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
        if pygame.mixer.music.get_busy(): self.audiobtn = self.muted = False
        else: self.audiobtn = self.muted = True

    def draw(self, S):
        pygame.draw.rect(S, (100, 100, 120), (339, 82, 344, 412))
        pygame.draw.rect(S, 'Black', (339, 82, 344, 412), 1)
        S.blit(self.resumebtn, self.resumebtnrect)
        S.blit(self.restartbtn, self.restartbtnrect)
        S.blit(self.quitbtn, self.quitbtnrect)
        S.blit(self.audiobtn, self.audiobtnrect)
        if self.muted: pygame.draw.line(S, 'Black', self.audiobtnrect.topleft, self.audiobtnrect.bottomright, 2)
        pygame.draw.line(S, 'Black', (self.audiobarxpos[0], 130), (self.audiobarxpos[1], 130), 4)
        pygame.draw.circle(S, 'Black', self.audiosliderrect.center, 10)

class Notifications():
    def __init__(self, S, vm_buyingprices, vm_income):
        self.S, self.vm_buyingprices, self.vm_income = S, vm_buyingprices, vm_income
        self.displaynoti = [True, True]
        self.counter = 0
        self.anglecounter = 0
        self.alertcenter = [(51, 159), (91, 159)]
        self.angles = [0, 0, 25, -25, 25, -25]
        self.hovering = False

        vm1noti, vm2noti = iconlist[4], iconlist[5]
        vm1notirect = vm1noti.get_rect(center=(38, 170))
        vm2notirect = vm2noti.get_rect(center=(78, 170))
        self.alertbtn = pygame.image.load("Assets/Images/MAIN_Alertbtn.png").convert_alpha()

        self.notis = [{'surf': vm1noti, 'rect': vm1notirect}, 
                      {'surf': vm2noti, 'rect': vm2notirect}]
    
    def displayicon(self, vm_level, xsfont):
        if not displaystat: return
        elif not self.displaynoti[0] and not self.displaynoti[1]: return

        self.counter += 1
        if self.counter % 30 == 0:
            if self.anglecounter < (len(self.angles) - 1): self.anglecounter += 1
            else:self.anglecounter = 0
        notialert = pygame.transform.rotate(self.alertbtn, self.angles[self.anglecounter])

        for i in range(len(vm_level)):
            if self.displaynoti[i]:
                if not vm_level[i]:
                    surf = pygame.transform.grayscale(self.notis[i]['surf'])
                else: surf = self.notis[i]['surf']

                self.S.blit(surf, self.notis[i]['rect'])
                if vm_level[i] < 3 and money >= self.vm_buyingprices[i][vm_level[i]]:
                    self.S.blit(notialert, notialert.get_rect(center=(self.alertcenter[i])))
                elif vm_level[i]:
                    pygame.draw.circle(self.S, 'Green', (self.alertcenter[i]), 6)
                    pygame.draw.circle(self.S, 'Black', (self.alertcenter[i]), 6, 1)
        
        if self.hovering: self.displaytip(vm_level, xsfont)

    def updatetip(self, vm_level, E):
        if E.type == pygame.MOUSEMOTION: 
            for i in range(len(vm_level)):
                if self.displaynoti[i] and (self.notis[i]['rect']).collidepoint(E.pos):
                    self.tippos = E.pos
                    self.hovering = True
                    break
                else: self.hovering = False

    def displaytip(self, vm_level, xsfont):
        for i in range(len(vm_level)):
            if self.displaynoti[i] and (self.notis[i]['rect']).collidepoint(pygame.mouse.get_pos()):
                if not vm_level[i]: 
                    lvltxt, incometxt = '', '(Not Owned)'
                else:
                    lvltxt = f'(Lv{vm_level[i]})' if vm_level[i] <= 2 else '(Maxed)'
                    incometxt = f'income:{self.vm_income[i][vm_level[i]-1]}$/s'

                tipsurfs = [xsfont.render((f'VM{i + 1} ' + lvltxt).center(12), False, 'Black'), 
                           xsfont.render(incometxt, False, 'Black')]
                tiprect = pygame.Rect(self.tippos[0] + 10, self.tippos[1] + 10, 100, 30)
                pygame.draw.rect(self.S, 'White', tiprect)
                pygame.draw.rect(self.S, 'Black', tiprect, 2)
                for i in range(len(tipsurfs)):
                    self.S.blit(tipsurfs[i], (tiprect.x + 6, tiprect.y + 5 + i * 12))
