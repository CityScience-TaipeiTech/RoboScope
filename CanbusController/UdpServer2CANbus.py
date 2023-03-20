#!/usr/bin/python3
import datetime
import argparse
import socket
import json
import can

def arg_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, help="UDP source ip address", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, help="UDP receiving port on this machine", default=5005)
    parser.add_argument("-c", "--can", type=str, help="CAN bus interface on this machine", default="vcan0")
    return parser.parse_args()

def udp_socket_init(ip, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print("UDP server starts receiving data at port ", port)
    return sock

def udp_socket_receive(sock, can_interface=None):
    while True:
        recieved = sock.recvfrom(1024)
        try:
            json_obj = json.loads(recieved[0])
        except ValueError as e:
            print(e)
            print("[", datetime.datetime.now(), "] Json loads failed, please make sure you json format is correct")
            print("received raw data: ",  recieved[0])
            return
        # print("[", datetime.datetime.now(), "] ", json_obj)
        
        if(can_interface == None):

            print("[", datetime.datetime.now(), "] Running in UDP test mode, and here this received UDP data: ")
            print(json_obj)
        else:
            print("[", datetime.datetime.now(), "] ", "Received UDP data and sending out through SocketCAN...")
            can_send_msg(can_interface, json_obj)

def can_init(can_channel, bustype):
    try:
        bus = can.Bus(channel=can_channel, interface=bustype)
        return bus
    except OSError as e:
        print(e)
        print("Can not open", can_channel)
        return None

def can_send_msg(can_interface, msg):
    offset = 10
    for cell in msg["data"]:
        # Row-major order
        pos = cell["position"]
        h = cell["height"]*10
        id = 4*pos["y"]+pos["x"] + offset
        msg = can.Message(arbitration_id=id, data=[0xff, h, 0, 0], is_extended_id=False)
        can_interface.send(msg)

def main():
    args = arg_init()
    sock = udp_socket_init(args.ip, args.port)
    can_interface = can_init(args.can, "socketcan")    
    udp_socket_receive(sock, can_interface)
    return 0

if __name__ == '__main__':
    main()