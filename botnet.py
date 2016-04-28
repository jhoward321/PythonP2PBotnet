import hashlib
import sys
from twisted.internet import reactor
from twisted.python import log
#import kademlia
import time
import keylogger
from kademlia.network import Server

log.startLogging(sys.stdout)

#best way to initialize is grab the neighbor's finger table and update as needed
#finger table will contain both the id of a neighbor along with its IP, port?
# Class FingerTable(object):
# 	def _init_(self,m,):
# Class Address(object):
# 	def _init_(self, ip, port):
# 		self.ip = ip
# 		self.port = port
# Class Node(object):
# 	def _init_(self, key, ip, port, predecessor, successor, routing_table):
# 		self.key = key
# 		self.predecessor = predecessor
# 		self.successor = successor
# 		self.ip = ip
# 		self.port = port

#use linked list for chord circle 
#for routing: name will be key, value will be object with ip, port
#might switch touting implementation from chord to kademlia for ease of use
#but kademelia has a lot of the same ideas

def get_hash(ip, port):
	m = hashlib.sha1()
	m.update(ip)
	m.update(port)
	print m.hexdigest()
	return m

def done(result):
    print "Key result:", result
    reactor.stop()

def setDone(result, server):
    server.get("a key").addCallback(done)

def bootstrapDone(found, server):
    server.set("Loser", "Braves").addCallback(setDone, server)

now = time.time()
done = lambda: time.time() > now + 60
def print_keys(t, modifiers, keys): print "%.2f   %r   %r" % (t, keys, modifiers)

keylogger.log(done, print_keys)
#server = Server()
#server.listen(8469)
#server.bootstrap([("192.168.56.101", 8468)]).addCallback(bootstrapDone, server)

#reactor.run()