import http.client
from http.server import *
import ssl  # SSL/TLS wrapper


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        ''' gets called @ request of type GET '''
        # pass a CLASS (not instance) to HTTPServer
        # request data available in instance variables self.path, self.headers
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("{} faktorial".format(self.path[1:]), 'utf-8'))
        # sockets only accept byte sequences, not str


def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
