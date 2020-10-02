#!/usr/bin/python3
# author: Rui z000000
# Lab2 Q5 样例代码

import sys
import socket, datetime


def ping(host='127.0.0.1', port=8800):
    # init 
    rtt_lst = []
    packet_lost = 0

    # 格式化地址和端口
    address = (host, port)
    # 实例化socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 发送10个包
    for i in range(10):
        # 计算时间(发送消息的时间, 记录为t1)
        t1 = datetime.datetime.now()
        # PING sequence_number time CRLF
        msg = f"PING {i} {t1}\r\n"  # 消息的格式: "PING 包的序号 时间"
        # 调用socket的sendto功能, 发送msg到指定地址
        sock.sendto(msg.encode(), address)

        try:
            sock.settimeout(1)  # 超时时间 = 1s
            data = sock.recv(1024)  # 接受回应(等待回应)
            t2 = datetime.datetime.now()  # 计算时间(接受到消息的时间, 记录为t2)
            rtt = (t2 - t1).total_seconds() * 1000  # 计算时间: 消息来回的RTT = (t1-t2)
            rtt_lst.append(rtt)
            print(f"ping to {host}, seq = {i}, rtt = {rtt} ms")

        except socket.timeout:
            # 如果超时了
            packet_lost += 1
            print(f"ping to {host}, seq = {i}, rtt = time out")

    # report
    print(f"Packets: Sent = 10, Lost = {packet_lost} ( {packet_lost / 10 * 100}% loss)")
    print("Approximate round trip times in milli-seconds:")
    print("\tMinimum = {}ms, Maximum = {}ms, Average = {}ms".format(min(rtt_lst), max(rtt_lst),
                                                                    sum(rtt_lst) / len(rtt_lst)))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 PingClient.py host port")
    else:
        ping(sys.argv[1], int(sys.argv[2]))
