import pygame

MAXHP, MAXMP = 999999, 999999
displaystat = True
floating_texts = [] 
floating_texts_pos = {'hp': {'x': 300, 'y': 40}, 'mp': {'x': 300, 'y': 110},
                      'inventoryE': {'x': 250, 'y': 500}, 'inventoryF': {'x': 350, 'y': 500}}
sprinttime = 0

def initialize_stats(hp=520, mp=520):
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
        text_surface = floating_font.render(ft["text"], False, ft["color"])
        text_surface.set_alpha(alpha)

        # Create an outline by drawing black text slightly shifted
        outline_color = (30, 30, 30)  
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    outline_surface = floating_font.render(ft["text"], True, outline_color)
                    outline_surface.set_alpha(alpha)
                    S.blit(outline_surface, (ft["x"] + dx, ft["y"] - offset_y + dy))
    
        S.blit(text_surface, (ft["x"], ft["y"] - offset_y))

    for ft in texts_to_remove:
        floating_texts.remove(ft)

def get_sprite(sprite_width, sprite_height, spritesheet, trim=False):
    surflist = []
    for i in range(int(spritesheet.get_height()/sprite_height)):
        for j in range(int(spritesheet.get_width()/sprite_width)):
            surf = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA).convert_alpha()
            surf.blit(spritesheet, (0,0), (j*sprite_width, i*sprite_height, sprite_width, sprite_height))
            if trim:
                rect = surf.get_bounding_rect()
                surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA).convert_alpha()
                surface.blit(spritesheet, (0,0), (j*sprite_width, i*sprite_height, sprite_width, sprite_height))
                surflist.append(surface)
            else: 
                surflist.append(surf)
            if trim:
                rect = surf.get_bounding_rect()
                surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA).convert_alpha()
                surface.blit(spritesheet, (0,0), (j*sprite_width, i*sprite_height, sprite_width, sprite_height))
                surflist.append(surface)
            else: 
                surflist.append(surf)
    return surflist

def load_sprite():
    global iconlist, mainbtnlist, menubtnlist, tbtnlist, itemlist
    global iconlist, mainbtnlist, menubtnlist, tbtnlist, itemlist
    iconsheet = pygame.image.load("Assets/Images/Iconsheet.png").convert_alpha()
    abtnsheet = pygame.image.load("Assets/Images/Mainbtnsheet.png").convert_alpha()
    ebtnsheet = pygame.image.load("Assets/Images/Menubtnsheet.png").convert_alpha()
    tbtnsheet = pygame.image.load("Assets/Images/Transactionbtnsheet.png").convert_alpha()
    itemsheet = pygame.image.load("Assets/Images/Itemsheet.png").convert_alpha()
    itemsheet = pygame.image.load("Assets/Images/Itemsheet.png").convert_alpha()

    iconlist = get_sprite(30, 30, iconsheet)
    mainbtnlist = get_sprite(80, 80, abtnsheet)
    menubtnlist = get_sprite(271, 81, ebtnsheet)
    tbtnlist = get_sprite(76, 34, tbtnsheet)
    itemlist = get_sprite(208, 175, itemsheet, True)
    itemlist = get_sprite(208, 175, itemsheet, True)

def playsound(soundtype):
    if not pygame.mixer.music.get_busy(): return
    volume, channel = pygame.mixer.music.get_volume(), None
    if soundtype == "btnclicked": 
        channel = pygame.mixer.Sound("Assets/Audio/button_click.mp3").play()
    elif soundtype == "success": 
        channel = pygame.mixer.Sound("Assets/Audio/success.mp3").play(maxtime=2500)
    elif soundtype == "fail":  
        channel = pygame.mixer.Sound("Assets/Audio/fail.mp3").play()
    elif soundtype == "transaction": 
        channel = pygame.mixer.Sound("Assets/Audio/Cashier-Ka-Ching (u_byub5wd934).mp3").play(fade_ms=800)
    elif soundtype == "eating": 
        channel = pygame.mixer.Sound("Assets/Audio/Eating-Effect (u_scysdwddsp).mp3").play(maxtime=1200)
    elif soundtype == "coin":
        channel = pygame.mixer.Sound("Assets/Audio/coinmusic.mp3").play()

    if channel: channel.set_volume(volume)

