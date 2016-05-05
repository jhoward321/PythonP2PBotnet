import os, sys, socket

def upload(host, port, filepath):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    fp = open(filepath, 'rb')
    line = fp.read(1024)
    while(line):
        sock.send(line)
        line = fp.read(1024)
    sock.close()
    
#use: python upload.py [host] [port] [filepath]
def main():
    if len(sys.argv) != 4:
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]
    upload(host, port, filepath)

if __name__ == '__main__':
    main();
