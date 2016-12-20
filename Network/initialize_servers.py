import time
import BaseHTTPServer
import subprocess
import urlparse
from pprint import pprint
import webbrowser as wb
from ConfigParser import SafeConfigParser

HOST_NAME = 'luca.local'
PORT_NUMBER = 8880
START_MAMP = True


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_HEAD(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
        def do_GET(s):
                """Respond to a GET request."""
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.send_header("Access-Control-Allow-Origin", "*")
                s.end_headers()
                s.wfile.write("<html><head><title>ANALOGY</title></head>")
                s.wfile.write("<body><form action='.' method='POST'><input name='x' value='1' /><input type='submit' /></form><p>This is a test.</p>")
                # If someone went to "http://something.somewhere.net/foo/bar/",
                # then s.path equals "/foo/bar/".
                s.wfile.write("<p>GET: You accessed path: %s</p>" % s.path)
                s.wfile.write("</body></html>")
                #pprint (vars(s))
        def do_POST(s):
                """Respond to a POST request."""

                # Extract and print the contents of the POST
                length = int(s.headers['Content-Length'])
                post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
                for key, value in post_data.iteritems():

                        print 'key {}, value {}'.format(key,value[0])
                        cmd = "python model_to_DB.py")
                        subprocess.call(cmd, shell=True)

                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.send_header("Access-Control-Allow-Origin", "*")
                s.end_headers()
                pprint (vars(s))
                """pprint (vars(s.request))"""

if __name__ == '__main__':
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
        if START_MAMP:
                subprocess.call('open /Applications/MAMP/MAMP.app/', shell=True)
                wb.get('chrome %s').open_new_tab('http://localhost:8888/Editing/selection.html')
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)