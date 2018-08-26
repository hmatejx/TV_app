#!/usr/bin/python
#
import pygame
from pygame.locals import *
from utils import *

# import configuration
import config

# import main menu class
import menu


# MAIN PROGRAM
if __name__ == '__main__':

    # read configuration
    cfg = config.Config()

    # hide mouse cursor
    set_cursor('%s/etc/empty.cursor' % cfg.cwd)

    # initialize pygame
    pygame.init()
    pygame.display.set_mode((cfg.dimx, cfg.dimy))
    pygame.mouse.set_visible(0)
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([KEYDOWN, QUIT, USEREVENT + 1])

    # launch start menu
    menu = menu.Menu(cfg)
    rv = menu.start_menu()

    # stop pygame
    pygame.quit()

    # Remote Control Quit request: perform a gracefull shutdown!
    if rv == 1 and cfg.shutdown:
        shutdown()
    else:
        # show cursor again
        set_cursor()

