from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', 12000))

while True:
    msg,client_addr = serverSocket.recvfrom(1024)
    if msg:
        print(msg.decode())
        if msg.decode() == 'login':
            serverSocket.sendto("please give me your username and password!".encode(), client_addr)

        else:
            serverSocket.sendto("unknown command!".encode(), client_addr)
