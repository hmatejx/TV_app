import pygame
from pygame.locals import *
import os
from utils import *


class Web_Menu:

    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def preprocess(self):
        
        # render html file
        utils.exec_external_app('/usr/local/bin/CutyCapt', ['--url=file:%s/web/gold.html' % self.config.cwd, \
                                             '--out=%s/web/render.png' % self.config.cwd, \
                                             '--min-width=%s' % self.config.dimx, \
                                             '--min-height=%s'% self.config.dimy])
            
        # load image
        image = pygame.image.load('%s/web/render.png' % self.config.cwd)     
        return image

    def start(self):

        # get current screen
        screen = pygame.display.get_surface()
        image = self.preprocess()

        screen.blit(image, (0, 0))
        pygame.display.flip()
        while 1:
            # process events
            e = pygame.event.wait()
            if e.type == QUIT:
                exit()
            # any key pressed?
            elif e.type == KEYDOWN:
                # ENTER
                if e.key == K_RETURN or e.key == K_ESCAPE:
                    # exit web mode
                    break
        return True
