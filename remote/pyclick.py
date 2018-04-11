import os
import sys
import time
import select
import subprocess
from pygame import mixer


# the characters associated with each button
# you probably won't have to edit these
PLAY = 1
PREV = 16
NEXT = 8
VOLDOWN = 4
VOLUP = 2


# you can edit these strings to change what command
# is run when each button is pressed
commands = {}
commands[PLAY] =    "/usr/bin/xte 'key Escape'"
commands[PREV] =    "/usr/bin/xte 'key p'"
commands[NEXT] =    "/usr/bin/xte 'key n'"
commands[VOLDOWN] = "/usr/bin/xte 'key Down'"
commands[VOLUP] =   "/usr/bin/xte 'key Up'"


# device filename
hidfilename = "/dev/usb/hiddev0"


# debug mode (0 = off, 1 = basic, 2 = verbose)
DEBUG = 0
    

# class for airclick usb remote
class AirClick:

    def __init__(self, hidfilename):
        self.event_size, self.key_offset = 64, 31
        self.time_threshold = 0.1
        self.repeat_threshold = 0.2
        self.count, self.zcount, self.kcount = 0, 0, 0
        self.activekey = 0
        self.blocked = 0
        self.repeat = 0
        self.start_time = 0
        self.hidfile = os.open(hidfilename, os.O_RDONLY)
        self.sound = mixer.Sound("remote/Tock.wav")

    def click(self):
        self.sound.play()

    def display(self, string):
        for i in range(0, len(string)):
            if i % self.event_size == 0:
                print 'event %d: count %3d (zero %3d, key %3d) -------------------------' % \
                      (i/self.event_size + 1, self.count, self.zcount, self.count - self.zcount)
            sys.stdout.write('%3s|' % ord(string[i]))
            if (i + 1) % 16 == 0:
                print ''
        print '----------------------------------------------------------------'
        return True

    def flush(self):
        rd = select.select([self.hidfile],[],[])[0]
        os.read(self.hidfile, 100*self.event_size)

    def get_event(self, flush = False):
        # flush remaining bytes
        if flush:
            self.flush()

        # read event when available
        rd = select.select([self.hidfile],[],[])[0]
        event = os.read(self.hidfile, 100*self.event_size)
        size = len(event)

        # print info
        if DEBUG:
            if size < self.event_size: print 'pyclick: short read from device (%d bytes)!' % size
            elif size > self.event_size: print 'pyclick: long read from device  (%d bytes)!' % size

        return event


    def get_key(self, flush = False):
        # get event
        event = self.get_event(flush)

        # print info
        if DEBUG == 2:
            print 'pyclick: got %d events.' % (len(event) / self.event_size)
            self.display(event)

        # determine which key was pressed, and increment counters
        key = ord(event[self.key_offset])
        self.count += 1
        if key:
            self.zcount += 1
        else:
            self.kcount += 1

        return key

    def emit(self):
        self.click()
        subprocess.Popen(commands[self.activekey], shell = True)

    def process_events(self):
        # flush for the first time
        flush = True

        # main event loop
        while 1:
            # get key
            key = self.get_key(flush)
            now = time.time()
            flush = False

            # print info
            if DEBUG:
                print 'pyclick: key = %d (last key = %d).' % (key, self.activekey)

            # valid key pressed
            if key:
                # if new key, reset and start timing
                if key != self.activekey:
                    self.activekey = key
                    self.repeat = 0
                    self.blocked = 0
                    self.start_time = now
            
                # same key still held down and can repeat
                elif self.activekey == key and not self.blocked:
                    # set time threshold
                    if self.repeat:
                        threshold = self.repeat_threshold
                    else:
                        threshold = self.time_threshold
                    # if key held long enough, emit key event
                    if (now - self.start_time) >= threshold:
                        if DEBUG:
                            print 'pyclick EMIT: %d (timer = %f s)' % (key, now - self.start_time)
                        self.emit()
                        # enable repeat or block?
                        if key == PLAY:
                            self.blocked = 1
                        else:
                            self.flush()
                            self.repeat = 1
                            # reset timer
                            self.start_time = now

            # key released to early, reset            
            elif self.activekey:
                self.activekey = 0


# MAIN
if __name__ == "__main__":
    if DEBUG:
        print 'DEBUG mode: %d.' % DEBUG
    mixer.init(48000, -16, 2)
    rc = AirClick(hidfilename)
    rc.process_events()

