import os, sys, socket

def sendGETrequest(sock, host, filepath):
    sock.send("GET /"+filepath+" HTTP/1.1\r\nHost: " + host + "\r\n\r\n")

def download(host, port, filepath):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
   
    sendGETrequest(sock, host, filepath)

    fp = open(filepath, 'wb')
    
    line = sock.recv(1024)
    while(line)
        fp.write(line)
        line = sock.recv(1024)
    fp.close()
    sock.close()
    
#use: python download.py [host] [port] [filepath]
def main():
    if len(sys.argv) != 4:
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]
    download(host, port, filepath)

if __name__ == '__main__':
    main()
