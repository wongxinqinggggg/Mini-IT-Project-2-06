import pygame

# Variable for MG4
temp_vm = None
mpchange = None
buyingprices = [[300, 400, 500], [800, 900, 1000]]
sellingprices = [[150, 350, 600], [400, 850, 1350]]
vm1_colour = [(50, 41, 71), (207, 255, 112), (255, 250, 209), (77, 166, 255)]
vm2_colour = [(235, 23, 23), (102, 255, 227), (39, 39, 54)]
txtboxposX = [[64, 52], [464, 452]]
txtboxposY = [[343, 363], [295, 315], 428]
txtrectsize = (200, 100)
txtinfo = ["f\"{buyingprices[i][self.vm_level[i]]}$\"", 
          "f\"({vm_income[i][self.vm_level[i]]}$/s)\"",
          "f\"({sellingprices[i][self.vm_level[i] - 1]}$)\""]

class MG4():
    def mainpage(self, screen, width, height, mg_state, vm_level, vm_income, Sfont):
        self.screen, self.mg_state, self.vm_level = screen, mg_state, vm_level
        mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (width, height))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = (750, 50))

        colourlist = []
        if not self.vending_machine[0]: colourlist.extend(vm1_colour)
        if not self.vending_machine[1]: colourlist.extend(vm2_colour)

        for colour in colourlist: mg4_base = self.greyscale(mg4_base, colour)
        self.screen.blit(mg4_base, (0, 0))
        self.screen.blit(exitbtn, self.exitbtnrect)

        self.buttons = pygame.sprite.Group()
        for i in range(len(self.vm_level)):     # Determine which btn to display based on lvl
            if not self.vm_level[i]: btnpaths = ["Buybtn"]
            elif self.vm_level[i] <= 2: btnpaths = ["Upgradebtn", "Sellbtn"]
            else: btnpaths = ["Maxbtn", "Sellbtn"]

            for btnpath in btnpaths: self.buttons.add(Buttons(i, btnpath))
        
        self.buttons.draw(self.screen)
        self.displayinfo(vm_income, Sfont)

    def greyscale(self, surf, colour):
        image = pygame.Surface(surf.get_size())
        newRGB = (colour[0] + colour[1] + colour[2]) / 3
        image.fill((newRGB, newRGB, newRGB))
        surf.set_colorkey(colour)
        image.blit(surf, (0,0))
        return image
    
    def eventhandler(self, mouse_X, mouse_Y, mp, VM1, VM2):
        global temp_vm, mpchange
        temp_vm, mpchange = self.vm_level, None

        if self.exitbtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = None
        else: self.buttons.update(mouse_X, mouse_Y, mp, VM1, VM2)
        return temp_vm

    def getstate(self):
        return self.mg_state

    def displayinfo(self, vm_income, Sfont):
        infolist = []

        # Get info and rect based on vm lvl
        for i in range(len(self.vm_level)):
            if self.vm_level[i] <= 2:
                for j in range(2):
                    surf = Sfont.render(eval(txtinfo[j]), True, 'Black')
                    k = 1 if self.vm_level[i] else 0
                    rect = pygame.rect.Rect((txtboxposX[i][j], txtboxposY[k][j]), txtrectsize)
                    infolist.append([surf, rect])

            if self.vm_level[i]:
                surf = Sfont.render(eval(txtinfo[2]), True, 'Black')
                rect = pygame.rect.Rect((txtboxposX[i][1], txtboxposY[2]), txtrectsize)
                infolist.append([surf, rect])
        
        for surf, rect in infolist: self.screen.blit(surf, rect)

class Buttons(pygame.sprite.Sprite):
    def __init__(self, vending_machine, btnpath):
        super().__init__()
        self.attributes = [None, None]

        if not vending_machine: X_pos, self.attributes[0] = 55, 0 
        else: X_pos, self.attributes[0] = 455, 1

        if btnpath == "Buybtn": Y_pos, self.attributes[1] = 300, 1
        elif btnpath == "Upgradebtn": Y_pos, self.attributes[1] = 250, 2
        elif btnpath == "Maxbtn": Y_pos, self.attributes[1] = 250, 3
        else: Y_pos, self.attributes[1] = 380, 0

        self.image = pygame.image.load(f"Assets/Images/MGE_{btnpath}.png").convert_alpha()
        self.rect = pygame.rect.Rect(X_pos, Y_pos, 76, 34)                                        
                                                                 
    def update(self, mouse_X, mouse_Y, mp, VM1, VM2):
        global temp_vm, mpchange

        if self.rect.collidepoint(mouse_X, mouse_Y): 
            if not self.attributes[1]: 
                mpchange = sellingprices[self.attributes[0]][temp_vm[self.attributes[0]] - 1]
                temp_vm[self.attributes[0]] = 0
                if not self.attributes[0]: pygame.time.set_timer(VM1, 0)
                else: pygame.time.set_timer(VM2, 0)

            elif self.attributes[1] == 3: pass

            else:
                buyingprice =  buyingprices[self.attributes[0]][temp_vm[self.attributes[0]]]
                if mp >= buyingprice: 
                    mpchange = -buyingprice 
                    temp_vm[self.attributes[0]] += 1
                    if not self.attributes[0]: pygame.time.set_timer(VM1, 10000)
                    else: pygame.time.set_timer(VM2, 10000)
     