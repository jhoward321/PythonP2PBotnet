from twisted.application import service, internet
from twisted.python.log import ILogObserver
from twisted.internet import reactor, task

import sys, os
sys.path.append(os.path.dirname(__file__))
from kademlia.network import Server
from kademlia import log

application = service.Application("kademlia")
application.setComponent(ILogObserver, log.FileLogObserver(sys.stdout, log.INFO).emit)

if os.path.isfile('cache.pickle2'):
    kserver = Server.loadState('cache.pickle2')
else:
    kserver = Server()
    kserver.bootstrap([("192.168.56.101", 8468)])
kserver.saveStateRegularly('cache.pickle2', 10)

server = internet.UDPServer(8468, kserver.protocol)
server.setServiceParent(application)
