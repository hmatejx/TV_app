import pygame
from pygame.locals import *
import os
from utils import *
import random


# a list of valid video extensions
vidext = {'.avi'  : 'mplayer',
		  '.mpg'  : 'mplayer',
		  '.mpeg' : 'mplayer',
		  '.xvid' : 'mplayer',
		  '.divx' : 'mplayer',
		  '.iso'  : 'mplayer',
		  '.mp4'  : 'mplayer-x264',
		  '.mkv'  : 'mplayer',
		  '.mov'  : 'mplayer',
		  '.vob'  : 'mplayer',
		  '.flv'  : 'mplayer',
		  '.mp3'  : 'mplayer'}


class Video_Menu:

    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def start(self):
        # file list frame
        frimage = pygame.Surface((self.config.dimx, self.config.dimy), SRCALPHA, 32)
        pygame.draw.rect(frimage, self.config.bgcol, (64, 64, self.config.dimx - 128, self.config.dimy - 160))
        pygame.draw.rect(frimage, self.config.fontcol, (64, 64, self.config.dimx - 128, self.config.dimy - 160), 1)

        # marker image
        font_height = self.theme.font.size('A')[1]
        ps = self.config.fontsize
        posimage = pygame.Surface((ps+2, ps+2), SRCALPHA, 32)
        pygame.draw.polygon(posimage, self.config.fonthi, ((0,0), (0,ps), (ps/2,ps/2)), 0)
        pygame.draw.line(posimage, self.config.fontbg, (0,ps), (ps/2,ps/2), 3)

        # geometry parameters
        items_per_page = (self.config.dimy - 224) / font_height
        name_max = 48

        # base directory
        video_path = os.path.normpath(self.config.playlist_video)

        def draw_video_menu(place, marker):
            # get current screen
            screen = pygame.display.get_surface()

            # draw background
            screen.blit(self.theme.background_image, (0, 0))

            # draw remote icon
            if self.config.remote:
                screen.blit(self.theme.remote_image, (32, self.config.dimy - 80))

            # draw frame
            screen.blit(frimage, (0, 0))

            # draw visible items
            count = 0
            col = 160
            for item in items[place:]:
                ren_name = item
                line = 80 + count*font_height
                if len(item) > name_max:
                    ren_name = ren_name[:name_max] + '~'
                if os.path.isdir(os.path.join(cwd, item)):
                    ren_name = '[' + ren_name + ']'
                rline = pygame.Surface((self.config.dimx - col, font_height + 2),  SRCALPHA, 32)
                # highlight selected
                if item == '***':
                    ren_name = '[  ]'
                    rline.blit(posimage, (col + 26, 5))
                if count == marker:
                    renH = self.theme.font2.render(ren_name, True, self.config.fonthi)
                    renB = self.theme.font2.render(ren_name, True, self.config.fontbg)
                    rline.blit(renB, (col+2, 2))
                    rline.blit(renH, (col, 0))
                    rline.blit(posimage, (col - 70, 5))
                else:
                    ren = self.theme.font2.render(ren_name, True, self.config.fontcol)
                    rline.blit(ren, (col, 0))
                screen.blit(rline, (0, line))
                count += 1
                if count == items_per_page:
                    break



        # get top directory items
        cwd = video_path
        items = list_dir(cwd, vidext.keys())
        # top directory does not exist
        if items is None:
            return True

        items.append('***')

        # main loop
        maxpos = len(items)
        pos, place, marker = 0, 0, 0
        draw_video_menu(place, marker)
        pygame.display.flip()
        while 1:
            # process events
            e = pygame.event.wait()
            if e.type == QUIT:
                exit()
            # any key pressed?
            elif e.type == KEYDOWN:
                # DOWN ARROW or N
                if e.key == K_DOWN or e.key == K_n:
                    marker += 1
                    # reached end of page?
                    if marker == items_per_page:
                        # but not end of list?
                        if place + marker < maxpos:
                            place += items_per_page
                        else:
                            place = 0
                        marker = 0
                    # reached end of list?
                    elif place + marker == maxpos:
                        place = 0
                        marker = 0
                    pos = place + marker
                # UP ARROW or P
                elif e.key == K_UP or e.key == K_p:
                    marker -= 1
                    pos -= 1
                    # reached start of page?
                    if marker < 0:
                        # go to previous page
                        if place >= items_per_page:
                            place -= items_per_page
                            marker = items_per_page - 1
                        # go to end
                        else:
                            if maxpos > items_per_page:
                                place = ((maxpos - 1)/ items_per_page) * items_per_page
                            else:
                                place = 0
                            marker = maxpos - 1 - place
                        pos = place + marker
                # ENTER
                elif e.key == K_RETURN or e.key == K_ESCAPE:
                    # exit video mode?
                    if cwd == video_path and pos == 0:
                        break
                    # is it a directory?
                    elif os.path.isdir(os.path.join(cwd, items[pos])) and items[pos] != 'VIDEO_TS':
                        cwd = os.path.normpath(os.path.join(cwd, items[pos]))
                        items = list_dir(cwd, vidext.keys())
                        items.append('***')
                        maxpos = len(items)
                        pos, place, marker = 0, 0, 0
                    # is it a ripped DVD, launch mplayer
                    elif items[pos] == 'VIDEO_TS':
                        dvdpath = os.path.join(cwd, items[pos])
                        launch_mplayer(['dvd://', '-dvd-device', dvdpath, '-slang', 'sl,en', \
                                        '-input', 'conf=%s/etc/mplayer_input.conf' % self.config.cwd])
					# playlist
                    elif items[pos] == '***':
                        files = [os.path.join(cwd, f) for f in items if not os.path.isdir(os.path.join(cwd, f)) or items is not '***']
                        random.shuffle(files) 
                        arg = ['-cache', '8192', '-input', 'conf=%s/etc/mplayer_input.conf' % self.config.cwd]
                        launch_mplayer(arg + files)
                    # else launch selected player
                    else:
						ext = os.path.splitext(items[pos])[1]
						player = vidext[ext.lower()]
						if player == 'mplayer':
							video = os.path.join(cwd, items[pos])
							launch_mplayer(['-slang', 'sl,en', '-subcp', 'enca:si:cp1250', '-unicode', '-cache', '8192', \
											'-input', 'conf=%s/etc/mplayer_input.conf' % self.config.cwd, video])
						elif player == 'vlc':
							ladunch_vlc(['--config', '%s/etc/vlc_video.conf' % self.config.cwd, video, 'vlc://quit'])
						elif player == 'mplayer-x264':
							video = os.path.join(cwd, items[pos])
							launch_mplayer(['-slang', 'sl,en', '-subcp', 'enca:si:cp1250', '-unicode', '-cache', '8192', '-vfm', 'ffmpeg', '-lavdopts', 'lowres=2:fast:skiploopfilter=all:threads=8', \
                                            '-input', 'conf=%s/etc/mplayer_input.conf' % self.config.cwd, video])

                # draw menu
                draw_video_menu(place, marker)
                pygame.display.flip()

        return True
