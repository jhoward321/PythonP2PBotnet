# P2P Botnet

This project is a proof of concept P2P botnet written in Python. It was a final project for CS460 at the University of Illinois at Urbana-Champaign for the Spring 2016 semester. The main idea behind the project was to design a botnet architecture that was not only resistant to targeted takedown attempts, but also protected the identity of the botnet owner. This was accomplished by using a Kademlia DHT. Upon joining the network, bots query a specific hash in the DHT, post their unique ID, and then wait for an acknowledgement from a commander. A commander will constantly check the login location for new bots, and send out ACKs when new bots join the network. Commands are sent via specific query locations that are unique to each bot. Since every bot has a unique command location, its easy to send commands to individual clients while still being easy to send global commands to all clients. The commander never has direct contact with a bot, all communication is performed through DHT queries. This protects the commander from being compromised by a rogue client. This is just a proof of concept, but more features such as digitally signed commands could easily be added for additional security. 


botnet.py spawns a p2p node that will communicate with other nodes. Using python kademlia library

keylogger.py - takes in an argument for a logging directory and will create log files in that folder. Each log file will be named based off the window that key was recording from. This makes it easier to interprete what program was using what keystrokes.

ddos.py - Takes in two arguments (hostname and port) and will establish 4 connections to the target in seperate threads. Each connection will then spam 1 million GET requests to the target address in an attempt to overload the server.

upload.py
Use: python upload.py [host] [port] [filepath]
Requires requests library. Can be installed from: pip install requests
Uploads the file at filepath to target server using multipart/form-data Post request

download.py
Use: python download.py [host] [port] [filepath]
GET requests file from target server

fileserver.py
Use: python fileserver.py [port]
Simple HTTPServer to handle GET/download requests and POST/upload requests. GET requests pull files from the filehost directory. Upload request files get stored in /filedump/[client_ip] directory.
