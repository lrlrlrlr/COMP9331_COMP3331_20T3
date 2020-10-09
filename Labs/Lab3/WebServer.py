import socket, threading, time, re, os, sys


def tcplink(sock, addr):
    print("Accept new conn from %s:%s..." % addr)

    while True:
        data = sock.recv(1024)  # 服务器尝试监听端口
        time.sleep(1)
        if data:  # 如果我们的服务器收到了任何request, 则根据它请求的东西作出相应的回应

            # split the request from client
            request = data.decode().split('\n')

            # if get
            if "GET" in request[0]:
                try:
                    file = re.search(r'GET /(.*) HTTP', request[0]).group(1)
                except AttributeError:

                    # cant parse the file path, return 404
                    sock.send("\nHTTP/1.1 404 Not Found\n\n".encode())

                # return the content of file
                # if the file is in directory
                if os.path.exists(file):
                    with open(file, 'rb') as f:
                        content = f.read()
                    sock.send("\nHTTP/1.1 200 OK\n\n".encode())
                    sock.sendall(content)


                else:
                    sock.send("\nHTTP/1.1 404 Not Found\n\n".encode())
                    sock.send("404 Not Found".encode())
                sock.close()
                break

        else:
            break
    sock.close()
    print("Conn from %s:%s closed." % addr)


if __name__ == '__main__':
    if sys.argv[1]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 实例化socket

        s.bind(('127.0.0.1', int(sys.argv[1])))  # 监听地址 127.0.0.1:{端口号}
        s.listen(5)
        print("wait for conn...")

        while True:
            sock, addr = s.accept()
            t = threading.Thread(target=tcplink, args=(sock, addr))  # 多线程
            t.start()
