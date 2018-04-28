import http.server
import socketserver
from http.server import *
from http import cookies
import random
import string


chars = string.ascii_letters + string.digits


# C = cookies.SimpleCookie()
session_value = ''.join(random.choice(chars) for i in range(20))


class Server_Response(BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie',session_value)
        # self.send_header('Server', 'Microsoft IIS/7.5')
        self.end_headers()

    # Allow GET
    def do_GET(self):
        self.set_headers()
        # message = raw_input("Enter command :  " )
        message = raw_input("command : ")
        self.wfile.write(bytes(message))

    # Allow POST
    def do_POST(self):
        self.set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run():
    print("Server Started ..!!")
    server_address = ('', 80)
    httpd = HTTPServer(server_address, Server_Response)
    print('running server...')
    httpd.serve_forever()

run()

"""

from __builtin__ import raw_input
from scratchpad import *
import sys
import threading
def threadingConn():
    conn_thread = threading.Thread(target=sock_connect(),args=())
    conn_thread.daemon = True
    conn_thread.start()

def main():
    create_socket('', 9997)
    sock_connect()
"""
