import pygame
from pygame.locals import *

# import modules
import config
import remote
import theme
import tv
import video
import dvd
import music
import photo
import web

class Menu:

    def __init__(self, config):
        # read config file
        self.cfg = config

        # launch remote control "driver"
        if self.cfg.remote:
            self.rc = remote.Remote()
        else:
            self.rc = None

        # initialize theme
        self.thm = theme.Theme(self.cfg)

        # initialize menu classes
        self.tv_menu = tv.TV_Menu(self.cfg, self.thm)
        self.video_menu = video.Video_Menu(self.cfg, self.thm)
        self.dvd_menu = dvd.DVD_Menu(self.cfg, self.thm)
        self.music_menu = music.Music_Menu(self.cfg, self.thm)
        self.photo_menu = photo.Photo_Menu(self.cfg, self.thm)
        self.web_menu = web.Web_Menu(self.cfg, self.thm)


    def start_menu(self):
        # menu position image
        ps = self.cfg.fontsize
        posimage = pygame.Surface((ps+2, ps+2), SRCALPHA, 32)
        pygame.draw.polygon(posimage, self.cfg.fonthi, ((0, 0), (0, ps), (ps/2, ps/2)), 0)
        pygame.draw.line(posimage, self.cfg.fontbg, (0, ps), (ps/2, ps/2), 3)

        def render_text(menu_text, color):
            return [self.thm.font.render(text, True, color) for text in menu_text]

        # menu item text
        menu_text = ["TV", "VIDEO", "DVD", "RADIO", "PHOTO", "GOLD", "QUIT"]
        options = render_text(menu_text, self.cfg.fontcol)
        optionsB = render_text(menu_text, self.cfg.fontbg)
        optionsH = render_text(menu_text, self.cfg.fonthi)

        # calc. screen positions
        x1 = self.cfg.dimx*self.cfg.xm
        y1 = self.cfg.dimy*self.cfg.ym
        x2 = self.cfg.dimx*self.cfg.xi
        y2 = self.cfg.dimy*self.cfg.yi

        # text spacing
        deltay = 100

        def draw_start_menu(marker):
            # get current screen
            screen = pygame.display.get_surface()

            # draw background
            screen.blit(self.thm.background_image, (0, 0))

            # draw remote icon
            if self.cfg.remote:
                screen.blit(self.thm.remote_image, (32, self.cfg.dimy - 80))

            # draw menu text
            for i in range(0, len(options)):
                yt = y1 + deltay*i
                yb = yt + deltay
                if i != marker:
                    screen.blit(options[i], (x1, yb))
                else:
                    screen.blit(optionsB[i], (x1 + 2, yb + 2))
                    screen.blit(optionsH[i], (x1, yb))

            # draw selected text marker
            screen.blit(posimage, (x1 - 80, y1 + deltay*(marker + 1) + 5))
            screen.blit(self.thm.menu_image[marker], (x2, y2))

        def launch_item(pos):
            # VLC TV
            if pos == 0:
                self.tv_menu.start()
            # VLC videos
            elif pos == 1:
                self.video_menu.start()
            # Mplayer DVD
            elif pos == 2:
                self.dvd_menu.start()
            # Music
            elif pos == 3:
                self.music_menu.start()
            # view photos
            elif pos == 4:
                self.photo_menu.start()
            # view gold price
            elif pos == 5:
                self.web_menu.start()
            else:
                return False
            return True

        # main menu loop
        pos = 0
        maxpos = len(options)
        # draw initial menu
        draw_start_menu(pos)
        pygame.display.flip()
        while 1:
            # process events
            e = pygame.event.wait()
            if e.type == QUIT:
                exit(255)
            # any key pressed?
            elif e.type == KEYDOWN:
                redraw = True
                # DOWN ARROW or N
                if e.key == K_DOWN or e.key == K_n:
                    pos += 1
                    if pos == maxpos: pos = 0
                # UP ARROW or P
                elif e.key == K_UP or e.key == K_p:
                    pos -= 1
                    if pos < 0: pos = maxpos - 1
                # ENTER or ESCAPE
                elif e.key == K_RETURN or e.key == K_ESCAPE:
                    if not launch_item(pos):
                        # transmit Quit request
                        if e.key == K_ESCAPE:
                            return 1
                        else:
                            return 0
                # R (restart remote driver)
                elif e.key == K_r:
                    self.rc.restart()
                    redraw = False
                
                # draw menu
                if redraw:
                    draw_start_menu(pos)
                    pygame.display.flip()
