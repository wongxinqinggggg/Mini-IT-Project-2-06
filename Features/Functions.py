import pygame

MAXHP, MAXMP = 999999, 999999
displaystat = True
floating_texts = [] 
floating_texts_pos = {'hp': {'x': 300, 'y': 40}, 'mp': {'x': 300, 'y': 110},
                      'inventoryE': {'x': 250, 'y': 500}, 'inventoryF': {'x': 350, 'y': 500}}
sprinttime = 0

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

class Notifications():
    def __init__(self, S, vm_buyingprices, vm_income):
        self.S, self.vm_buyingprices, self.vm_income = S, vm_buyingprices, vm_income
        self.displaynoti = [True, True]
        self.counter = 0
        self.anglecounter = 0
        self.alertcenter = [(51, 159), (91, 159)]
        self.angles = [0, 0, 25, -25, 25, -25]
        self.hovering = False

        vm1noti = pygame.image.load("Assets/Images/VM1noti.png").convert_alpha()
        vm1notirect = vm1noti.get_rect(center=(38, 170))
        vm2noti = pygame.image.load("Assets/Images/VM2noti.png").convert_alpha()
        vm2notirect = vm2noti.get_rect(center=(78, 170))
        sprint = pygame.image.load("Assets/Images/Sprintnoti.png").convert_alpha()
        sprintrect = sprint.get_rect(center=(118, 170))
        self.alertbtn = pygame.image.load("Assets/Images/MAIN_Alertbtn.png").convert_alpha()

        self.notis = [{'surf': vm1noti, 'rect': vm1notirect}, 
                      {'surf': vm2noti, 'rect': vm2notirect},
                      {'surf': sprint, 'rect': sprintrect}]
    
    def displayicon(self, mp, vm_level, xsfont):
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
                if vm_level[i] < 3 and mp >= self.vm_buyingprices[i][vm_level[i]]:
                    self.S.blit(notialert, notialert.get_rect(center=(self.alertcenter[i])))
                elif vm_level[i]:
                    pygame.draw.circle(self.S, 'Green', (self.alertcenter[i]), 6)
                    pygame.draw.circle(self.S, 'Black', (self.alertcenter[i]), 6, 1)

        if sprinttime > 0: self.S.blit(self.notis[2]['surf'], self.notis[2]['rect'])
        
        if self.hovering: self.displaytip(vm_level, xsfont)

    def updatetip(self, vm_level, E):
        if E.type == pygame.MOUSEMOTION: 
            for i in range(len(vm_level)):
                if self.displaynoti[i] and (self.notis[i]['rect']).collidepoint(E.pos):
                    self.tippos = E.pos
                    self.hovering = True
                    break
                else: self.hovering = False

            if (self.notis[2]['rect']).collidepoint(E.pos): 
                self.tippos = E.pos
                self.hovering = True

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

        if sprinttime > 0 and (self.notis[2]['rect']).collidepoint(pygame.mouse.get_pos()):
            tipsurf = xsfont.render((f'Sprint ({round(sprinttime)}s)').center(12), False, 'Black') 
            tiprect = pygame.Rect(self.tippos[0] + 10, self.tippos[1] + 10, 100, 17)
            pygame.draw.rect(self.S, 'White', tiprect)
            pygame.draw.rect(self.S, 'Black', tiprect, 2)
            self.S.blit(tipsurf, (tiprect.x + 6, tiprect.y + 5))

