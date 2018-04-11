import pygame
from pygame.locals import *
from utils import *


class DVD_Menu:
    
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    
    def start(self):
        # launch mplayer
        mplayer_config = '%s/etc/mplayer_input.conf' % self.config.cwd
        launch_mplayer(['dvd://2-99', '-slang', 'sl,en', '-input', 'conf=%s' % mplayer_config])

        # eject DVD
        screen = pygame.display.get_surface()
        screen.blit(self.theme.background_image, (0, 0))
        x2, y2 = self.config.dimx*self.config.xi, self.config.dimy*self.config.yi
        screen.blit(self.theme.menu_image[2], (x2, y2))
        text = self.theme.font.render('Ejecting...', True, self.config.fontcol)
        screen.blit(text, (x2, y2 + 300))    
        if self.config.remote:
            screen.blit(self.theme.remote_image, (32, self.config.dimy - 80))
        pygame.display.flip()
        exec_external_app('eject')
        
        return True
