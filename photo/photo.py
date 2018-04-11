import pygame
from pygame.locals import *
import os
from utils import *
import EXIF


class Photo_Menu:

    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def preprocess(self, image_file):
        # read EXIF data
        f = open(image_file, 'rb')
        exifdata = EXIF.process_file(f, stop_tag = 'Orientation')
        f.close()
        
        # load image
        image = pygame.image.load(image_file)     
       
        # get image orientation
        if 'Image Orientation' in exifdata.keys():
            orientation = exifdata['Image Orientation'].printable
            # rotate image if necessary
            if orientation == 'Rotated 90 CW':
                image = pygame.transform.rotate(image, -90)
            elif orientation == 'Rotated 90 CCW':
                image = pygame.transform.rotate(image, 90)
            elif orientation == 'Rotated 180':
                image = pygame.transform.rotate(image, 180)
        
        # get image dimensions
        w, h = image.get_size()
        scale = float(w) / h
        
        # scale to fit screen
        flag = 0
        if w >= h:
            w = self.config.dimx
            h = int(w // scale)
            flag = 1
        if h >= w:
            h = self.config.dimy
            w = int(h * scale)
            flag = 1
        if flag:
            return pygame.transform.scale(image, (w,h))
        else:
            return image

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
        photo_path = os.path.normpath(self.config.playlist_photo)

        def slideshow(cwd, items, startpos):
            # get current screen
            screen = pygame.display.get_surface()

            # count subdirectories
            ndir = 0
            while os.path.isdir(os.path.join(cwd, items[ndir])):
                ndir += 1

            # number of items (first entry is "..")
            minpos = ndir
            maxpos = len(items) - 1

            # show first photo
            image_c = self.preprocess(os.path.join(cwd, items[startpos]))
            dim = image_c.get_size()
            off = ((self.config.dimx - dim[0])/2, (self.config.dimy - dim[1])/2)
            screen.fill((0, 0, 0))
            screen.blit(image_c, off)
            pygame.display.flip()

            # cache next and previous photo
            next = startpos + 1
            if next > maxpos:
                next = minpos
            prev = startpos - 1
            if prev < minpos:
                prev = maxpos
            image_p = self.preprocess(os.path.join(cwd, items[prev]))
            image_n = self.preprocess(os.path.join(cwd, items[next]))

            # set up timer event
            pygame.time.set_timer(USEREVENT + 1, 5000)

            # main loop
            direction = 1
            while 1:
                # process events
                e = pygame.event.wait()
                if e.type == QUIT:
                    exit()
                # any key pressed?
                elif e.type == KEYDOWN:
                    # reset timer
                    pygame.time.set_timer(USEREVENT + 1, 0)
                    pygame.time.set_timer(USEREVENT + 1, 5000)
                    # DOWN ARROW or N
                    if (e.key == K_DOWN or e.key == K_n):
                        direction = 1
                    # UP ARROW or P
                    elif (e.key == K_UP or e.key == K_p):
                        direction = -1
                    # ENTER
                    elif e.key == K_RETURN or e.key == K_ESCAPE:
                        # exit photo mode?
                        break
                            
                # move image cache window
                if direction == 1:
                    image_p = image_c
                    image_c = image_n
                    next += 1
                    if next > maxpos:
                        next = minpos
                    prev += 1
                    if prev > maxpos:
                        prev = minpos
                else:
                    image_n = image_c
                    image_c = image_p
                    prev -= 1
                    if prev < minpos:
                        prev = maxpos
                    next -= 1
                    if next < minpos:
                        next = maxpos

                # show photo
                dim = image_c.get_size()
                off = ((self.config.dimx - dim[0])/2, (self.config.dimy - dim[1])/2)
                screen.fill((0, 0, 0))
                screen.blit(image_c, off)
                pygame.display.flip()

                # next image caching
                if direction == 1:
                    image_n = self.preprocess(os.path.join(cwd, items[next]))
                else:
                    image_p = self.preprocess(os.path.join(cwd, items[prev]))
            
            # unset timer event
            pygame.time.set_timer(USEREVENT + 1, 0)


        def draw_photo_menu(place, marker):
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

        # a list of valid photo extensions
        vidext = ['.jpg', '.jpeg']

        # get top directory items
        cwd = photo_path
        items = list_dir(cwd, vidext)
        # top directory does not exist
        if items is None:
            return True

        # main loop
        maxpos = len(items)
        pos, place, marker = 0, 0, 0
        draw_photo_menu(place, marker)
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
                    # exit photo mode?
                    if cwd == photo_path and pos == 0:
                        break
                    # is it a directory?
                    elif os.path.isdir(os.path.join(cwd, items[pos])):
                        cwd = os.path.normpath(os.path.join(cwd, items[pos]))
                        items = list_dir(cwd, vidext)
                        maxpos = len(items)
                        pos, place, marker = 0, 0, 0
                    # start viewing images
                    else:
                        slideshow(cwd, items, pos)
                        pos = 0
                        place = 0
                        marker = 0

                # draw menu
                draw_photo_menu(place, marker)
                pygame.display.flip()

        return True
