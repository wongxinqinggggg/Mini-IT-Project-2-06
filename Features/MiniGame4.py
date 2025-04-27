import pygame

class MG4():
    def __init__(self, screen, width, height, mg_state):
        self.screen, self.WIDTH, self.HEIGHT, self.mg_state = screen, width, height, mg_state
        
        if self.mg_state == "mainpage": self.mainpage()

    def mainpage(self):
        mg4_base = pygame.transform.scale(pygame.image.load("Assets/Images/MG4_Base.png").convert(), (self.WIDTH, self.HEIGHT))
        colourlist = [(235, 23, 23), (102, 255, 227)]
        mg4_base = self.greyscale(mg4_base, colourlist)
        self.screen.blit(mg4_base, (0, 0))

    def greyscale(self, surf, colourlist):
        image = pygame.Surface(surf.get_size())
        for colour in colourlist:
            newRGB = (colour[0] + colour[1] + colour[2]) / 3
            image.fill((newRGB, newRGB, newRGB))
            surf.set_colorkey(colour)
            image.blit(surf, (0,0))
        
        return image
