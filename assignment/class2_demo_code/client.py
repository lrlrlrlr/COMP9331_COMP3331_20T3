import json
import os
import sys
import threading
import time
from socket import *


class Client:
    def __init__(self, serverPort=12000):
        '''
        这是client的主程序
        逻辑是:
            1. 连接上服务器
            2. 验证username 和 密码
            3. 发送消息
            4. ....
        :param serverPort: 服务器的端口号
        '''

        print("Client is running...")
        serverName = 'localhost'
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((serverName, serverPort))

        # 建立一个线程来监听所有收到的信息
        t = threading.Thread(target=self.listen)
        t.start()

        login = False
        # while not login:
        #     # todo 登录
        #         # 发送username
        #     self.sock.send(username) #
        #         # 发送password
        #     self.sock.recv(1024) # 服务端传回来的username验证结果
        #     if ...:
        #
        #     self.sock.send(psw)
        #     self.sock.recv(1024)  # 服务端传回来的psw验证结果
        #     if ...:
        #         # 验证成功
        #         # 验证失败了

        # 主线程持续处理用户输入的信息
        client_status = True
        while client_status:
            client_status = CMDHandler(self.sock).status
            time.sleep(0.5)

        self.sock.close()
        sys.exit(0)

    def listen(self):
        '''
        监听所有的消息
        :return: None
        '''
        # 监听所有收到的消息, 并打印出来
        while True:
            try:
                msg = self.sock.recv(1024)
                if msg:
                    print(msg.decode())

                if 'download' in msg.decode() and 'filecontent' in msg.decode():
                    # 保存文件
                    filename = json.loads(msg.decode()).get('data').get('filename')
                    filecontent = json.loads(msg.decode()).get('data').get('filecontent')
                    CMDHandler.save_file(filename, filecontent)
                    print(msg.decode())
                    print(f'file {filename} saved!')
            except Exception as e:
                print(f'An Error {e} occur with msg: ', msg.decode())
                sys.exit(0)


class CMDHandler:
    # 用来处理你的命令
    def __init__(self, sock):
        self.status = True
        cmd = input("What do you want to send:")
        # sock.send(cmd.encode())
        print('send', cmd, 'to server!')

        # 当你输入的命令是logout, 则登出
        if cmd == 'logout':
            print("Actively close.")
            self.status = False

        elif 'sendfile' in cmd:
            # 当用户输入指令 sendfile filename的时候, 发送文件
            filename = cmd.split(' ')[1]
            if filename not in os.listdir():
                print(f'Filename {filename} not exist!')
            else:
                msg = json.dumps({'type': 'sendfile', 'data': self.read_files(filename)})
                sock.send(msg.encode())

        elif 'download' in cmd:
            filename = cmd.split(' ')[1]
            msg = json.dumps({'type': 'download', 'data': {'filename': filename}})
            sock.send(msg.encode())



        # 当你输入的命令是登录...
        # elif cmd == 'login':
        #     do_something()
        # 当你输入的命令是xxx.....
        else:
            msg = cmd
            sock.send(msg.encode())

    def read_files(self, filename: str) -> dict:
        with open(filename, 'r') as file:
            data = file.read()
        return {'filename': filename, 'filecontent': data}

    @staticmethod
    def save_file(filename, fs):
        if not os.path.exists('recv_client'):
            os.mkdir('recv_client')
        with open('recv_client\\' + filename, 'w+') as file:
            file.write(fs)


def example(attr1: int, attr2: str) -> dict:
    '''
    描述你的函数逻辑
        1. 第一步干嘛
        2. 第二步干嘛
        3. 第三步干嘛
    :param attr1: 描述这个参数的类型/意义
    :param attr2: 描述这个参数的类型/意义
    :return: 返回的东西是怎么样的
    '''
    return dict({attr1: attr2})


if __name__ == '__main__':
    c = Client()

    # import doctest
    # doctest.testmod()
