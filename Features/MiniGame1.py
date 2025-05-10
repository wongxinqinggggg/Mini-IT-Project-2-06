import pygame
from random import randint, choice, uniform

STATS = {'hp': 10, 'mp': 10}
time_limit, plate_requirement = 10, 5
msg = [["YOU LOSE!", 380], ["YOU WIN!", 400], ["INSUFFICIENT ENERGY!", 190]]
audiobarxpos = [447, 649]
menubtnpos = (975, 50)

class MG1():
    def __init__(self, S, W, H, var_dict, E=None, C=None):
        global statschange
        self.var_dict, statschange = var_dict, {'hpc': None, 'mpc': None}

        if E: self.eventhandler(E, self.var_dict['mg_state'])
        self.update()
        if not E: self.draw(S, W, H, self.var_dict['mg_state'], C)
        self.update()

    def eventhandler(self, E, mg_state):
        global countdown
        if E.type == pygame.MOUSEBUTTONDOWN:
            if mg_state == "mainpage":
                if self.var_dict['msg']: self.var_dict['msg'] = None
                elif self.exitbtnrect.collidepoint(E.pos): self.var_dict['mg_state'] = None
                elif self.instrucbtnrect.collidepoint(E.pos): self.var_dict['mg_state'] = "instruc"
                elif self.startbtnrect.collidepoint(E.pos): 
                    if self.var_dict['hp'] >= STATS['hp']:
                        statschange['hpc'] = (-STATS['hp'])
                        self.var_dict['mg_state'] = "countdown"
                        self.var_dict['new_plate'] = True
                        self.var_dict['time_passed'] = 0
                        countdown = 4

                    else: self.var_dict['msg'] = msg[2]

            elif mg_state == "instruc":
                if self.instrucbackrect.collidepoint(E.pos): self.var_dict['mg_state'] = "mainpage"
        
            elif mg_state == "game": 
                if self.menubtnrect.collidepoint(E.pos): 
                    self.var_dict['mg_state'] = "menu"
                    self.var_dict['time_passed'] = self.time_passed

                else: self.stains.update(E.pos)

            elif self.var_dict['mg_state'] == "displaymsg": self.var_dict['mg_state'] = "mainpage"

            elif self.var_dict['mg_state'] == "menu":
                if self.resumebtnrect.collidepoint(E.pos): 
                    self.var_dict['mg_state'] = "game"

                elif self.restartbtnrect.collidepoint(E.pos): 
                    self.var_dict['mg_state'] = "countdown"
                    self.var_dict['new_plate'] = True
                    self.var_dict['time_passed'] = 0
                    countdown = 4

                elif self.quitbtnrect.collidepoint(E.pos): self.var_dict['mg_state'] = None

                elif self.audiobtnrect.collidepoint(E.pos): 
                    # Toggle on and off the audio btn
                    if pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                    else: 
                        pygame.mixer.music.unpause()
                        # Set volume to .33 if its initially zero
                        if not pygame.mixer.music.get_volume(): pygame.mixer.music.set_volume(0.33)

                elif self.audiosliderrect.collidepoint(E.pos):
                    self.var_dict['dragging'] = True     # To detect dragging of audio slider
 
        elif E.type == pygame.MOUSEMOTION:
            if self.var_dict['dragging']:
                # Update volume by using position of mouse
                pygame.mixer.music.set_volume(min(max((E.pos[0] - audiobarxpos[0]) / (audiobarxpos[1] - audiobarxpos[0]), 0), 1))
                if not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()

        elif E.type == pygame.MOUSEBUTTONUP:
            self.var_dict['dragging'] = False

    def update(self):
        self.var_dict['hpc'], self.var_dict['mpc'] = statschange['hpc'], statschange['mpc']

    def draw(self, S, W, H, mg_state, C):
        base = pygame.transform.scale(pygame.image.load("Assets/Images/MG1_Base.png").convert(), (W, H))
        S.blit(base, (0, 0))

        if mg_state == "mainpage": 
            self.mainpage(S, W, H, self.var_dict['Lfont'])
            pygame.mouse.set_cursor()
        elif mg_state == "instruc": 
            self.instruc(S, W, H, self.var_dict['Mfont'])
            pygame.mouse.set_cursor()
        elif mg_state == "game": 
            self.game(S, W, H, self.var_dict['plates'], self.var_dict['new_plate'], self.var_dict['Lfont'], C)
            sponge = pygame.image.load("Assets/Images/MG1_Sponge.png").convert_alpha()
            pygame.mouse.set_cursor((50, 50), sponge)
        elif mg_state == "menu": 
            self.menu(S, W, H)
            pygame.mouse.set_cursor()
        elif mg_state == "countdown": 
            self.countdown(S, W, H, C, self.var_dict['Lfont'])
            pygame.mouse.set_cursor()

    def mainpage(self, S, W, H, Lfont):
        title = pygame.image.load("Assets/Images/MG1_Title.png").convert_alpha()
        startbtn = pygame.image.load("Assets/Images/MGE_Startbtn.png").convert_alpha()
        self.startbtnrect = startbtn.get_rect(center = (W/2, 490))
        instrucbtn = pygame.image.load("Assets/Images/MGE_Instrucbtn.png").convert_alpha()
        self.instrucbtnrect = instrucbtn.get_rect(center = (W/2, 390))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = menubtnpos)

        S.blit(title, title.get_rect(center = (W/2, 240)))
        S.blit(startbtn, self.startbtnrect)
        S.blit(instrucbtn, self.instrucbtnrect)
        S.blit(exitbtn, self.exitbtnrect)

        if self.var_dict['msg']: self.displaymsg(S, W, H, self.var_dict['msg'][0], self.var_dict['msg'][1], Lfont)

    def instruc(self, S, W, H, Mfont):
        instruction = ("This game cost 10 Energy to play. "
                       "Click on the dirty area of the plate to clean it. "
                       "Clean a total of 5 plates in 10 seconds to earn 10$.")
        instrucbox = pygame.image.load("Assets/Images/MGE_Instrucbox.png").convert_alpha()
        instrucback = pygame.image.load("Assets/Images/MGE_Instrucback.png").convert_alpha()
        self.instrucbackrect = instrucback.get_rect(center = (W/2, 450))
        instrucrect = pygame.Rect(200, 180, 710, 400)

        S.blit(instrucbox, instrucbox.get_rect(center = (W/2, H/2)))
        S.blit(instrucback, self.instrucbackrect)
        
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

    def game(self, S, H, W, plates, new_plate, Lfont, C):
        self.stains, self.time_passed = self.var_dict['stains'], self.var_dict['time_passed']
        self.time_passed += C.get_time()/1000
        
        if self.time_passed >= time_limit: 
            self.var_dict['mg_state'], self.var_dict['msg'] = "mainpage", msg[0]
            self.var_dict['stains'], self.var_dict['plates'] = None, 0
            return
        
        menubtn = pygame.image.load("Assets/Images/MAIN_Menubtn.png").convert_alpha()
        self.menubtnrect = menubtn.get_rect(center = menubtnpos)
        plate = pygame.image.load("Assets/Images/MG1_Plate.png").convert_alpha()
        platerect = plate.get_rect(center = (W/2 + 100, H/2))
        horiplate = pygame.image.load("Assets/Images/MG1_Horiplate.png").convert_alpha()
        horiplatestack = pygame.Surface((225, 500), pygame.SRCALPHA)

        for i in range(plate_requirement - plates - 1):
            horiplatestack.blit(horiplate, horiplate.get_rect(bottomleft = (0, 500 - i * 25)))

        if new_plate:
            # Creating new stains for new plate
            self.stains = pygame.sprite.Group()
            platemask = pygame.mask.from_surface(plate)
            for i in range(randint(3, 5)): self.stains.add(Stains(platerect, platemask, self.stains))
            new_plate = False

        S.blit(plate, platerect)
        S.blit(menubtn, self.menubtnrect)
        S.blit(horiplatestack, horiplatestack.get_rect(bottomleft = (20, 550)))
        self.displayscore(S, plates, (time_limit - self.time_passed), Lfont)

        if self.stains: self.stains.draw(S)
        else:
            plates += 1
            if plates < plate_requirement:  new_plate = True
            else: 
                self.var_dict['msg'], statschange['mpc'] = msg[1], STATS['mp']
                self.var_dict['stains'], self.var_dict['plates'] = None, 0
                self.var_dict['mg_state'] = "mainpage"
                return
            
        self.var_dict ['stains'] = self.stains
        self.var_dict ['plates'] = plates
        self.var_dict ['new_plate'] = new_plate
        self.var_dict ['time_passed'] = self.time_passed

    def menu(self, S, W, H):
        menu = pygame.image.load("Assets/Images/MENU_Menu.png").convert_alpha()
        resumebtn = pygame.image.load("Assets/Images/MENU_Resumebtn.png").convert_alpha()
        self.resumebtnrect = resumebtn.get_rect(center = (W/2, 235))
        restartbtn = pygame.image.load("Assets/Images/MENU_Restartbtn.png").convert_alpha()
        self.restartbtnrect = restartbtn.get_rect(center = (W/2, 335))
        quitbtn = pygame.image.load("Assets/Images/MENU_Quitbtn.png").convert_alpha()
        self.quitbtnrect = quitbtn.get_rect(center = (W/2, 435))
        audioslider = pygame.image.load("Assets/Images/MENU_Audioslider.png").convert_alpha()

        # Get pos of audio slider based on volume
        audiosliderxpos = audiobarxpos[0] + pygame.mixer.music.get_volume() * (audiobarxpos[1] - audiobarxpos[0])
        self.audiosliderrect = audioslider.get_rect(center = (audiosliderxpos, 132))

        # Load audio btn if music playing, load muted btn otherwise
        if pygame.mixer.music.get_busy(): audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn1.png").convert_alpha()
        else: audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn2.png").convert_alpha()
        self.audiobtnrect = audiobtn.get_rect(center = (400, 132))
        
        S.blit(menu, (0,0))
        S.blit(resumebtn, self.resumebtnrect)
        S.blit(restartbtn, self.restartbtnrect)
        S.blit(quitbtn, self.quitbtnrect)
        S.blit(audiobtn, self.audiobtnrect)
        S.blit(audioslider, self.audiosliderrect)

    def displayscore(self, S, plates, time_left, Lfont):
        # Display no of plates and time left
        time_left = (str(format(time_left, '.2f')) + 's').zfill(6)
        time_leftsurf = Lfont.render(time_left, False, 'Black')
        time_leftrect = pygame.Rect(20, 20, 230, 80)
        plates = 'No:' + str(plates) + "/5"
        platessurf = Lfont.render(plates, False, 'Black')
        platesrect = pygame.Rect(20, 140, 230, 80)

        pygame.draw.rect(S, 'Dark Green', platesrect)
        pygame.draw.rect(S, 'Dark Green', time_leftrect)
        S.blit(platessurf, (platesrect.x + 22, platesrect.y + 22))
        S.blit(time_leftsurf, (time_leftrect.x + 22, time_leftrect.y + 22))

    def displaymsg(self, S, W, H, msg, xpos, Lfont, ypos = 480):
        box_rect = pygame.Rect(30, 40, W-60, 180)
        pygame.draw.rect(S, 'White', box_rect)
        pygame.draw.rect(S, 'Black', box_rect, 3)
        S.blit(self.Lfont.render(self.msg, True, 'Black'), (xpos, ypos))

    def countdown(self, S, W, H, C, Lfont):
        global countdown
        countdownbox = pygame.Rect(0, 200, W, 200)
        pygame.draw.rect(S, (255, 0, 0, 0), countdownbox, 200)
        if countdown >= 1 :
            S.blit(Lfont.render(str(int(countdown)), True, 'Black'), (W/2, H/2))
            countdown -= C.get_time()/1000
            return
        elif countdown >= 0:
            S.blit(Lfont.render('START!', True, 'Black'), (W/2 - 70, H/2))
            countdown -= C.get_time()/1000
            return
        else: self.var_dict['mg_state'] = "game"

class Stains(pygame.sprite.Sprite):
    def __init__(self, platerect, platemask, stains):
        super().__init__()

        path = choice(["MG1_Stain1", "MG1_Stain2"])
        image = pygame.image.load(f"Assets/Images/{path}.png")

        while True:
            # Randomize stain images
            temp = pygame.sprite.Sprite()
            temp.image = pygame.transform.rotozoom(image, randint(-360, 360), round(uniform(1, 1,4), 2))
            temp.mask = pygame.mask.from_surface(temp.image)
            temp.rect = temp.mask.get_rect(center = (randint(350, 850),randint(50, 550)))

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
