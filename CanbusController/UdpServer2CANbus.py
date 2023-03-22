#!/usr/bin/python3
import datetime
import argparse
import socket
import threading
import json
import can

def arg_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, help="UDP server ip address", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, help="UDP server receiving port on this machine", default=5005)
    parser.add_argument("-gi", "--gip", type=str, help="UDP client destination ip address", default="127.0.0.2")
    parser.add_argument("-gp", "--gport", type=int, help="UDP client destination  port on this machine", default=5005)
    parser.add_argument("-c", "--can", type=str, help="CAN bus interface on this machine", default="vcan0")
    return parser.parse_args()

def udp_server_init(ip, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print("UDP server starts receiving data at port ", port)
    return sock

def udp_sender_init():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return sock

def udp_socket_receiver(sock, can_interface=None):
    while True:
        recieved = sock.recvfrom(1024)
        try:
            json_obj = json.loads(recieved[0])
        except ValueError as e:
            print(e)
            print(f"[{datetime.datetime.now()}] Json loads failed, please make sure you json format is correct")
            print("received raw data: ",  recieved[0])
            return        
        if(can_interface == None):
            print(f"[{datetime.datetime.now()}] Running in UDP test mode, and here this received UDP data: ")
            print(json_obj)
        else:
            print(f"[{datetime.datetime.now()}] Received UDP data and sending out through SocketCAN...")
            can_send_msg(can_interface, json_obj)

def udp_send(udp_client, data):
    print(f"[{datetime.datetime.now()}] Received {len(data)} CAN data and sending out through UDP...")
    data_to_send = {
        "data":[]
    }
    for id, d in data.items():
        obj = {"position": {"x": id % 4, "y": int(id/4)}, "height": d[1]}
        data_to_send["data"].append(obj)
    data_to_send_str = json.dumps(data_to_send)
    # print(data_to_send_str)
    udp_client["sock"].sendto(data_to_send_str.encode(),(udp_client["ip"], udp_client["port"]))

def can_receiver(udp_client, can_interface=None):
    if can_interface is None:
        print("Can bus not found!")
        return
    data = {}
    while True:
        message = can_interface.recv(0.1)
        if message is None:
            if not len(data) == 0:
                udp_send(udp_client, data)
                data.clear()
            continue
        if not message.dlc == 4:
            continue
        data[message.arbitration_id] = message.data
    
def can_init(can_channel, bustype):
    try:
        bus = can.Bus(channel=can_channel, interface=bustype)
        bus.set_filters([{"can_id": 0x000, "can_mask": 0xF00, "extended": False}])
        return bus
    except OSError as e:
        print(e)
        print("Can not open", can_channel)
        return None

def can_send_msg(can_interface, msg):
    offset = 0x100
    for cell in msg["data"]:
        # Row-major order
        pos = cell["position"]
        h = cell["height"]*10
        id = 4*pos["y"]+pos["x"] + offset
        msg = can.Message(arbitration_id=id, data=[0xff, h, 0, 0], is_extended_id=False)
        can_interface.send(msg)

def main():
    threads = list()
    args = arg_init()
    udp_server = udp_server_init(args.ip, args.port)
    udp_client = {}
    udp_client["sock"] = udp_sender_init()
    udp_client["ip"] = args.gip
    udp_client["port"] = args.gport
    can_interface = can_init(args.can, "socketcan")    
    # udp_socket_receive(sock, can_interface)
    udp2can_thread = threading.Thread(target=udp_socket_receiver, args=(udp_server,can_interface))
    threads.append(udp2can_thread)
    print("Starting UDP to CAN bus thread...")
    udp2can_thread.start()
    # can_receive(can_interface)
    can2udp_thread = threading.Thread(target=can_receiver, args=(udp_client, can_interface))
    threads.append(can2udp_thread)
    print("Starting CAN to UDP thread...")
    can2udp_thread.start()
    return 0

if __name__ == '__main__':
    main()