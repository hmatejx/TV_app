from utils import *

class Music_Menu:

    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def start(self):
        #set_cursor()
        #ret = exec_external_app('/usr/bin/rhythmbox')
        #set_cursor('%s/etc/empty.cursor' % self.config.cwd)
        #return True

        ret = launch_vlc(['--config', 'etc/vlc_tv.conf', '--miface-addr',\
                          '84.255.194.127', 'playlists/%s' % self.config.playlist_radio])
        return ret
