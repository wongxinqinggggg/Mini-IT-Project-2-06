import pygame

class MG4():
    def __init__(self, screen, width, height, mg_state, vending_machine):
        self.screen, self.WIDTH, self.HEIGHT, self.mg_state, self.vending_machine = screen, width, height, mg_state, vending_machine
        
        if self.mg_state == "mainpage": self.mainpage()

    def mainpage(self):
        mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (self.WIDTH, self.HEIGHT))

        colourlist = []
        if not self.vending_machine[0]: colourlist += [(50, 41, 71), (207, 255, 112), (255, 250, 209), (77, 166, 255)]
        if not self.vending_machine[1]: colourlist += [(235, 23, 23), (102, 255, 227), (39, 39, 54)]

        for colour in colourlist: mg4_base = self.greyscale(mg4_base, colour)
        self.screen.blit(mg4_base, (0, 0))

    def greyscale(self, surf, colour):
        image = pygame.Surface(surf.get_size())
        newRGB = (colour[0] + colour[1] + colour[2]) / 3
        image.fill((newRGB, newRGB, newRGB))
        surf.set_colorkey(colour)
        image.blit(surf, (0,0))
        return image
