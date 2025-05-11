import pygame
from random import randint, choice, uniform

class MG1():
    def __init__(self, W, H):
        self.W, self.H = W, H 
        self.STATS = {'hp': 10, 'mp': 10}
        self.time_limit, self.plate_requirement = 20, 10
        self.msg = [["YOU LOSE!", 380], ["YOU WIN!", 400], ["INSUFFICIENT ENERGY!", 190]]
        menubtnpos = (975, 50)
        self.audiobarxpos = [447, 649]
        self.statschange = {'hpc': None, 'mpc': None}

        self.btnsound = pygame.mixer.Sound("Assets/Audio/button_click.mp3")
        self.successsound = pygame.mixer.Sound("Assets/Audio/success.mp3")
        self.failsound = pygame.mixer.Sound("Assets/Audio/fail.mp3")
        pygame.mixer.music.load("Assets/Audio/Puzzle-Game (Cyberwave-Orchestra).mp3")
        pygame.mixer.music.play(-1)

        self.base = pygame.transform.scale(pygame.image.load("Assets/Images/MG1_Base.png").convert(), (W, H))
        self.title = pygame.image.load("Assets/Images/MG1_Title.png").convert_alpha()
        self.startbtn = pygame.image.load("Assets/Images/MGE_Startbtn.png").convert_alpha()
        self.startbtnrect = self.startbtn.get_rect(center = (W/2, 490))
        self.instrucbtn = pygame.image.load("Assets/Images/MGE_Instrucbtn.png").convert_alpha()
        self.instrucbtnrect = self.instrucbtn.get_rect(center = (W/2, 390))
        self.instrucback = pygame.image.load("Assets/Images/MGE_Instrucback.png").convert_alpha()
        self.instrucbackrect = self.instrucback.get_rect(center = (W/2, 450))
        self.menubtn = pygame.image.load("Assets/Images/MAIN_Menubtn.png").convert_alpha()
        self.menubtnrect = self.menubtn.get_rect(center = menubtnpos)
        self.menupage = pygame.image.load("Assets/Images/MENU_Menu.png").convert_alpha()
        self.resumebtn = pygame.image.load("Assets/Images/MENU_Resumebtn.png").convert_alpha()
        self.resumebtnrect = self.resumebtn.get_rect(center = (W/2, 235))
        self.restartbtn = pygame.image.load("Assets/Images/MENU_Restartbtn.png").convert_alpha()
        self.restartbtnrect = self.restartbtn.get_rect(center = (W/2, 335))
        self.quitbtn = pygame.image.load("Assets/Images/MENU_Quitbtn.png").convert_alpha()
        self.quitbtnrect = self.quitbtn.get_rect(center = (W/2, 435))
        self.audioslider = pygame.image.load("Assets/Images/MENU_Audioslider.png").convert_alpha()
        self.audiosliderrect = self.audioslider.get_rect(center = (0, 132))
        audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn1.png").convert_alpha()
        self.audiobtnrect = audiobtn.get_rect(center = (400, 132))
        self.plate = pygame.image.load("Assets/Images/plate10x.png").convert_alpha()
        self.platerect = self.plate.get_rect(center = (W/2 + 100, H/2))
        self.horiplate = pygame.image.load("Assets/Images/horiplate5x.png").convert_alpha()
        self.spongecursor = pygame.image.load("Assets/Images/MG1_Sponge.png").convert_alpha()

        self.btnrectlist = {'mainpage': [self.startbtnrect, self.instrucbtnrect, self.menubtnrect], 
                            'instruc': [self.instrucbackrect], 'game': [self.menubtnrect], 'countdown': None,
                            'menu': [self.resumebtnrect, self.restartbtnrect, self.quitbtnrect, self.audiobtnrect, self.audiosliderrect]}

    def eventhandler(self, E, var_dict):
        self.var_dict = var_dict
        mg_state = self.var_dict['mg_state']

        if E.type == pygame.MOUSEBUTTONDOWN:
            if mg_state == "mainpage":
                if self.var_dict['msg']: self.var_dict['msg'] = None

                elif self.instrucbtnrect.collidepoint(E.pos): self.var_dict['mg_state'] = "instruc"

                elif self.menubtnrect.collidepoint(E.pos):
                    self.var_dict['prev_state'] = self.var_dict['mg_state'] 
                    self.var_dict['mg_state'] = "menu"

                elif self.startbtnrect.collidepoint(E.pos): 
                    self.newgame(self.var_dict['hp'])

            elif mg_state == "instruc":
                if self.instrucbackrect.collidepoint(E.pos): self.var_dict['mg_state'] = "mainpage"
        
            elif mg_state == "game": 
                if self.menubtnrect.collidepoint(E.pos): 
                    self.var_dict['prev_state'] = self.var_dict['mg_state'] 
                    self.var_dict['mg_state'] = "menu"
                    self.var_dict['time_passed'] = self.time_passed

                else: self.stains.update(E.pos)

            elif self.var_dict['mg_state'] == "displaymsg": self.var_dict['mg_state'] = "mainpage"

            elif self.var_dict['mg_state'] == "menu":
                if self.resumebtnrect.collidepoint(E.pos): 
                        self.var_dict['mg_state'] = self.var_dict['prev_state']
                        self.var_dict['prev_state'] = None

                elif self.restartbtnrect.collidepoint(E.pos): self.newgame(self.var_dict['hp'])

                elif self.quitbtnrect.collidepoint(E.pos):
                    pygame.mixer.music.unload()
                    self.var_dict['mg_state'] = None

                elif self.audiobtnrect.collidepoint(E.pos): 
                    # Toggle on and off the audio btn
                    if pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                    else: 
                        pygame.mixer.music.unpause()
                        # Set volume to .33 if its initially zero
                        if not pygame.mixer.music.get_volume(): pygame.mixer.music.set_volume(0.33)

                elif self.audiosliderrect.collidepoint(E.pos):
                    self.var_dict['dragging'] = True     # To detect dragging of audio slider
        
            if self.var_dict['btnrectlist']:
                for rect in self.var_dict['btnrectlist']:
                    if rect.collidepoint(E.pos):
                        self.btnsound.play()

        elif E.type == pygame.MOUSEMOTION:
            global cursorcollide
            cursorcollide = False

            if self.var_dict['mg_state'] == "game": 
                pygame.mouse.set_cursor((50, 50), self.spongecursor)
                cursorcollide = True

            if self.var_dict['btnrectlist']:
                for rect in self.var_dict['btnrectlist']:
                    if rect.collidepoint(E.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        cursorcollide = True
                        break

            if self.var_dict['dragging']:
                # Update volume by using position of mouse
                pygame.mixer.music.set_volume(min(max((E.pos[0] - self.audiobarxpos[0]) / (self.audiobarxpos[1] - self.audiobarxpos[0]), 0), 1))
                if not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()

            if not cursorcollide: 
                pygame.mouse.set_cursor()

        elif E.type == pygame.MOUSEBUTTONUP:
            self.var_dict['dragging'] = False

    def update(self, mg_state, C, var_dict):
        self.var_dict = var_dict
        self.var_dict['hp'], self.var_dict['mp'] = self.statschange['hpc'], self.statschange['mpc']
        self.statschange['hpc'], self.statschange['mpc'] = None, None

        if mg_state == "game":
            self.stains, self.time_passed = self.var_dict['stains'], self.var_dict['time_passed']
            self.time_passed += C.get_time()/1000

            if self.time_passed >= self.time_limit:
                self.var_dict['mg_state'], self.var_dict['msg'] = "mainpage", self.msg[0]
                self.var_dict['stains'], self.var_dict['plates'] = None, 0
                self.failsound.play()
                pygame.mixer.music.load("Assets/Audio/Puzzle-Game (Cyberwave-Orchestra).mp3")
                pygame.mixer.music.play(-1)
                return

            self.horiplatestack = pygame.Surface((225, 500), pygame.SRCALPHA)
            for i in range(self.plate_requirement - self.var_dict['plates'] - 1):
                self.horiplatestack.blit(self.horiplate, self.horiplate.get_rect(bottomleft = (0, 500 - i * 25)))

            if self.var_dict['new_plate']:
                # Creating new stains for new plate
                self.stains = pygame.sprite.Group()
                platemask = pygame.mask.from_surface(self.plate)
                for i in range(randint(3, 5)): self.stains.add(Stains(self.platerect, platemask, self.stains))
                self.var_dict['new_plate'] = False

            if not self.stains:
                self.var_dict['plates'] += 1
                if self.var_dict['plates'] < self.plate_requirement:  self.var_dict['new_plate'] = True
                else: 
                    self.var_dict['msg'], self.statschange['mpc'] = self.msg[1], self.STATS['mp']
                    self.var_dict['stains'], self.var_dict['plates'] = None, 0
                    self.var_dict['mg_state'] = "mainpage"
                    self.successsound.play(maxtime=2500)
                    pygame.mixer.music.load("Assets/Audio/Puzzle-Game (Cyberwave-Orchestra).mp3")
                    pygame.mixer.music.play(-1)
                    return

            self.var_dict['stains'], self.var_dict['time_passed'] = self.stains, self.time_passed

        if mg_state: 
            self.var_dict['btnrectlist'] = self.btnrectlist[f'{mg_state}']

            if mg_state == "mainpage" or (mg_state == "countdown" and self.statschangetimer >= 0):
                self.var_dict['displaystats'] = True
            else: self.var_dict['displaystats'] = False

    def draw(self, S, W, H, mg_state, C, var_dict):
        self.var_dict = var_dict
        S.blit(self.base, (0, 0))

        if mg_state == "mainpage": 
            self.mainpage(S, W, self.var_dict['Lfont'])
        elif mg_state == "instruc": 
            self.instruc(S, W, H, self.var_dict['Mfont'])
        elif mg_state == "game": 
            self.game(S, self.var_dict['plates'], self.var_dict['Lfont'])
        elif mg_state == "menu": 
            self.menu(S)
        elif mg_state == "countdown":
            self.countdown(S, W, H, C, self.var_dict['XLfont']) 

    def mainpage(self, S, W, Lfont):
        S.blit(self.title, self.title.get_rect(center = (W/2, 240)))
        S.blit(self.startbtn, self.startbtnrect)
        S.blit(self.instrucbtn, self.instrucbtnrect)
        S.blit(self.menubtn, self.menubtnrect)
        if self.var_dict['msg']: self.displaymsg(S, W, self.var_dict['msg'][0], self.var_dict['msg'][1], Lfont)

    def instruc(self, S, W, H, Mfont):
        instruction = (f"This game cost {self.STATS['hp']} Energy to play. "
                       "Click on the dirty area of the plate to clean it. "
                       f"Clean a total of {self.plate_requirement} plates " 
                       f"in {self.time_limit} seconds to earn {self.STATS['mp']}$.")
        instrucbox = pygame.image.load("Assets/Images/MGE_Instrucbox.png").convert_alpha()
        instrucrect = pygame.Rect(200, 180, 710, 400)

        S.blit(instrucbox, instrucbox.get_rect(center = (W/2, H/2)))
        S.blit(self.instrucback, self.instrucbackrect)
        
        words = instruction.split(' ')
        lines, line = [], ''
        padding, lineheight = 5, 30

        # Render wrapped text
        for word in words:
            if Mfont.size(line + word + ' ')[0] < instrucrect.width - 2 * padding:  line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)

        # Display insturction msg
        for i, l in enumerate(lines):
            line_surface = Mfont.render(l.strip(), True, 'Black')
            S.blit(line_surface, (instrucrect.x + padding, instrucrect.y + padding + i * lineheight))

    def game(self, S, plates, Lfont):
        S.blit(self.plate, self.platerect)
        S.blit(self.menubtn, self.menubtnrect)
        S.blit(self.horiplatestack, self.horiplatestack.get_rect(bottomleft = (20, 550)))
        self.displayscore(S, plates, (self.time_limit - self.var_dict['time_passed']), Lfont)
        self.var_dict['stains'].draw(S)

    def menu(self, S):
        # Get pos of audio slider based on volume
        audiosliderxpos = self.audiobarxpos[0] + pygame.mixer.music.get_volume() * (self.audiobarxpos[1] - self.audiobarxpos[0])
        self.audiosliderrect.center = (audiosliderxpos, 132)

        # Load audio btn if music playing, load muted btn otherwise
        if pygame.mixer.music.get_busy(): audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn1.png").convert_alpha()
        else: audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn2.png").convert_alpha()

        S.blit(self.menupage, (0,0))
        S.blit(self.resumebtn, self.resumebtnrect)
        S.blit(self.restartbtn, self.restartbtnrect)
        S.blit(self.quitbtn, self.quitbtnrect)
        S.blit(audiobtn, self.audiobtnrect)
        S.blit(self.audioslider, self.audiosliderrect)

    def displayscore(self, S, plates, time_left, Lfont):
        # Display no of self.var_dict['plates'] and time left
        time_left = (str(format(time_left, '.2f')) + 's').zfill(6)
        time_leftsurf = Lfont.render(time_left, False, 'Black')
        time_leftect = pygame.Rect(20, 20, 260, 80)
        plates = 'No:' + str(plates) + f"/{self.plate_requirement}"
        platessurf = Lfont.render(plates, False, 'Black')
        platesrect = pygame.Rect(20, 120, 260, 80)
        pygame.draw.rect(S, 'Dark Green', time_leftect)
        pygame.draw.rect(S, 'Dark Green', platesrect)
        S.blit(time_leftsurf, (time_leftect.x + 40, time_leftect.y + 22))
        S.blit(platessurf, (platesrect.x + 22, platesrect.y + 22))

    def displaymsg(self, S, W, msg, xpos, Lfont, ypos = 480):
        box_rect = pygame.Rect(30, 400, W-60, 180)
        pygame.draw.rect(S, 'White', box_rect)
        pygame.draw.rect(S, 'Black', box_rect, 3)
        S.blit(Lfont.render(msg, True, 'Black'), (xpos, ypos))
    
    def newgame(self, hp):
        if hp < self.STATS['hp']:
            self.var_dict['msg'] = self.msg[2]
            self.var_dict['mg_state'] = "mainpage"
            return
        
        pygame.mixer.music.load("Assets/Audio/Arcade-Beat (NoCopyrightSound633).mp3")
        pygame.mixer.music.play(-1)
        self.statschange['hpc'] = (-self.STATS['hp'])
        self.var_dict['mg_state'] = "countdown"
        self.var_dict['new_plate'] = True
        self.var_dict['time_passed'] = 0
        self.var_dict['plates'] = 0
        self.var_dict['stains'] = pygame.sprite.Group()
        self.countdowntimer = 4
        self.statschangetimer = 2
        self.fadealpha = 0

    def countdown(self, S, W, H, C, XLfont):
        if self.statschangetimer >= 0:
            self.mainpage(S, W, XLfont)
            self.statschangetimer -= C.get_time()/1000
            return
        else: self.var_dict['fade'] = None

        if self.countdowntimer >= 0:
            countdownbox = pygame.Rect(0, 200, W, 200)
            pygame.draw.rect(S, (255, 0, 0, 0), countdownbox, 200)
            if self.countdowntimer >= 1 : S.blit(XLfont.render(str(int(self.countdowntimer)), True, 'Black'), (W/2, H/2))
            else: S.blit(XLfont.render('START!', True, 'Black'), (W/2 - 80, H/2))
            self.countdowntimer -= C.get_time()/1000
            return
        
        else:
            self.var_dict['mg_state'] = "game"
            self.update(self.var_dict['mg_state'], C, self.var_dict)

