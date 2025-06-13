import pygame
from Features import Functions

class STORE():
    def __init__(self, Menu, Inventory):
        # Initializing variable for store
        global mpchange 
        self.Menu, self.Inventory = Menu, Inventory
        self.pricelist = [10, 25, 50, 120, 45, 100]
        self.infolist = [20, '10s', 150, 500, 80, 200]
        self.rackrect = [(112, 324, 800, 30), (112, 534, 800, 30)]
        self.infopos = [[(245, 220), (245, 252), (323, 250)], [(500, 220), (480, 252), (582, 250)],
                        [(850, 220), (830, 252), (935, 250)], [(270, 430), (270, 462), (375, 460)],
                        [(550, 430), (550, 462), (628, 460)], [(820, 430), (820, 462), (925, 460)]]
        self.btnpos = [(300, 190), (555, 190), (880, 190), (330, 400), (600, 400), (880, 400)]
        itemcenter = [(190, 245), (425, 245), (720, 236), (200, 470), (490, 454), (740, 456)]
        menubtnpos = (975, 50)
        mpchange = None

        Functions.play_music("Retro-Game-Music (moodmode)")
        self.menubtn = Functions.mainbtnlist[1]
        self.menubtnrect = self.menubtn.get_rect(center = menubtnpos)
        self.itemsurflist = Functions.itemlist
        sprint, hp, pethp = Functions.iconlist[2], Functions.iconlist[0], Functions.iconlist[3]
        self.iconlist = [hp, sprint, hp, hp, pethp, pethp]
        self.itemlist = []
        for i in range(len(self.itemsurflist)):
            rect = self.itemsurflist[i].get_rect(center=itemcenter[i])
            self.itemlist.append({'surf': self.itemsurflist[i], 'rect': rect,
                                  'price': f'-{self.pricelist[i]}$', 'pricerect': (self.infopos[i][0], (26, 100)),
                                  'info': f'+{self.infolist[i]}', 'inforect': (self.infopos[i][1], (26, 100)),
                                  'icon': self.iconlist[i], 'iconrect': (self.infopos[i][2], (26, 100))})

        self.btnrectdict = {'mainpage': [self.menubtnrect]}

    def eventhandler(self, mg_state, E):
        if E.type == pygame.MOUSEBUTTONDOWN:
            cursorclicked = False
            if mg_state == "mainpage":
                if self.menubtnrect.collidepoint(E.pos): 
                    self.var_dict['prev_state'] = self.var_dict['mg_state']
                    self.var_dict['mg_state'] = "menu"

                else: self.buttons.update(E, Inventory=self.Inventory)

            elif mg_state == "menu":
                self.var_dict, cursorclicked = self.Menu.eventhandler(E, self.var_dict)

            if self.btnrectdict.get(mg_state): 
                for rect in self.btnrectdict[mg_state]:
                    if rect.collidepoint(E.pos) or cursorclicked:
                        Functions.playsound("btnclicked")
                        break

        elif E.type == pygame.MOUSEMOTION:
            global cursorcollide
            cursorcollide = False
            if mg_state == "menu":
                self.var_dict, cursorcollide = self.Menu.eventhandler(E, self.var_dict)

            if self.btnrectdict.get(mg_state): 
                for rect in self.btnrectdict[mg_state]:
                    if rect.collidepoint(E.pos):
                        cursorcollide = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break
                
                if mg_state == "mainpage": self.buttons.update(E, updatecursor=True)

            if not cursorcollide: pygame.mouse.set_cursor()

        elif E.type == pygame.MOUSEBUTTONUP: self.var_dict['dragging'] = False

    def update(self, mg_state, var_dict):
        global mpchange
        self.var_dict = var_dict
        if mpchange: 
            Functions.update_stats(mpchange=mpchange)
            Functions.add_floating_text(f"{mpchange}", 'mp')
            mpchange = None

        if mg_state == "mainpage":
            Functions.displaystat = True
            self.buttons = pygame.sprite.Group()
            for i in range(len(self.pricelist)): 
                self.buttons.add(Buttons(i, self.pricelist, self.btnpos))
                if Functions.money < self.pricelist[i]:
                    self.itemlist[i]['surf'] = pygame.transform.grayscale(self.itemsurflist[i])
                else: self.itemlist[i]['surf'] = self.itemsurflist[i]

        elif mg_state == "menu": 
            Functions.displaystat = False
            self.Menu.update()
    
    def draw(self, S, mg_state):
        S.fill((77, 166, 255))
        if mg_state == "mainpage": self.mainpage(S)
        elif mg_state == "menu": self.Menu.draw(S)
        
    def mainpage(self, S):
        for i in range(2):
            pygame.draw.rect(S, (96, 96, 112), self.rackrect[i])
        S.blit(self.menubtn, self.menubtnrect)
        for item in self.itemlist:
            S.blit(item['surf'], item['rect'])
            txt = self.var_dict['Mfont'].render(item['price'], False, 'Black')
            S.blit(txt, item['pricerect'])
            S.blit(item['icon'], item['iconrect'])
            txt = self.var_dict['Mfont'].render(item['info'], False, 'Black')
            S.blit(txt, item['inforect'])
        self.buttons.draw(S)
        Functions.draw_floating_texts(S)
    
class Buttons(pygame.sprite.Sprite): # Sprite grp for btns
    def __init__(self, id, pricelist, btnpos):
        super().__init__()
        self.image = Functions.tbtnlist[0]
        if Functions.money < pricelist[id]: 
            self.clickable = False
            self.image = pygame.transform.grayscale(self.image)
            
        else: self.clickable = True

        self.rect = self.image.get_rect(center = (btnpos[id]))
        self.mpc = (-pricelist[id])
        self.item_id = id + 1
                                                                 
    def update(self, E, Inventory=None, updatecursor=False):
        if updatecursor:
            self.updatecursor(E)
            return

        global mpchange
        soundtype = None
        if self.rect.collidepoint(E.pos):
            if self.clickable: 
                if Inventory.additem(self.item_id):
                    mpchange = self.mpc 
                    soundtype = "transaction"

            soundtype = "btnclicked" if not soundtype else soundtype
            Functions.playsound(soundtype)

    def updatecursor(self, E):
        global cursorcollide
        if self.rect.collidepoint(E.pos):
            cursorcollide = True
            if self.clickable: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