def play_music(path):
    playing = pygame.mixer.music.get_busy()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(f"Assets/Audio/{path}.mp3")
    pygame.mixer.music.play(-1)
    if not playing: pygame.mixer.music.pause()

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
        self.audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn.png").convert_alpha()
        self.audiobtnrect = self.audiobtn.get_rect(center = (400, 132))

        self.btnrectlist = [self.resumebtnrect, self.restartbtnrect, self.quitbtnrect, 
                            self.audiobtnrect, self.audiosliderrect]
    
    def eventhandler(self, E, var_dict):
        cursor = False
        restartable = True if var_dict['prev_state'] == "game" else False

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

        # Pause audio if volume = 0
        if not pygame.mixer.music.get_volume(): pygame.mixer.music.pause()

        # Load audio btn if music playing, load muted btn otherwise
        if pygame.mixer.music.get_busy(): self.muted = False
        else: self.muted = True

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
        self.displaynoti = [True, True, False, False]
        self.counter = 0
        self.anglecounter = 0
        self.iconcenter = [(38, 170), (78, 170), (118, 170), (158, 170)]
        self.alertcenter = [(51, 159), (91, 159), (131, 159)]
        self.angles = [0, 0, 25, -25, 25, -25]
        self.hovering = False

        petnoti, vm1noti, vm2noti, sprint = iconlist[3], iconlist[4], iconlist[5], iconlist[2]
        self.alertbtn = pygame.image.load("Assets/Images/MAIN_Alertbtn.png").convert_alpha()

        self.notis = [{'surf': vm1noti, 'rect': vm1noti.get_rect()}, 
                      {'surf': vm2noti, 'rect': vm2noti.get_rect()},
                      {'surf': petnoti, 'rect': petnoti.get_rect()},
                      {'surf': sprint, 'rect': sprint.get_rect()}]
    
    def displayicon(self, vm_level, pet_npc, xsfont, is_night):
        if not displaystat: return
        elif not self.displaynoti.count(True): return

        self.displaynoti[2] = True if pet_npc.owned else False
        self.displaynoti[3] = True if sprinttime > 0 else False
        self.counter += 1
        if self.counter % 30 == 0:
            if self.anglecounter < (len(self.angles) - 1): self.anglecounter += 1
            else:self.anglecounter = 0
        notialert = pygame.transform.rotate(self.alertbtn, self.angles[self.anglecounter])

        for i in range(len(self.displaynoti)):
            alert, indicate, surf = False, False, None
            if self.displaynoti[i]:
                num = self.displaynoti[:i].count(True)
                if i in [0, 1]:
                    if not vm_level[i]:
                        surf = pygame.transform.grayscale(self.notis[i]['surf'])
                    elif vm_level[i] < 3 and money >= self.vm_buyingprices[i][vm_level[i]]: 
                        alert = True
                    elif vm_level[i]: 
                        indicate = True
                        color = 'Grey' if is_night else 'Green'

                else:
                    if i == 2:
                        percentage = pet_npc.pet_hp/pet_npc.MAXHP
                        if percentage <= pet_npc.hp_percentage['hungry']: 
                            alert = True
                            if not percentage: surf = pygame.transform.grayscale(self.notis[i]['surf'])
                        else: 
                            color = 'Green' if (percentage >= pet_npc.hp_percentage['happy']) else 'Grey'
                            indicate = True

                if not surf: surf = self.notis[i]['surf']
                self.notis[i]['rect'].center = self.iconcenter[num]
                self.S.blit(surf, self.notis[i]['rect'])
                if alert: self.S.blit(notialert, notialert.get_rect(center=(self.alertcenter[num])))
                elif indicate:
                    pygame.draw.circle(self.S, color, (self.alertcenter[num]), 6)
                    pygame.draw.circle(self.S, 'Black', (self.alertcenter[num]), 6, 1)
        
        if self.hovering: self.displaytip(vm_level, pet_npc, xsfont, is_night)

    def updatetip(self, E):
        if E.type == pygame.MOUSEMOTION: 
            for i in range(len(self.displaynoti)):
                if self.displaynoti[i] and (self.notis[i]['rect']).collidepoint(E.pos):
                    self.tippos = E.pos
                    self.hovering = True
                    break
                else: self.hovering = False

    def displaytip(self, vm_level, pet_npc, xsfont, is_night):
        for i in range(len(self.displaynoti)):
            if self.displaynoti[i] and (self.notis[i]['rect']).collidepoint(pygame.mouse.get_pos()):
                if i in [0, 1]:
                    if not vm_level[i]: 
                        lvltxt, incometxt = '', '(Not Owned)'
                    else:
                        lvltxt = f'(Lv{vm_level[i]})' if vm_level[i] <= 2 else '(Maxed)'
                        if is_night: incometxt = 'Shop Closed'
                        else: incometxt = f'income:{self.vm_income[i][vm_level[i]-1]}$/s'

                    tipsurfs = [xsfont.render((f'VM{i + 1} ' + lvltxt).center(12), False, 'Black'), 
                                xsfont.render(incometxt, False, 'Black')]
                    tipboxheight = 30

                elif i == 2:
                    tipsurfs = [xsfont.render((f'{pet_npc.pet_name}').center(12), False, 'Black'), 
                                xsfont.render((f'HP: {pet_npc.pet_hp}/{pet_npc.MAXHP}').center(12), False, 'Black')]
                    tipboxheight = 30

                elif i == 3:
                    tipsurfs = [xsfont.render((f'Sprint ({round(sprinttime)}s)').center(12), False, 'Black')]
                    tipboxheight = 17

                tiprect = pygame.Rect(self.tippos[0] + 10, self.tippos[1] + 10, 100, tipboxheight)
                pygame.draw.rect(self.S, 'White', tiprect)
                pygame.draw.rect(self.S, 'Black', tiprect, 2)
                for j in range(len(tipsurfs)):
                    self.S.blit(tipsurfs[j], (tiprect.x + 6, tiprect.y + 5 + j * 12))
                break