class Inventory():
    def __init__(self, S, C):
        self.S, self.C = S, C
        self.maxlist = [1, 3, 9]
        exitbtnpos = (975, 50)
        self.dragging = False
        self.hpchanges = [20, None, 150, 500]
        self.statschange, self.usedcell = {'hp': None, 'mp': None}, None
        self.bagprices = [-500, -2000]
        self.baglvl, self.itemmax, self.surflist, self.rectlist, self.rectcenter = 1, 0, [], [], []
        self.inventories = {'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 
                            'c6': None, 'c7': None, 'c8': None, 'c9': None}
        for key in self.inventories.keys(): self.inventories[key] = {'id': None, 'no': 0, 'locked': False}

        self.baglist = [pygame.image.load("Assets/Images/Bag1.png").convert_alpha(),
                        pygame.image.load("Assets/Images/Bag2.png").convert_alpha(),
                        pygame.image.load("Assets/Images/Bag3.png").convert_alpha()]
        
        self.bag = self.baglist[0]
        self.upgradebtn = pygame.image.load("Assets/Images/MGE_Upgradebtn.png").convert_alpha()
        self.maxbtn = pygame.image.load("Assets/Images/MGE_Maxbtn.png").convert_alpha()
        self.bagbtn, self.btnrect = self.upgradebtn, self.maxbtn.get_rect(center = (185, 480))
        self.exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = self.exitbtn.get_rect(center = exitbtnpos)

        self.itemlist = [pygame.image.load("Assets/Images/STORE_Item1.png").convert_alpha(),
                         pygame.image.load("Assets/Images/STORE_Item2.png").convert_alpha(),
                         pygame.image.load("Assets/Images/STORE_Item3.png").convert_alpha(),
                         pygame.image.load("Assets/Images/STORE_Item4.png").convert_alpha()]
    
        for i in range(len(self.itemlist)):
            surf = self.itemlist[i]
            Wratio, Hratio = surf.get_width()/120, surf.get_height()/120
            if Wratio > 1 or Hratio > 1: ratio = min(1/Wratio, 1/Hratio)
            else: ratio = max(Wratio, Hratio)
            self.itemlist[i] = pygame.transform.scale(surf, (surf.get_width() * ratio, surf.get_height() * ratio))
            
        for i in range(9): self.rectcenter.append(((475 + int(i % 3) * 170, 135 + int(i / 3) * 170)))

    def eventhandler(self, mp, E, inventorypage=True):
        global sprinttime
        if E.type == pygame.MOUSEBUTTONDOWN and inventorypage:
            soundtype = None
            if self.btnrect.collidepoint(E.pos):
                if self.baglvl < 3 and mp >= (-self.bagprices[self.baglvl - 1]):
                    self.statschange['mp'] = self.bagprices[self.baglvl - 1]
                    self.baglvl += 1
                    soundtype = 'transaction'
                else: soundtype = 'btnclicked'
                playsound(soundtype)
            
            if self.exitbtnrect.collidepoint(E.pos):
                soundtype = 'btnclicked'
                playsound(soundtype)
                return 1

            self.dragging = True

        elif E.type == pygame.MOUSEMOTION:
            pass

        elif E.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif E.type == pygame.KEYDOWN:      
            key = 'c' + E.unicode
            if self.inventories.get(key): 
                selectedcell = self.inventories[key]
                if selectedcell['id'] and selectedcell['no']:
                    self.hpchange, self.usedcell = self.hpchanges[selectedcell['id'] - 1], key
                    if selectedcell['id'] == 2: 
                        sprinttime = 10

                else: add_floating_text("Inventory slot empty!", 'inventoryE')

        return
            
    def update(self, hp, mp):
        global sprinttime
        hp, mp = update_stats(hp, mp, self.statschange['hp'], self.statschange['mp'])
        if self.statschange['hp']: add_floating_text(f"+{self.statschange['hp']}", 'hp')
        if self.statschange['mp']: add_floating_text(f"{self.statschange['mp']}", 'mp')
        self.statschange['hp'], self.statschange['mp'] = None, None

        if self.usedcell:
            self.inventories[self.usedcell]['no'] -= 1
            if not self.inventories[self.usedcell]['no'] and not self.inventories[self.usedcell]['locked']:
                self.inventories[self.usedcell]['id'] = None
            self.usedcell = None

        self.itemmax, self.surflist, self.rectlist, i = self.maxlist[self.baglvl - 1], [], [], 0
        for key in self.inventories.keys():
            surf = None
            if self.inventories[key]['id']:
                if self.inventories[key]['no']: surf = self.itemlist[self.inventories[key]['id'] - 1]  
                else: surf = pygame.transform.grayscale(self.itemlist[self.inventories[key]['id'] - 1])

            rect = None if not surf else surf.get_rect(center = self.rectcenter[i])
            self.surflist.append(surf), self.rectlist.append(rect)
            i += 1

        if self.baglvl < 3:
            if mp >= (-self.bagprices[self.baglvl - 1]): self.bagbtn = self.upgradebtn 
            else: self.bagbtn = pygame.transform.grayscale(self.upgradebtn)
        else: self.bagbtn = self.maxbtn

        self.bag = self.baglist[self.baglvl - 1]
        sprinttime = max(0, sprinttime - self.C.get_time()/1000 )
        return hp, mp

    def draw(self, xsfont, font):
        self.S.fill((71, 59, 120))
        self.S.blit(self.bag, (120, 300))
        self.S.blit(self.bagbtn, self.btnrect)
        self.S.blit(self.exitbtn, self.exitbtnrect)

        for i in range(9):
            dx, dy = int(i % 3) * 170, int(i / 3) * 170
            pygame.draw.rect(self.S, 'White', ((400 + dx), (60 + dy), 150, 150), 0, 30)
            pygame.draw.rect(self.S, 'Black', ((400 + dx), (60 + dy), 150, 150), 3, 30)
            pygame.draw.circle(self.S, 'White', ((405 + dx), (202 + dy)), 15)
            pygame.draw.circle(self.S, 'Black', ((405 + dx), (202 + dy)), 15, 1)
            keytext = font.render(f'{i + 1}', False, 'Black')
            self.S.blit(keytext, ((396 + dx), (194 + dy)))

            if self.inventories['c' + str(i + 1)]['id']:
                pygame.draw.circle(self.S, 'Grey', ((543  + dx), (68 + dy)), 15)
                pygame.draw.circle(self.S, 'Black', ((543 + dx), (68 + dy)), 15, 1)
                notext = xsfont.render(f'{self.inventories['c' + str(i + 1)]['no']}/{self.itemmax}', True, 'Black')
                self.S.blit(notext, ((531 + dx), (65 + dy)))

        for i in range(len(self.surflist)):
            if self.surflist[i]: self.S.blit(self.surflist[i], self.rectlist[i])

        draw_floating_texts(self.S)

    def additem(self, item_id):
        cell, cell1, cell2 = None, None, None
        for key in self.inventories.keys():
            if self.inventories[key]['id'] == item_id and self.inventories[key]['no'] < self.itemmax:
                cell1 = key if not cell1 else cell1    # Prioritise the first cell if no locked cell
                if self.inventories[key]['locked']: 
                    cell = key      # Prioritise the locked cell
                    break

            elif not self.inventories[key]['id']: cell2 = key if not cell2 else cell2  # Use empty cell if no available cell
        
        if not cell:
            if cell1: cell = cell1
            else: cell = cell2
        if cell: 
            self.inventories[cell]['id'] = item_id
            self.inventories[cell]['no'] += 1
            return True    
        
        else: 
            add_floating_text("Inventory full!", 'inventoryF')
            return False