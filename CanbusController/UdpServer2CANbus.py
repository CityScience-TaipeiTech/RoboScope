#!/usr/bin/python3
import argparse
import socket
import json
# import can

def arg_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, help="UDP source ip address", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, help="UDP receiving port on this machine", default=5005)
    parser.add_argument("-c", "--can", type=str, help="CAN bus interface on this machine", default="")
    return parser.parse_args()

def udp_socket_init(ip, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print("UDP server starts receiving data at port ", port)
    return sock

def udp_socket_receive(sock):
    while True:
        recieved = sock.recvfrom(1024)
        json_obj = json.loads(recieved[0])
        print(json_obj)

def main():
    args = arg_init()
    sock = udp_socket_init(args.ip, args.port)
    udp_socket_receive(sock)
    return 0

if __name__ == '__main__':
    main()