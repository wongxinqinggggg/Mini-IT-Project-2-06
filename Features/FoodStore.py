import pygame

statschange = None
hplist = [20, 65, 150, 500]
pricelist = [10, 25, 50, 120]
btncolour = (15, 97, 43)
btnpos = [(465, 190), (755, 190), (475, 400), (750, 395)]
colours = [[(12, 80, 46), (0, 189, 38)], [(0, 61, 184), (255, 0, 0)], 
           [(240, 215, 128), (128, 212, 156), (36, 185, 85), (15, 97, 43), 
            (20, 69, 36), (168, 143, 89), (94, 78, 18)], 
            [(75, 91, 171), (71, 59, 120)]]

def greyscale(surf, colour = None):
        image = pygame.Surface(surf.get_size())
        newRGB = (colour[0] + colour[1] + colour[2]) / 3 if colour else 0
        image.fill((newRGB, newRGB, newRGB))
        surf.set_colorkey(colour)
        image.blit(surf, (0,0))
        return image

class STORE():
    def mainpage(self, screen, width, height, mg_state, mp):
        colourlist = []
        self.screen, self.mg_state = screen, mg_state
        base = pygame.transform.scale(pygame.image.load("Assets/Images/STORE_base.png").convert(), (width, height))
        exitbtn = pygame.image.load("Assets/Images/MGE_Exitbtn.png").convert_alpha()
        self.exitbtnrect = exitbtn.get_rect(center = (975, 50))

        for i in range(len(pricelist)):
            if mp < pricelist[i]: colourlist.extend(colours[i])
        for colour in colourlist: base = greyscale(base, colour)

        self.buttons = pygame.sprite.Group()
        for i in range(len(pricelist)): self.buttons.add(Buttons(i, mp))

        self.screen.blit(base, (0, 0))
        self.screen.blit(exitbtn, self.exitbtnrect)
        self.buttons.draw(self.screen)

    def eventhandler(self, mouse_X, mouse_Y, mp):
        global statschange 
        statschange = [None, None]

        if self.exitbtnrect.collidepoint(mouse_X, mouse_Y): self.mg_state = None
        else: self.buttons.update(mouse_X, mouse_Y, mp)

        return statschange
    
    def getstate(self):
        return self.mg_state

class Buttons(pygame.sprite.Sprite):
    def __init__(self, id, mp):
        super().__init__()
        buybtn = pygame.image.load("Assets/Images/MGE_Buybtn.png").convert_alpha()
        if mp < pricelist[id]: 
            buybtn = greyscale(buybtn)
            buybtn = greyscale(buybtn, btncolour)
            buybtn.set_colorkey((0, 0, 0))    

        self.image = buybtn
        self.rect = self.image.get_rect(center = (btnpos[id]))
        self.id = id
                                                                 
    def update(self, mouse_X, mouse_Y, mp):
        global statschange
         
        if self.rect.collidepoint(mouse_X, mouse_Y):
            if mp >= pricelist[self.id]: 
                print(pricelist[self.id])
                statschange[0] = hplist[self.id]
                statschange[1] = (-pricelist[self.id])
            else:
                statschange[0] = None
                statschange[1] = None