import pygame
from Features import Functions

class MG4():
    def __init__(self, W, H):
        global temp_vm, mpchange
        temp_vm, mpchange = [], None
        self.infolist = []
        self.buyingprices = [[300, 400, 500], [800, 900, 1000]]
        self.sellingprices = [[150, 350, 600], [400, 850, 1350]]
        self.menubtnpos = (975, 50)
        self.btnposX = [130, 630]
        self.btnposY = [250, 300, 380]
        self.txtboxposX = [130, 630]
        self.txtboxposY = [[340, 360], [290, 310], 420]
        self.txtrectsize = [(50, 20), (80, 20), (90, 20)]
        self.txtinfo = ["f\"{self.buyingprices[i][vm_level[i]]}$\"", 
                    "f\"({vm_income[i][vm_level[i]]}$/s)\"",
                    "f\"({self.sellingprices[i][vm_level[i] - 1]}$)\""]
        
        self.mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (W, H))
        self.vm1 = pygame.image.load("Assets/Images/MG4_VM1.png").convert_alpha()
        self.vm1rect = self.vm1.get_rect(center = (350, 375))
        self.vm2 = pygame.image.load("Assets/Images/MG4_VM2.png").convert_alpha()
        self.vm2rect = self.vm2.get_rect(center = (860, 375))
        self.menubtn = pygame.image.load("Assets/Images/MAIN_Menubtn.png").convert_alpha()
        self.menubtnrect = self.menubtn.get_rect(center = self.menubtnpos)

    def eventhandler(self, E, var_dict):
        if E.type == pygame.MOUSEBUTTONDOWN:
            if self.menubtnrect.collidepoint(E.pos): 
                self.var_dict['mg_state'] = None
            else: self.buttons.update(E, self.var_dict['VM_EVENT'])
        
        elif E.type == pygame.MOUSEMOTION:
            global collidebtn
            collidebtn = False
            E.pos = E.pos

            if self.menubtnrect.collidepoint(E.pos): 
                collidebtn = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                
            else: self.buttons.update(E, self.var_dict['VM_EVENT'], True)

            if not collidebtn: pygame.mouse.set_cursor()

    def update(self, mg_state, var_dict):
        global temp_vm, mpchange
        self.var_dict, temp_vm = var_dict, var_dict['vm_level']

        if mg_state == "mainpage":
            mp, Sfont = self.var_dict['mp'], self.var_dict['Sfont']
            vm_level, vm_income = self.var_dict['vm_level'], self.var_dict['vm_income']
            self.buttons, self.infolist = pygame.sprite.Group(), []
            self.vm1surf, self.vm2surf = self.vm1, self.vm2
            for i in range(len(vm_level)):  # Determine which btn to display based on lvl
                if not vm_level[i]: 
                    btnpaths = ["Buybtn"]
                    if not i: self.vm1surf = pygame.transform.grayscale(self.vm1) # Greyscale vm that are not bought
                    else: self.vm2surf = pygame.transform.grayscale(self.vm2) 
                elif vm_level[i] <= 2: btnpaths = ["Upgradebtn", "Sellbtn"]
                else: btnpaths = ["Maxbtn", "Sellbtn"]

                for btnpath in btnpaths: self.buttons.add(Buttons(i, btnpath, mp, vm_level[i], self.btnposX, self.btnposY, self.buyingprices, self.sellingprices))

            for i in range(len(vm_level)):
                if vm_level[i] <= 2:
                    for j in range(2):
                        surf = Sfont.render(eval(self.txtinfo[j]), True, 'Black')
                        k = 1 if vm_level[i] else 0
                        rect = pygame.rect.Rect((0, 0), self.txtrectsize[j])
                        rect.center = (self.txtboxposX[i], self.txtboxposY[k][j])
                        self.infolist.append([surf, rect])

                if vm_level[i]:
                    surf = Sfont.render(eval(self.txtinfo[2]), True, 'Black')
                    if len(str(self.sellingprices[i][vm_level[i] - 1])) <= 3:
                        rect = pygame.rect.Rect((0, 0), self.txtrectsize[1])
                        rect.center = (self.txtboxposX[i], self.txtboxposY[2])
                    else:
                        rect = pygame.rect.Rect((0, 0), self.txtrectsize[2])
                        rect.center = (self.txtboxposX[i], self.txtboxposY[2])
                    self.infolist.append([surf, rect])

        self.var_dict['hp'], self.var_dict['mp'] = Functions.update_stats(self.var_dict['hp'], self.var_dict['mp'], mpchange=mpchange)
        if mpchange: 
            if mpchange < 0: Functions.add_floating_text(f"{mpchange}", 'mp', (128, 128, 128))
            else: Functions.add_floating_text(f"+{mpchange}", 'mp', (128, 128, 128))
        mpchange, self.var_dict['vm_level'] = None, temp_vm

        if mg_state == "mainpage": self.var_dict['displaystats'] = True
        elif mg_state == "menu": self.var_dict['displaystats'] = False
    
    def draw(self, S, mg_state):
        S.blit(self.mg4_base, (0, 0))
        if mg_state == "mainpage": self.mainpage(S)
        elif mg_state == "menu": self.menu(S)

    def mainpage(self, S):
        S.blit(self.menubtn, self.menubtnrect)
        S.blit(self.vm1surf, self.vm1rect)
        S.blit(self.vm2surf, self.vm2rect)
        for surf, rect in self.infolist: S.blit(surf, rect)
        self.buttons.draw(S)
        Functions.draw_floating_texts(S, self.var_dict['Mfont'])

    def manu(self, S):
        pass
        
class Buttons(pygame.sprite.Sprite):
    def __init__(self, vm, btnpath, mp, vm_level, btnposX, btnposY, buyingprices, sellingprices):
        super().__init__()
        self.id = vm
        self.image = pygame.image.load(f"Assets/Images/MGE_{btnpath}.png").convert_alpha() 
        X_pos = btnposX[self.id]

        if btnpath == "Buybtn" or btnpath == "Upgradebtn": 
            Y_pos = btnposY[1] if btnpath == "Buybtn" else btnposY[0]
            self.mpc = (-buyingprices[self.id][vm_level])
            self.attribute = 1
            if mp < (-self.mpc):
                self.clickable = False
                self.image = pygame.transform.grayscale(self.image)

            else: self.clickable = True

        elif btnpath == "Maxbtn": 
            self.clickable, Y_pos = False, btnposY[0]

        elif btnpath == "Sellbtn": 
            self.clickable, self.attribute = True, 0
            Y_pos = btnposY[2]
            self.mpc = (+sellingprices[self.id][vm_level - 1])
        
        self.rect = self.image.get_rect(center = (X_pos, Y_pos))      
                                                                 
    def update(self, E, VM_EVENT, updatecursor=False):
        if updatecursor: 
            self.updatecursor(E)
            return
        
        global temp_vm, mpchange
        if self.rect.collidepoint(E.pos): 
            if self.clickable:
                mpchange = self.mpc
                if self.attribute:
                    temp_vm[self.id] += 1
                    pygame.time.set_timer(VM_EVENT[self.id], 1000)
                else: 
                    temp_vm[self.id] = 0
                    pygame.time.set_timer(VM_EVENT[self.id], 0)

    def updatecursor(self, E):
        global collidebtn
        if self.rect.collidepoint(E.pos):
            collidebtn = True
            if self.clickable: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
