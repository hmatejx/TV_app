import sys
import os

class Config():

    def __init__(self):
        # current directory
        self.cwd = os.getcwd()

        # import user settings
        sys.path.append('etc')
        import userconfig as cfg

        # windows resolution
        self.dimx = cfg.RESOLUTION[0]
        self.dimy = cfg.RESOLUTION[1]

        # screen positions --> move to theme
        self.xm = cfg.XM
        self.ym = cfg.YM
        self.xi = cfg.XI
        self.yi = cfg.YI

        # fonts --> move to theme!
        self.font = os.path.join('fonts', cfg.FONT)
        self.font2 = os.path.join('fonts', cfg.FONT2)
        self.fontsize = cfg.FONTSIZE

        # colors --> move to theme!
        self.fontcol = cfg.FONTCOLOR
        self.fonthi = cfg.FONTHICOLOR
        self.fontbg = cfg.FONTSHADOW
        self.bgcol = cfg.BGCOLOR

        # theme
        self.theme = cfg.THEME

        # remote
        self.remote = cfg.REMOTE

        # playlists
        self.playlist_tv = cfg.PLAYLIST_TV
        self.playlist_radio = cfg.PLAYLIST_RADIO
        self.playlist_video = cfg.PLAYLIST_VIDEO
        self.playlist_photo = cfg.PLAYLIST_PHOTO

        # shutdown at exit
        self.shutdown = cfg.SHUTDOWN

        # unimport
        del cfg

