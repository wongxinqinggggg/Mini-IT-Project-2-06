import pygame
import time
from random import randint

class PlayMG1():
    def __init__(self, screen, WIDTH, HEIGHT, mg_state):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.mg_state = mg_state
        mg1_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG1_Base.png").convert(), (self.WIDTH, self.HEIGHT))
        self.screen.blit(mg1_base, (0, 0))

    def getstate(self):
        return self.mg_state
    
    def eventhandler(self, mouse_X, mouse_Y):
        if self.mg_state == "mainpage":
            if self.startbtnrect.collidepoint(mouse_X, mouse_Y):    self.mg_state = "newgame"
            elif self.instrucbtnrect.collidepoint(mouse_X, mouse_Y):    self.mg_state = "instruc"
            elif self.exitbtnrect.collidepoint(mouse_X, mouse_Y):   self.mg_state = None
        
        elif self.mg_state == "instruc":
            if self.instrucbackrect.collidepoint(mouse_X, mouse_Y): self.mg_state = "mainpage"
        
        elif self.mg_state == "game":
            for stain, stainrect in self.stains.items():
                if stainrect.collidepoint(mouse_X, mouse_Y):
                    del self.stains[stain]
                    return
        elif self.mg_state == "end": self.mg_state = "mainpage"

    def mainpage(self, hp, mp, Lfont):
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
        self.displaystats(hp, mp, Lfont)

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
        
        # Display insturction msg
        words = instruction.split(' ')
        lines, line = [], ''
        padding, lineheight = 5, 30

        for word in words:
            if Mfont.size(line + word + ' ')[0] < instrucrect.width - 2 * padding:  line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)

        for i, l in enumerate(lines):
            line_surface = Mfont.render(l.strip(), True, 'Black')
            self.screen.blit(line_surface, (instrucrect.x + padding, instrucrect.y + padding + i * lineheight))

    def game(self, plates, new_plate, start_time, stains, font):
        timer = time.time() - start_time
        self.win = False
        self.stains = stains

        if (timer >= 10): 
            self.mg_state = "end"
            return None, None, None
        
        plate = pygame.image.load("Assets/Images/MG1_Plate.png").convert_alpha()
        platerect = plate.get_rect(center = (400,300))
        platemask = pygame.mask.from_surface(plate)
        stain1 = pygame.image.load("Assets/Images/MG1_Stain1.png").convert_alpha()
        stain1mask = pygame.mask.from_surface(stain1)
        stain2 = pygame.image.load("Assets/Images/MG1_Stain2.png").convert_alpha()
        stain2mask = pygame.mask.from_surface(stain2)

        if new_plate:
            while True:
                stain1rect = stain1.get_rect(center = (randint(200, 600), randint(180, 570)))
                stain2rect = stain2.get_rect(center = (randint(200, 600), randint(180, 570)))

                offset1 = platerect[0] - stain1rect[0], platerect[1] - stain1rect[1]
                offset2 = platerect[0] - stain2rect[0], platerect[1] - stain2rect[1]
                offset = stain1rect[0] - stain2rect[0], stain1rect[1] - stain2rect[1]
                overlap1 = stain1mask.overlap_area(platemask, offset1)
                overlap2 = stain2mask.overlap_area(platemask, offset2)
                overlap = stain1mask.overlap(stain2mask, offset)
                
                if (stain1mask.count() == overlap1 
                    and stain2mask.count() == overlap2 
                    and not overlap):
                    break

            self.stains.update({stain1: stain1rect})
            self.stains.update({stain2: stain2rect})
            new_plate = False

        self.screen.blit(plate, platerect)
        self.displayscore(plates, timer, font)

        if self.stains:
            for stain, stainrect in self.stains.items():
                    self.screen.blit(stain, stainrect)
        else:
            plates += 1
            if plates < 5:  new_plate = True
            else: self.mg_state, self.win = "win", True

        return plates, new_plate, start_time
            
    def checkcond(self):
        return self.stains, self.win

    def displayscore(self, plates, timer, Lfont):
        plates = 'No: ' + str(plates)
        scoresurf = Lfont.render(plates, False, 'Black')
        scorerect = pygame.Rect(20, 20, 200, 80)

        timeleft = str(round(10 - timer, 2)) + 's'
        timesurf = Lfont.render(timeleft, False, 'Black')
        timerect = pygame.Rect(580, 20, 200, 80)

        pygame.draw.rect(self.screen, 'Dark Green', scorerect)
        pygame.draw.rect(self.screen, 'Dark Green', timerect)

        self.screen.blit(scoresurf, (scorerect.x + 22, scorerect.y + 22))
        self.screen.blit(timesurf, (timerect.x + 22, timerect.y + 22))

    def end(self, win, hp, mp, Lfont):
        self.win = win
        if self.win:
            endmsg = "YOU WIN!"
        else:
            endmsg = "YOU LOSE"

        box_rect = pygame.Rect(30, 410, 740, 180)
        pygame.draw.rect(self.screen, 'White', box_rect)
        pygame.draw.rect(self.screen, 'Black', box_rect, 3)
        self.screen.blit(Lfont.render(endmsg, True, 'Black'), (280, 480))
        self.displaystats(hp, mp, Lfont)

    def displaystats(self, hp, mp, Lfont):
        statsbar = pygame.image.load("Assets/Images/MGE_Statsbar.png").convert_alpha()
        hp = (4 - len(hp)) * ' ' + hp
        mp = (4 - len(mp)) * ' ' + mp

        hpsurf = Lfont.render(hp, False, 'Black')
        hprect = pygame.Rect(95, 30, 100, 50)
        mpsurf = Lfont.render(mp, False, 'Black')
        mprect = pygame.Rect(95, 105, 100, 50)

        self.screen.blit(statsbar, (0,0))
        self.screen.blit(hpsurf, hprect)
        self.screen.blit(mpsurf, mprect)
