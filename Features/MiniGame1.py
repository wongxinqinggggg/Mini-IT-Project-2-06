import pygame
from random import randint, choice, uniform

class MG1():
    def __init__(self, screen, WIDTH, HEIGHT, mg_state):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.mg_state = mg_state
        mg1_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG1_Base.png").convert(), (self.WIDTH, self.HEIGHT))
        self.screen.blit(mg1_base, (0, 0))

        # Call function for certain mg state
        if self.mg_state == "mainpage": self.mainpage()
        elif self.mg_state == "menu": self.menu()

    def getstate(self):
        return self.mg_state
    
    def eventhandler(self, mouse_X, mouse_Y, dragging = False):
        if self.mg_state == "mainpage":
            if self.startbtnrect.collidepoint(mouse_X, mouse_Y):    self.mg_state = "newgame"
            elif self.instrucbtnrect.collidepoint(mouse_X, mouse_Y):    self.mg_state = "instruc"
            elif self.exitbtnrect.collidepoint(mouse_X, mouse_Y):   self.mg_state = None
        
        elif self.mg_state == "instruc":
            if self.instrucbackrect.collidepoint(mouse_X, mouse_Y): self.mg_state = "mainpage"
        
        elif self.mg_state == "game":
            if self.menubtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = "menu"
            else: self.stains.update(mouse_X, mouse_Y)

        elif self.mg_state == "displaymsg": self.mg_state = "mainpage"

        elif self.mg_state == "menu":
            if self.resumebtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = "resume"
            elif self.restartbtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = "newgame"
            elif self.quitbtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = None

            elif self.audiobtnrect.collidepoint(mouse_X, mouse_Y): 
                # Toggle on and off the audio btn
                if pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                else: 
                    pygame.mixer.music.unpause()
                    # Set volume to .33 if its initially zero
                    if not pygame.mixer.music.get_volume(): pygame.mixer.music.set_volume(0.33)

            elif self.audiosliderrect.collidepoint(mouse_X, mouse_Y):
                dragging = True     # To detect dragging of audio slider
            
            if dragging:
                # Update volume by using position of mouse
                pygame.mixer.music.set_volume(min(max((mouse_X - 335) / (535 - 335), 0), 1))
                if not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
        
        return dragging

    def mainpage(self):
        title = pygame.image.load("Assets/Images/MG1_Title.png").convert_alpha()
        startbtn = pygame.image.load("Assets/Images/MGE_Startbtn.png").convert_alpha()
        self.startbtnrect = startbtn.get_rect(center = (400, 500))
        instrucbtn = pygame.image.load("Assets/Images/MGE_Instrucbtn.png").convert_alpha()
        self.instrucbtnrect = instrucbtn.get_rect(center = (400, 400))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = (750, 50))

        self.screen.blit(title, (0,0))
        self.screen.blit(startbtn, self.startbtnrect)
        self.screen.blit(instrucbtn, self.instrucbtnrect)
        self.screen.blit(exitbtn, self.exitbtnrect)

    def instruc(self, Mfont):
        instruction = ("This game cost 10 Energy to play. "
                       "Click on the dirty area of the plate to clean it. "
                       "Clean a total of 5 plates in 10 seconds to earn 10$.")
        instrucbox = pygame.image.load("Assets/Images/MGE_Instrucbox.png").convert_alpha()
        instrucback = pygame.image.load("Assets/Images/MGE_Instrucback.png").convert_alpha()
        self.instrucbackrect = instrucback.get_rect(center = (400, 450))
        instrucrect = pygame.Rect(100, 180, 650, 400)

        self.screen.blit(instrucbox, (0,0))
        self.screen.blit(instrucback, self.instrucbackrect)
        
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
            self.screen.blit(line_surface, (instrucrect.x + padding, instrucrect.y + padding + i * lineheight))

    def game(self, plates, new_plate, time_left, stains, Lfont):
        self.win = False
        self.stains = stains

        if (time_left >= 10): 
            self.stains.empty()
            self.mg_state, self.win = "end", False
            return None, None
        
        menubtn = pygame.image.load("Assets/Images/MAIN_Menubtn.png").convert_alpha()
        self.menubtnrect = menubtn.get_rect(center = (750, 50))
        plate = pygame.image.load("Assets/Images/MG1_Plate.png").convert_alpha()
        platerect = plate.get_rect(center = (400,300))

        if new_plate:
            # Creating new stains for new plate
            platemask = pygame.mask.from_surface(plate)
            plate_sprite = pygame.sprite.Sprite()
            plate_sprite.image = plate
            plate_sprite.rect = platerect
            plate_sprite.mask = platemask
            for i in range(randint(3, 5)):
                self.stains.add(Stains(plate_sprite, self.stains))
            new_plate = False

        self.screen.blit(plate, platerect)
        self.screen.blit(menubtn, self.menubtnrect)
        self.displayscore(plates, time_left, Lfont)

        if self.stains:
            self.stains.draw(self.screen)
        else:
            plates += 1
            if plates < 5:  new_plate = True
            else: self.mg_state, self.win, plates, new_plate = "win", True, None, None

        return plates, new_plate
            
    def menu(self):
        menu = pygame.image.load("Assets/Images/MENU_Menu.png").convert_alpha()
        resumebtn = pygame.image.load("Assets/Images/MENU_Resumebtn.png").convert_alpha()
        self.resumebtnrect = resumebtn.get_rect(center = (400, 265))
        restartbtn = pygame.image.load("Assets/Images/MENU_Restartbtn.png").convert_alpha()
        self.restartbtnrect = restartbtn.get_rect(center = (400, 365))
        quitbtn = pygame.image.load("Assets/Images/MENU_Quitbtn.png").convert_alpha()
        self.quitbtnrect = quitbtn.get_rect(center = (400, 465))
        audioslider = pygame.image.load("Assets/Images/MENU_Audioslider.png").convert_alpha()

        # Get pos of audio slider based on volume
        self.audiosliderrect = audioslider.get_rect(center = (335  + pygame.mixer.music.get_volume() * (535 - 335), 170))

        # Load audio btn if music playing, load muted btn otherwise
        if pygame.mixer.music.get_busy():
            audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn1.png").convert_alpha()
        else: audiobtn = pygame.image.load("Assets/Images/MENU_Audiobtn2.png").convert_alpha()

        self.audiobtnrect = audiobtn.get_rect(center = (290, 170))
        self.screen.blit(menu, (0,0))
        self.screen.blit(resumebtn, self.resumebtnrect)
        self.screen.blit(restartbtn, self.restartbtnrect)
        self.screen.blit(quitbtn, self.quitbtnrect)
        self.screen.blit(audiobtn, self.audiobtnrect)
        self.screen.blit(audioslider, self.audiosliderrect)

    def checkcond(self):
        return self.stains, self.win

    def displayscore(self, plates, time_left, Lfont):
        # Display no of plates and time left
        plates = 'No:' + str(plates) + "/5"
        scoresurf = Lfont.render(plates, False, 'Black')
        scorerect = pygame.Rect(20, 20, 200, 80)
        time_left = (str(format(time_left, '.2f')) + 's').zfill(6)
        time_leftsurf = Lfont.render(time_left, False, 'Black')
        time_leftrect = pygame.Rect(380, 20, 200, 80)

        pygame.draw.rect(self.screen, 'Dark Green', scorerect)
        pygame.draw.rect(self.screen, 'Dark Green', time_leftrect)
        self.screen.blit(scoresurf, (scorerect.x + 22, scorerect.y + 22))
        self.screen.blit(time_leftsurf, (time_leftrect.x + 22, time_leftrect.y + 22))

    def displaymsg(self, msg, xpos, ypos, Lfont):
        self.msg = msg
        self.xpos = xpos
        self.ypos = ypos
        self.Lfont = Lfont
        box_rect = pygame.Rect(30, 410, 740, 180)
        pygame.draw.rect(self.screen, 'White', box_rect)
        pygame.draw.rect(self.screen, 'Black', box_rect, 3)
        self.screen.blit(self.Lfont.render(self.msg, True, 'Black'), (self.xpos, self.ypos))

