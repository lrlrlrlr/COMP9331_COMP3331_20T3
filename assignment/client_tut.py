from socket import *


clientSocket = socket(AF_INET, SOCK_DGRAM)
while True:
    message = input("input your command: ")
    clientSocket.sendto(message.encode(),('127.0.0.1', 12000))
    msg = clientSocket.recv(1024)
    if msg:
        print(msg.decode())


