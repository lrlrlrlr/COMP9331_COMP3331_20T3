import threading, json
from socket import *
import os
from collections import defaultdict
import re

online_user = []


class Server:
    def __init__(self):
        # init the data
        self.threads = defaultdict(list)
        # {'threadtitle1': ['msg1', 'msg2', 'msg3']}

        print("server started")
        serverPort = 12000
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('localhost', serverPort))
        serverSocket.listen()
        print("The server is ready to receive")

        while True:
            sock, addr = serverSocket.accept()
            # 多线程接待
            print(f"Connection established: {addr}")
            t = threading.Thread(target=self.tcplink, args=(sock, addr))
            t.start()

    def tcplink(self, sock, addr):
        '''
        给每个连进来的客户端分别分配一个线程
        :param sock:
        :param addr:
        :return:
        '''
        # todo input method
        # 接受username并验证
        # while not login:
        #     msg = sock.recv(1024)
        #     username = msg.decode() ....
        #     if is_exist(username):
        #         .....
        #         # 接受psw并验证
        #         msg = sock.recv(1024)
        #         psw = msg.decode()....
        #         if verify(username,psw):
        #             login = True
        #
        #     else:
        #         # 用户不存在, 新建用户
        #         create_user(...)
        #         ....

        login = True

        try:
            while login:
                msg = sock.recv(1024)
                if msg:
                    print(msg.decode())

                    # give feedback to client
                    sock.send(f'Server have recvieved you msg: {msg.decode()}'.encode())

                    # 当客户端来的信息是logout, 则登出
                    if re.match('logout', msg.decode()):
                        login = False
                    # 当客户端来的信息是..., 则...
                    # todo elif msg.decode() == 'XXX':
                    #     DO_SOMETHING()

                    elif 'sendfile' in msg.decode():
                        filename = json.loads(msg.decode()).get('data').get('filename')
                        filecontent = json.loads(msg.decode()).get('data').get('filecontent')
                        savefile(filename, filecontent)
                        print(f'file {filename} saved!')

                    elif 'download' in msg.decode():
                        filename = json.loads(msg.decode()).get('data').get('filename')
                        filecontent = loadfile(filename)
                        data = json.dumps(
                            {'type': 'download', 'data': {'filename': filename, 'filecontent': filecontent}})
                        sock.send(data.encode())
                        print(f'file {filename} sent!')

        except Exception as e:
            if e is not ConnectionResetError:
                print(e)
            print(f"Connection {addr} closed!")

        finally:
            sock.close()


# I/O
def load_users():
    '''

    :return:
    '''
    r = []
    with open('credentials.txt', 'r') as file:
        for row in file.readlines():
            username, psw = row.strip('\n').split(' ')
            r.append((username, psw))
    return r


def verify(username, psw):
    return (username, psw) in load_users()


def is_exist(username):
    return any(username in tup for tup in load_users())


def create_user(username, password):
    with open('credentials.txt', 'a') as file:
        file.write(f"\n{username} {password}")


def savefile(filename, fs):
    recv_path = 'recv_server'
    if not os.path.exists(recv_path):
        os.mkdir(recv_path)
    with open(recv_path + '\\' + filename, 'w+') as file:
        file.write(fs)


def loadfile(filename) -> str:
    with open('recv_server\\' + filename, 'r') as file:
        return file.read()


def json_to_file(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def file_to_json():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    s = Server()