class Stains(pygame.sprite.Sprite):
    def __init__(self, plate, stains):
        super().__init__()

        path = choice(["MG1_Stain1", "MG1_Stain2"])
        image = pygame.image.load(f"Assets/Images/{path}.png")

        while True:
            # Randomize stain images
            temp = pygame.sprite.Sprite()
            temp.image = pygame.transform.rotozoom(image, randint(-360, 360), round(uniform(0.6, 1), 2))
            temp.mask = pygame.mask.from_surface(temp.image)
            temp.rect = temp.mask.get_rect(center = (randint(180, 620),randint(180, 580)))

            # Ensure stains images is within the plate and does not overlap with each other
            if pygame.sprite.collide_rect(temp, plate):
                offset = plate.rect[0] - temp.rect[0], plate.rect[1] - temp.rect[1]
                overlap = temp.mask.overlap_area(plate.mask, offset)

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
                        temp.image.set_colorkey((0, 0, 0))
                        self.image, self.rect, self.mask = temp.image, temp.rect, temp.mask
                        break

    def update(self, mouse_X, mouse_Y):
        if self.rect.collidepoint(mouse_X, mouse_Y): self.kill()    # Delete sprite when clicked

    def pallete_swap(self, surf, old_colour, new_colour = (0, 0, 0)):
        # Randomize the colour of stain image
        image = pygame.Surface(surf.get_size())

        if not new_colour:  new_colour = (randint(130, 210), randint(100, 160), randint(5, 65))

        image.fill(new_colour)
        surf.set_colorkey(old_colour)
        image.blit(surf, (0, 0))

        return image
