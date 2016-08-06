* botnet.py spawns a p2p node that will communicate with other nodes. Using python kademlia library

* keylogger.py - takes in an argument for a logging directory and will create log files in that folder. Each log file will be named based off the window that key was recording from. This makes it easier to interprete what program was using what keystrokes.

* ddos.py - Takes in two arguments (hostname and port) and will establish 4 connections to the target in seperate threads. Each connection will then spam 1 million GET requests to the target address in an attempt to overload the server.

* upload.py
Use: python upload.py [host] [port] [filepath]
Requires requests library. Can be installed from: pip install requests
Uploads the file at filepath to target server using multipart/form-data Post request

* download.py
Use: python download.py [host] [port] [filepath]
GET requests file from target server

* fileserver.py
Use: python fileserver.py [port]
Simple HTTPServer to handle GET/download requests and POST/upload requests. GET requests pull files from the filehost directory. Upload request files get stored in /filedump/[client_ip] directory.