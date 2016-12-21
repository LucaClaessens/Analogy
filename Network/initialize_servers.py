import time
import BaseHTTPServer
import subprocess
import urlparse
from pprint import pprint
import webbrowser as wb
from ConfigParser import SafeConfigParser

#set up the hostname and port number for the server to listen at
HOST_NAME = 'luca.local'
PORT_NUMBER = 8880
START_MAMP = True

#server handler
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_HEAD(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
        #our web interface sends post requests, handle these
        def do_POST(s):
                """Respond to a POST request."""
                # Extract and print the contents of the POST
                length = int(s.headers['Content-Length'])
                post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
                for key, value in post_data.iteritems():

                        print 'key {}, value {}'.format(key,value[0])
                        cmd = "python model_to_DB.py"
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
        # Start MAMP if configured
        if START_MAMP:
                subprocess.call('open /Applications/MAMP/MAMP.app/', shell=True)
                wb.get('chrome %s').open_new_tab('http://localhost:8888/Editing/selection.html')

        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        try:
                httpd.serve_forever()
        # Handle keyboard interrupts
        except KeyboardInterrupt:
                pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)