from utils import *


class TV_Menu:

    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def start(self):
        ret = launch_vlc(['--config', 'etc/vlc_tv.conf', '--miface-addr', '84.255.194.127',\
                          'playlists/%s' % self.config.playlist_tv])
        return ret