class Inventory():
    def __init__(self, S, C):
        self.S, self.C = S, C
        self.maxlist = [1, 3, 9]
        exitbtnpos = (975, 50)
        self.dragging, self.selecteditem = False, None
        self.effects = [{'effect': 'hp', 'value': 20}, {'effect': 'sprint', 'value': 10}, 
                        {'effect': 'hp', 'value': 150}, {'effect': 'hp', 'value': 500}, 
                        {'effect': 'pethp', 'value': 80}, {'effect': 'pethp', 'value': 200}]
        self.statschange, self.usedcell = {'hpc': None, 'mpc': None, 'pethpc': None}, None
        self.bagprices = [-500, -2000]
        self.pricepos = [(150, 510), (130, 510)]
        self.baglvl, self.itemmax = 1, 0
        self.inventories = {'c1': {}, 'c2': {}, 'c3': {}, 'c4': {}, 'c5': {}, 
                            'c6': {}, 'c7': {}, 'c8': {}, 'c9': {}}
        self.keys = list(self.inventories.keys())
        self.load_inventories()
        
        bagsheet = pygame.image.load("Assets/Images/Bagsheet.png").convert_alpha()
        self.baglist = get_sprite(136, 136, bagsheet)
        self.bag = self.baglist[0]
        self.lock = pygame.image.load("Assets/Images/Inventory_lock.png").convert_alpha()
        self.lockrect = self.lock.get_rect()
        self.upgradebtn, self.maxbtn = tbtnlist[1], tbtnlist[3]
        self.bagbtn, self.btnrect = self.upgradebtn, self.upgradebtn.get_rect(center = (185, 480))
        self.exitbtn = mainbtnlist[2]
        self.exitbtnrect = self.exitbtn.get_rect(center = exitbtnpos)


        self.itemsurflist = itemlist.copy()
            
        for i in range(len(self.itemsurflist)):
            surf = self.itemsurflist[i]
            Wratio, Hratio = surf.get_width()/120, surf.get_height()/120
            if Wratio >= 1 or Hratio >= 1: ratio = min(1/Wratio, 1/Hratio)
            else: ratio = max(Wratio, Hratio)
            self.itemsurflist[i] = pygame.transform.scale(surf, (surf.get_width() * ratio, surf.get_height() * ratio)) 

        self.btnrectlist = [self.btnrect, self.exitbtnrect]           

    def eventhandler(self, E, pet_npc=None, inventorypage=True):
        global sprinttime
        cursor = False
        if E.type == pygame.MOUSEBUTTONDOWN and inventorypage:
            soundtype = None
            if self.btnrect.collidepoint(E.pos):
                if self.baglvl < 3 and money >= (-self.bagprices[self.baglvl - 1]):
                    self.statschange['mpc'] = self.bagprices[self.baglvl - 1]
                    self.baglvl += 1
                    soundtype = 'transaction'
                else: soundtype = 'btnclicked'
                playsound(soundtype)
                return
            
            elif self.exitbtnrect.collidepoint(E.pos):
                soundtype = 'btnclicked'
                playsound(soundtype)
                return 1
            
            for i in range(len(self.keys)):
                key = self.keys[i]
                if self.inventories[key]['lockrect'].collidepoint(E.pos):
                    self.inventories[key]['locked'] = not self.inventories[key]['locked']
                    break

                elif (self.inventories[key]['rect'] and 
                      self.inventories[key]['rect'].collidepoint(E.pos) and
                      not self.inventories[key]['locked']):
                    self.selecteditem = key
                    self.cursorsurf = self.inventories[key]['surf']
                    self.cursorcenter = (self.cursorsurf.get_width()//2, self.cursorsurf.get_height()//2)
                    self.dragging = True
                    break

        elif E.type == pygame.MOUSEMOTION and inventorypage:
            if not self.dragging:
                for rect in self.btnrectlist:
                    if rect.collidepoint(E.pos):
                        cursor = pygame.SYSTEM_CURSOR_HAND
                        break
                for key in self.keys:
                    if self.inventories[key]['lockrect'].collidepoint(E.pos):
                        cursor = pygame.SYSTEM_CURSOR_HAND
                        break
                    elif self.inventories[key]['rect'] and self.inventories[key]['rect'].collidepoint(E.pos):
                        if self.inventories[key]['locked']: cursor = pygame.SYSTEM_CURSOR_NO
                        else: cursor = pygame.SYSTEM_CURSOR_HAND
                        break

        elif E.type == pygame.MOUSEBUTTONUP and inventorypage:
            if self.dragging:
                for i in range(len(self.keys)):
                    key = self.keys[i]
                    if self.inventories[key]['cellrect'].collidepoint(E.pos):
                        if self.inventories[key]['id'] == self.inventories[self.selecteditem]['id']:
                            if self.inventories[key]['no'] < self.itemmax:
                                maxno = self.itemmax - self.inventories[key]['no']
                                no = min(self.inventories[self.selecteditem]['no'], maxno)
                                self.inventories[self.selecteditem]['no'] -= no
                                self.inventories[key]['no'] += no

                        elif not self.inventories[key]['locked']:
                            temp = self.inventories[self.selecteditem]
                            id, no = temp['id'], temp['no']
                            self.inventories[self.selecteditem]['id'] = self.inventories[key]['id']
                            self.inventories[self.selecteditem]['no'] = self.inventories[key]['no']
                            self.inventories[key]['id'] = id
                            self.inventories[key]['no'] = no
                        break
                self.dragging = False

        elif E.type == pygame.KEYDOWN:      
            key = 'c' + E.unicode
            if self.inventories.get(key): 
                selectedcell = self.inventories[key]
                if selectedcell['id'] and selectedcell['no']:
                    if effect == 'pethp' and not pet_npc.owned:
                        add_floating_text("Item unusable!", 'inventoryF')
                        return
                    playsound('eating')
                    self.usedcell =  key
                    effect = self.effects[selectedcell['id'] - 1]['effect']
                    value = self.effects[selectedcell['id'] - 1]['value']

                    if effect == 'hp': self.statschange['hpc'] = value
                    elif effect == 'sprint': sprinttime = value
                    elif effect == 'pethp': self.statschange['pethpc'] = value

                else: add_floating_text("Inventory slot empty!", 'inventoryE')

        if not self.dragging: 
            if cursor: pygame.mouse.set_cursor(cursor)
            else: pygame.mouse.set_cursor()
        else: pygame.mouse.set_cursor(self.cursorcenter, self.cursorsurf)
            
    def update(self, pet_npc):
        global sprinttime
        update_stats(self.statschange['hpc'], self.statschange['mpc'])
        if self.statschange['hpc']: add_floating_text(f"+{self.statschange['hpc']}", 'hp')
        elif self.statschange['mpc']: add_floating_text(f"{self.statschange['mpc']}", 'mp')
        elif self.statschange['pethpc']: pet_npc.pet_hp  = min(pet_npc.pet_hp+self.statschange['pethpc'], pet_npc.MAXHP)
        for key in self.statschange.keys(): self.statschange[key] = None

        if self.usedcell:
            self.inventories[self.usedcell]['no'] -= 1
            if not self.inventories[self.usedcell]['no'] and not self.inventories[self.usedcell]['locked']:
                self.inventories[self.usedcell]['id'] = None
            self.usedcell = None

        self.itemmax = self.maxlist[self.baglvl - 1]
        for key in self.keys:
            if not self.inventories[key]['no'] and not self.inventories[key]['locked']: 
                self.inventories[key]['id'] = None
                surf = None
            if self.inventories[key]['id']:
                if self.inventories[key]['no']: surf = self.itemsurflist[self.inventories[key]['id'] - 1]  
                else: surf = pygame.transform.grayscale(self.itemsurflist[self.inventories[key]['id'] - 1])
            else: surf = None

            rect = None if not surf else surf.get_rect(center = self.inventories[key]['center'])
            self.inventories[key]['surf'], self.inventories[key]['rect'] = surf, rect

        if self.baglvl < 3:
            if money >= (-self.bagprices[self.baglvl - 1]): self.bagbtn = self.upgradebtn 
            else: self.bagbtn = pygame.transform.grayscale(self.upgradebtn)
        else: self.bagbtn = self.maxbtn

        self.bag = self.baglist[self.baglvl - 1]
        if sprinttime: sprinttime = max(0, sprinttime - self.C.get_time()/1000 )

    def draw(self, xsfont, font):
        self.S.fill((71, 59, 120))
        self.S.blit(self.bag, (120, 300))
        self.S.blit(self.bagbtn, self.btnrect)
        self.S.blit(self.exitbtn, self.exitbtnrect)

        if self.baglvl <= 2:
            pricetxt = font.render(f'{-self.bagprices[self.baglvl-1]}$', False, 'Black')
            self.S.blit(pricetxt, self.pricepos[self.baglvl-1])

        for i in range(len(self.keys)):
            key = self.keys[i]
            cell = self.inventories[key]
            dx, dy = int(i % 3) * 170, int(i / 3) * 170
            pygame.draw.rect(self.S, 'White', ((400 + dx), (60 + dy), 150, 150), 0, 30)
            pygame.draw.rect(self.S, 'Black', ((400 + dx), (60 + dy), 150, 150), 3, 30)
            pygame.draw.circle(self.S, 'White', ((405 + dx), (202 + dy)), 15)
            pygame.draw.circle(self.S, 'Black', ((405 + dx), (202 + dy)), 15, 1)
            keytext = font.render(f'{i + 1}', False, 'Black')
            self.S.blit(keytext, ((396 + dx), (194 + dy)))

            if cell['id']:
                pygame.draw.circle(self.S, 'Grey', ((543  + dx), (68 + dy)), 15)
                pygame.draw.circle(self.S, 'Black', ((543 + dx), (68 + dy)), 15, 1)
                notext = xsfont.render(f'{cell["no"]}/{self.itemmax}', True, 'Black')
                self.S.blit(notext, ((531 + dx), (65 + dy)))
                pygame.draw.circle(self.S, 'White', (cell['lockrect'].center), 15)
                pygame.draw.circle(self.S, 'Black', (cell['lockrect'].center), 15, 1)

                if cell['locked']: 
                    self.lockrect.center = cell['lockrect'].center
                    self.S.blit(self.lock, self.lockrect)

                self.S.blit(self.inventories[key]['surf'], self.inventories[key]['rect'])

        draw_floating_texts(self.S)

    def additem(self, item_id):
        cell, cell1, cell2 = None, None, None
        for key in self.keys:
            if self.inventories[key]['id'] == item_id and self.inventories[key]['no'] < self.itemmax:
                cell1 = key if not cell1 else cell1    # Prioritise the first cell if no locked cell
                if self.inventories[key]['locked']: 
                    cell = key      # Prioritise the locked cell
                    break

            elif not self.inventories[key]['id']: 
                cell2 = key if not cell2 else cell2  # Use empty cell if no available cell
        
        if not cell: cell = cell1 if cell1 else cell2
        if cell: 
            self.inventories[cell]['id'] = item_id
            self.inventories[cell]['no'] += 1
            return True    
        
        else: 
            add_floating_text("Inventory full!", 'inventoryF')
            return False
        
    def load_inventories(self, data=None):
        for i in range(len(self.keys)):
            key = self.keys[i]
            if data: self.inventories[key].update(data[key])
            else: self.inventories[key].update({'id': None, 'no': 0, 'locked': False})

            dx, dy = int(i % 3) * 170, int(i / 3) * 170
            center = ((475 + dx, 135 + dy))
            cell = pygame.rect.Rect((400 + dx), (60 + dy), 150, 150)
            lockrect = pygame.rect.Rect((528  + dx), (187 + dy), 30, 30)
            self.inventories[key].update({'surf': None, 'rect': None, 'center': center, 
                                          'cellrect': cell, 'lockrect': lockrect})
