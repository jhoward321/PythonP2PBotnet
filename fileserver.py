from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import cgi, sys, os, threading

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #Handle GET Request
        try:
            filepath = "filehost"+self.path
            print "Filepath: "+filepath
            f=open(filepath, "rb")

            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(f.read())
            f.close
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        #Handle POST Request - File Uploads

        try:
            #Use cgi form to parse post request
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
            filename = form['file'].filename
            data = form['file'].file.read()

            #store files in /filedump/<client-ip> directory
            client = self.client_address[0]
            dirpath = "filedump/"+client
            if not os.path.isdir(dirpath):
                os.makedirs(dirpath)

            f = open(dirpath+"/"+filename, "wb")
            f.write(data)
            self.send_response(200)
            f.close()
            return
        except IOError:
            self.send_error(500,'Internal Server Error: Upload Failed')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a seperate thread."""

def launchServer(port):
    try:
        server = ThreadedHTTPServer(('',port), RequestHandler)
        print "Starting file server"
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down server"
        server.socket.close()

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    port = int(sys.argv[1])
    launchServer(port)    

if __name__ == '__main__':
    main()
