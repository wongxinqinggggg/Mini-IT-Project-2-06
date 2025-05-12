import pygame
from Features import Functions

class STORE():
    def __init__(self, W, H):
        global statschange 
        self.menu = Functions.Menu(W)
        self.hplist = [20, 65, 150, 500]
        self.pricelist = [10, 25, 50, 120]
        self.btnpos = [(465, 190), (755, 190), (475, 400), (750, 395)]
        itemcenter = [(350, 245), (630, 245), (320, 446), (620, 470)]
        menubtnpos = (975, 50)
        statschange = {'hpc': None, 'mpc': None}

        pygame.mixer.music.load("Assets/Audio/Retro-Game-Music (moodmode).mp3")
        pygame.mixer.music.play(-1)

        self.base = pygame.transform.scale(pygame.image.load("Assets/Images/STORE_base.png").convert(), (W, H))
        self.mainbase = pygame.image.load("Assets/Images/STORE_Mainbase.png").convert_alpha()
        self.menubtn = pygame.image.load("Assets/Images/MAIN_Menubtn.png").convert_alpha()
        self.menubtnrect = self.menubtn.get_rect(center = menubtnpos)
        item1 = pygame.image.load("Assets/Images/STORE_Item1.png").convert_alpha()
        item1rect = item1.get_rect(center = itemcenter[0])
        item2 = pygame.image.load("Assets/Images/STORE_Item2.png").convert_alpha()
        item2rect = item2.get_rect(center = itemcenter[1])
        item3 = pygame.image.load("Assets/Images/STORE_Item3.png").convert_alpha()
        item3rect = item3.get_rect(center = itemcenter[2])
        item4 = pygame.image.load("Assets/Images/STORE_Item4.png").convert_alpha()
        item4rect = item4.get_rect(center = itemcenter[3])
        self.itemsurflist = [item1, item2, item3, item4]
        self.itemlist = [[item1, item1rect], [item2, item2rect], 
                         [item3, item3rect], [item4, item4rect]]
        self.btnrectdict = {'mainpage': [self.menubtnrect]}

    def eventhandler(self, mg_state, E):
        if E.type == pygame.MOUSEBUTTONDOWN:
            cursorclicked = False
            if mg_state == "mainpage":
                if self.menubtnrect.collidepoint(E.pos): 
                    self.var_dict['prev_state'] = self.var_dict['mg_state']
                    self.var_dict['mg_state'] = "menu"

                else: self.buttons.update(E)

            elif mg_state == "menu":
                self.var_dict, cursorclicked = self.menu.eventhandler(E, self.var_dict)

            if self.btnrectdict.get(mg_state): 
                for rect in self.btnrectdict[mg_state]:
                    if rect.collidepoint(E.pos) or cursorclicked:
                        Functions.playsound("btnclicked")
                        break

        elif E.type == pygame.MOUSEMOTION:
            global cursorcollide
            cursorcollide = False

            if mg_state == "menu":
                self.var_dict, cursorcollide = self.menu.eventhandler(E, self.var_dict)

            if self.btnrectdict.get(mg_state): 
                for rect in self.btnrectdict[mg_state]:
                    if rect.collidepoint(E.pos):
                        cursorcollide = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break
                
                if mg_state == "mainpage": self.buttons.update(E, True)

            if not cursorcollide: pygame.mouse.set_cursor()

        elif E.type == pygame.MOUSEBUTTONUP: self.var_dict['dragging'] = False

    def update(self, mg_state, var_dict):
        global statschange
        self.var_dict = var_dict
        self.var_dict['hp'], self.var_dict['mp'] = Functions.update_stats(self.var_dict['hp'], self.var_dict['mp'], statschange['hpc'], statschange['mpc'])
        if statschange['hpc']: Functions.add_floating_text(f"+{statschange['hpc']}", 'hp', (128, 128, 128))
        if statschange['mpc']: Functions.add_floating_text(f"{statschange['mpc']}", 'mp', (128, 128, 128))
        statschange['hpc'], statschange['mpc'] = None, None

        if mg_state == "mainpage":
            Functions.displaystat = True
            mp =  self.var_dict['mp']
            self.buttons = pygame.sprite.Group()
            for i in range(len(self.pricelist)): 
                self.buttons.add(Buttons(i, mp, self.hplist, self.pricelist, self.btnpos))
                if mp < self.pricelist[i]:
                    self.itemlist[i][0] = pygame.transform.grayscale(self.itemsurflist[i])
                else: self.itemlist[i][0] = self.itemsurflist[i]

        elif mg_state == "menu": 
            Functions.displaystat = False
            self.menu.update()
    
    def draw(self, S, mg_state):
        S.blit(self.base, (0, 0))
        if mg_state == "mainpage": self.mainpage(S)
        elif mg_state == "menu": self.menu.draw(S)
        
    def mainpage(self, S):
        S.blit(self.mainbase, (0, 0))
        S.blit(self.menubtn, self.menubtnrect)
        for surf, rect in self.itemlist: S.blit(surf, rect)
        self.buttons.draw(S)
        Functions.draw_floating_texts(S)
    
class Buttons(pygame.sprite.Sprite):
    def __init__(self, id, mp, hplist, pricelist, btnpos):
        super().__init__()
        self.image = pygame.image.load("Assets/Images/MGE_Buybtn.png").convert_alpha()
        if mp < pricelist[id]: 
            self.clickable = False
            self.image = pygame.transform.grayscale(self.image)
            
        else: self.clickable = True

        self.rect = self.image.get_rect(center = (btnpos[id]))
        self.hpc = hplist[id]
        self.mpc = (-pricelist[id])
                                                                 
    def update(self, E, updatecursor=False):
        if updatecursor:
            self.updatecursor(E)
            return

        global statschange
        if self.rect.collidepoint(E.pos):
            if self.clickable: 
                statschange['hpc'], statschange['mpc'] = self.hpc, self.mpc
                soundtype = "transaction"
            else: soundtype = "btnclicked"
            Functions.playsound(soundtype)

    def updatecursor(self, E):
        global cursorcollide
        if self.rect.collidepoint(E.pos):
            cursorcollide = True
            if self.clickable: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
