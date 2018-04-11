import subprocess
import os
import string


def exec_external_app(app, args = []):

    command = [app] + args
    ret = subprocess.call(command)
    return ret


def list_dir(cwd, extensions):

    try:
        items = os.listdir(cwd)
    except:
        return None

    # split items into files and directories
    items_d = [f for f in items if os.path.isdir(os.path.join(cwd, f))]
    items_f = [f for f in items if string.lower(os.path.splitext(f)[1]) in extensions]
    
    # sort by name
    items_d.sort()
    items_f.sort()

    # build list
    fitems = ['..']
    fitems.extend(items_d)
    fitems.extend(items_f)

    # return directories and video files
    return fitems


def launch_vlc(args):

    defargs = ['-v'] #['--quiet']
    ret = exec_external_app('/usr/bin/vlc', defargs + args)
    return ret


def launch_mplayer(args):

    defargs = ['-fs', '-quiet', '-slave', '-ao', 'alsa', '-stop-xscreensaver']
    ret = exec_external_app('/usr/bin/mplayer', defargs + args)
    return ret


def set_cursor(cursor = None):
	
    if cursor is None: 
        # default
        subprocess.Popen('/usr/bin/xsetroot -solid black -cursor_name left_ptr', shell = True) 
    else:
    	subprocess.Popen('/usr/bin/xsetroot -solid black -cursor %s %s' % (cursor, cursor), shell = True)


def shutdown():
    
    exec_external_app('sudo', ['/sbin/shutdown', '-h', 'now'])