class Stains(pygame.sprite.Sprite):
    def __init__(self, platerect, platemask, stains):
        super().__init__()

        path = choice(["MG1_Stain1", "MG1_Stain2"])
        image = pygame.image.load(f"Assets/Images/{path}.png")

        while True:
            # Randomize stain images
            temp = pygame.sprite.Sprite()
            temp.image = pygame.transform.rotozoom(image, randint(-360, 360), round(uniform(1, 1.4), 2))
            temp.mask = pygame.mask.from_surface(temp.image)
            temp.rect = temp.mask.get_rect(center = (randint(350, 850), randint(50, 550)))

            # Ensure stains images is within the plate and does not overlap with each other
            offset = platerect[0] - temp.rect[0], platerect[1] - temp.rect[1]
            overlap = temp.mask.overlap_area(platemask, offset)
            if temp.mask.count() == overlap:
                sprite_list = pygame.sprite.spritecollide(temp, stains.sprites(), False)
                if sprite_list:
                    for sprite in sprite_list:
                        offset = sprite.rect[0] - temp.rect[0], sprite.rect[1] - temp.rect[1]
                        if temp.mask.overlap(sprite.mask, offset):
                            temp = None
                            break
                
                if temp:
                    temp.image = self.pallete_swap(temp.image, (0, 0, 0, 0))
                    temp.image = self.pallete_swap(temp.image, (170, 117 ,34), None)
                    temp.image.set_colorkey((1, 1, 1))
                    self.image, self.rect, self.mask = temp.image, temp.rect, temp.mask
                    break

    def update(self, pos):
        if self.rect.collidepoint(pos): self.kill()    # Delete sprite when clicked

    def pallete_swap(self, surf, old_colour, new_colour = (1, 1, 1)):
        # Randomize the colour of stain image
        image = pygame.Surface(surf.get_size())
        if not new_colour:  new_colour = (randint(130, 210), randint(100, 160), randint(5, 65))
        image.fill(new_colour)
        surf.set_colorkey(old_colour)
        image.blit(surf, (0, 0))
        return image
