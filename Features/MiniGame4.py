import pygame

class MG4():
    def __init__(self, screen, width, height, mg_state, vending_machine):
        self.screen, self.WIDTH, self.HEIGHT, self.mg_state, self.vending_machine = screen, width, height, mg_state, vending_machine
        
        if self.mg_state == "mainpage": self.mainpage()

    def mainpage(self):
        mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (self.WIDTH, self.HEIGHT))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = (750, 50))
        buybtn = pygame.image.load("Assets/Images/MGE_Buybtn.png").convert_alpha()
        upgradebtn = pygame.image.load("Assets/Images/MGE_Upgradebtn.png").convert_alpha()
        sellbtn = pygame.image.load("Assets/Images/MGE_Sellbtn.png").convert_alpha()

        colourlist = []
        btnlist = []
        if not self.vending_machine[0]: 
            colourlist += [(50, 41, 71), (207, 255, 112), (255, 250, 209), (77, 166, 255)]
            self.buybtnrect1 = buybtn.get_rect(center = (100, 300))
            btnlist.append([buybtn, self.buybtnrect1])
        if not self.vending_machine[1]: 
            colourlist += [(235, 23, 23), (102, 255, 227), (39, 39, 54)]
            self.buybtnrect2 = buybtn.get_rect(center = (500, 300))
            btnlist.append([buybtn, self.buybtnrect2])

        for colour in colourlist: mg4_base = self.greyscale(mg4_base, colour)
        self.screen.blit(mg4_base, (0, 0))
        self.screen.blit(exitbtn, self.exitbtnrect)
        for surf, rect in btnlist: self.screen.blit(surf, rect)

    def greyscale(self, surf, colour):
        image = pygame.Surface(surf.get_size())
        newRGB = (colour[0] + colour[1] + colour[2]) / 3
        image.fill((newRGB, newRGB, newRGB))
        surf.set_colorkey(colour)
        image.blit(surf, (0,0))
        return image
    
    def eventhandler(self, mouse_X, mouse_Y):
        if self.exitbtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = None
        elif self.buybtnrect1.collidepoint(mouse_X, mouse_Y): self.vending_machine[0] = 1
        elif self.buybtnrect2.collidepoint(mouse_X, mouse_Y): self.vending_machine[1] = 1
        return self.vending_machine

    def getstate(self):
        return self.mg_state
