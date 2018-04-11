import os
import pygame


class Theme:

    def __init__(self, config):
        self.cfg = config

        # theme fonts
        self.font = pygame.font.Font(self.cfg.font, self.cfg.fontsize)
        self.font2 = pygame.font.Font(self.cfg.font2, self.cfg.fontsize)

        # theme images
        theme_path = os.path.join('themes', self.cfg.theme)
        self.background_image = pygame.image.load(os.path.join(theme_path, 'back.jpg')).convert()
        self.menu_image = [pygame.image.load(os.path.join(theme_path, 'tv.png')).convert_alpha(),
                           pygame.image.load(os.path.join(theme_path, 'video.png')).convert_alpha(),
                           pygame.image.load(os.path.join(theme_path, 'dvd.png')).convert_alpha(),
                           pygame.image.load(os.path.join(theme_path, 'music.png')).convert_alpha(),
                           pygame.image.load(os.path.join(theme_path, 'photo.png')).convert_alpha(),
                           pygame.image.load(os.path.join(theme_path, 'gold.png')).convert_alpha(),
                           pygame.image.load(os.path.join(theme_path, 'quit.png')).convert_alpha()]
        self.remote_image = pygame.image.load(os.path.join(theme_path, 'remote.png')).convert_alpha()


