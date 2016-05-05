import os, sys, httplib

def download(host, port, filepath):
    conn = httplib.HTTPConnection(host, port)
    conn.request("GET", "/"+filepath)

    fp = open(filepath, 'wb')

    resp =conn.getresponse()

    #read 4096 bytes at a time
    block_size = 4096
    buffer = resp.read(block_size)
    while(buffer):
        fp.write(buffer)
        buffer = resp.read(block_size)
    
    fp.close()
    conn.close()
    
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
