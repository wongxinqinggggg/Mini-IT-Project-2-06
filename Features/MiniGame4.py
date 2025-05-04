import pygame

# Variable for MG4
buyingprices = [[300, 400, 500], [800, 900, 1000]]
sellingprices = [[150, 350, 600], [400, 850, 1350]]
vm_colour = [[(50, 41, 71), (207, 255, 112), (255, 250, 209), (77, 166, 255)], 
             [(235, 23, 23), (102, 255, 227), (39, 39, 54)]]
btncolour = [(15, 97, 43), None]
menubtnpos = (975, 50)
btnposX = [130, 630]
btnposY = [250, 300, 380]
txtboxposX = [130, 630]
txtboxposY = [[340, 360], [290, 310], 420]
txtrectsize = [(50, 20), (80, 20), (90, 20)]
txtinfo = ["f\"{buyingprices[i][vm_level[i]]}$\"", 
          "f\"({vm_income[i][vm_level[i]]}$/s)\"",
          "f\"({sellingprices[i][vm_level[i] - 1]}$)\""]

def greyscale(surf, colours):
        if len(colours) > 1: surf = greyscale(surf, colours[1:])
        colour = colours[0] if colours else None
        image = pygame.Surface(surf.get_size())
        newRGB = (colour[0] + colour[1] + colour[2]) / 3 if colour else 1
        image.fill((newRGB, newRGB, newRGB))
        surf.set_colorkey(colour)
        image.blit(surf, (0,0))
        return image

class MG4():
    def __init__(self, S, W, H, var_dict, E=None):
        global temp_vm, mpchange
        self.var_dict, temp_vm, mpchange = var_dict, var_dict['vm_level'], None
        
        if E: self.eventhandler(E)
        self.update()
        if not E: self.draw(S, W, H)

    def eventhandler(self, E):
        if E.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = E.pos
            if self.exitbtnrect.collidepoint(mouse_x, mouse_y): self.var_dict['mg_state'] = None
            else: self.buttons.update(mouse_x, mouse_y, self.var_dict['VM_EVENT'])
        
        elif E.type == pygame.MOUSEMOTION:
            global collidebtn
            collidebtn = False
            mouse_x, mouse_y = E.pos

            if self.exitbtnrect.collidepoint(mouse_x, mouse_y): 
                collidebtn = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                
            else: self.buttons.update(mouse_x, mouse_y, self.var_dict['VM_EVENT'], True)

            if not collidebtn: pygame.mouse.set_cursor()

    def update(self):
        self.var_dict['mpc'], self.var_dict['vm_level'] = mpchange, temp_vm
        pass
    
    def draw(self, S, W, H):
        mp, Sfont = self.var_dict['mp'], self.var_dict['Sfont']
        vm_level, vm_income = self.var_dict['vm_level'], self.var_dict['vm_income']
        
        colourlist = []
        mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (W, H))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = menubtnpos)
        
        self.buttons = pygame.sprite.Group()
        for i in range(len(vm_level)):     # Determine which btn to display based on lvl
            if not vm_level[i]: btnpaths = ["Buybtn"]
            elif vm_level[i] <= 2: btnpaths = ["Upgradebtn", "Sellbtn"]
            else: btnpaths = ["Maxbtn", "Sellbtn"]

            for btnpath in btnpaths: self.buttons.add(Buttons(i, btnpath, mp, vm_level[i]))

            if not vm_level[i]: colourlist.extend(vm_colour[i])    # Greyscale vm that are not bought

        mg4_base = greyscale(mg4_base, colourlist)
        S.blit(mg4_base, (0, 0))
        S.blit(exitbtn, self.exitbtnrect)
        self.buttons.draw(S)
        self.displayinfo(S, vm_level, vm_income, Sfont)        

    def displayinfo(self, S, vm_level, vm_income, Sfont):
        infolist = []
        # Get info and rect based on vm lvl
        for i in range(len(vm_level)):
            if vm_level[i] <= 2:
                for j in range(2):
                    surf = Sfont.render(eval(txtinfo[j]), True, 'Black')
                    k = 1 if vm_level[i] else 0
                    rect = pygame.rect.Rect((0, 0), txtrectsize[j])
                    rect.center = (txtboxposX[i], txtboxposY[k][j])
                    infolist.append([surf, rect])

            if vm_level[i]:
                surf = Sfont.render(eval(txtinfo[2]), True, 'Black')
                if len(str(sellingprices[i][vm_level[i] - 1])) <= 3:
                    rect = pygame.rect.Rect((0, 0), txtrectsize[1])
                    rect.center = (txtboxposX[i], txtboxposY[2])
                else:
                    rect = pygame.rect.Rect((0, 0), txtrectsize[2])
                    rect.center = (txtboxposX[i], txtboxposY[2])
                infolist.append([surf, rect])
        
        for surf, rect in infolist: S.blit(surf, rect)

class Buttons(pygame.sprite.Sprite):
    def __init__(self, vm, btnpath, mp, vm_level):
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
                self.image = greyscale(self.image, btncolour)   # Greyscale btns that cannot afford
                self.image.set_colorkey((1, 1, 1)) 

            else: self.clickable = True

        elif btnpath == "Maxbtn": 
            self.clickable, Y_pos = False, btnposY[0]

        elif btnpath == "Sellbtn": 
            self.clickable, self.attribute = True, 0
            Y_pos = btnposY[2]
            self.mpc = sellingprices[self.id][vm_level - 1]

        self.rect = self.image.get_rect(center = (X_pos, Y_pos))                                         

    def update(self, mouse_x, mouse_y, VM_EVENT, updatecursor=False):
        if updatecursor: 
            self.updatecursor(mouse_x, mouse_y)
            return
        
        global temp_vm, mpchange
        if self.rect.collidepoint(mouse_x, mouse_y): 
            if self.clickable:
                mpchange = self.mpc
                if self.attribute:
                    temp_vm[self.id] += 1
                    pygame.time.set_timer(VM_EVENT[self.id], 1000)
                else: 
                    temp_vm[self.id] = 0
                    pygame.time.set_timer(VM_EVENT[self.id], 0)
     
    def updatecursor(self, mouse_x, mouse_y):
        global collidebtn
        if self.rect.collidepoint(mouse_x, mouse_y):
            collidebtn = True
            if self.clickable: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)