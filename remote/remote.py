import os
import subprocess
import signal

class Remote:
    
    def __init__(self):
        self.pid = -1
        self.driver = 'remote/pyclick.py'
        self.start()

    def start(self):
        if not self.pid > 0:
            self.pid = subprocess.Popen(['/usr/bin/python', '%s' % self.driver]).pid

    def kill(self):
        if self.pid > 0:
            os.kill(self.pid, signal.SIGKILL)
            os.waitpid(self.pid, os.WNOHANG)
            self.pid = -1

    def restart(self):
        self.kill()
        self.start()
