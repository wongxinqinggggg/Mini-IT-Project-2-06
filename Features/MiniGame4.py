import pygame

templist = None

class MG4():
    def __init__(self, screen, width, height, mg_state, vending_machines):
        self.screen, self.WIDTH, self.HEIGHT, self.mg_state, self.vending_machines = screen, width, height, mg_state, vending_machines
        
        if self.mg_state == "mainpage": self.mainpage()

    def mainpage(self):
        mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (self.WIDTH, self.HEIGHT))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = (750, 50))

        colourlist = []
        if not self.vending_machine[0]: 
            colourlist += [(50, 41, 71), (207, 255, 112), (255, 250, 209), (77, 166, 255)]
        if not self.vending_machine[1]: 
            colourlist += [(235, 23, 23), (102, 255, 227), (39, 39, 54)]

        for colour in colourlist: mg4_base = self.greyscale(mg4_base, colour)
        self.screen.blit(mg4_base, (0, 0))
        self.screen.blit(exitbtn, self.exitbtnrect)

        self.buttons = pygame.sprite.Group()
        for i in range(len(self.vending_machines)):
            if not self.vending_machines[i]:
                btnpaths = ["Buybtn"]
            else:
                btnpaths = ["Upgradebtn", "Sellbtn"]

            for btnpath in btnpaths: self.buttons.add(Buttons(i, btnpath))
        
        self.buttons.draw(self.screen)

    def greyscale(self, surf, colour):
        image = pygame.Surface(surf.get_size())
        newRGB = (colour[0] + colour[1] + colour[2]) / 3
        image.fill((newRGB, newRGB, newRGB))
        surf.set_colorkey(colour)
        image.blit(surf, (0,0))
        return image
    
    def eventhandler(self, mouse_X, mouse_Y):
        global templist
        templist = self.vending_machines

        if self.exitbtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = None
        else: self.buttons.update(mouse_X, mouse_Y)
        return templist

    def getstate(self):
        return self.mg_state

class Buttons(pygame.sprite.Sprite):
    def __init__(self, vending_machine, btnpath):
        super().__init__()
        self.attributes = [None, None]

        if not vending_machine: X_pos, self.attributes[0] = 55, 0 
        else: X_pos, self.attributes[0] = 455, 1

        if btnpath == "Buybtn": Y_pos, self.attributes[1] = 300, 1
        elif btnpath == "Upgradebtn": Y_pos, self.attributes[1] = 250, +1
        else: Y_pos, self.attributes[1] = 380, 0

        self.image = pygame.image.load(f"Assets/Images/MGE_{btnpath}.png").convert_alpha()
        self.rect = pygame.rect.Rect(X_pos, Y_pos, 76, 34)                                        
                                                                 
    def update(self, mouse_X, mouse_Y):
        global templist

        if self.rect.collidepoint(mouse_X, mouse_Y): 
           templist[self.attributes[0]] = self.attributes[1]