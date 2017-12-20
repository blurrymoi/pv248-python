import http.client
from http.server import *
import urllib.parse
from subprocess import call
import sys

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        ''' gets called @ request of type GET '''
        # pass a CLASS (not instance) to HTTPServer
        # request data available in instance variables self.path, self.headers
        self.send_response(200, 'OK')
        d = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        print(d)
        header = 'text/html' if 'html' in d['f'] else 'application/json'

        self.send_header('Content-Type', '%s' % header)
        self.end_headers()
        q = [x[-1] for x in d['q'] if x.startswith('search')][0]
        print(q)

        html = ''' <!DOCTYPE html><html><body>
            <h2> Result for q</h2>
            <ul style="list-style-type:circle">'''
#        for item in call(["python3", "search.py", q], stdout=fil):

        if 'f' in d and 'json' in d['f']:
            call(["python3", "search.py", q], stdout=self.wfile)
        elif 'f' in d and 'html' in d['f']:
            self.wfile.write(bytes(html, 'utf-8'))
            #call(["python3", "search.py", q], stdout=self.wfile)

        # self.wfile.write(bytes("{} faktorial".format(self.path[1:]), 'utf-8'))
        # sockets only accept byte sequences, not str

# something about html webform


def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
