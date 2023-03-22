#!/usr/bin/python3
import argparse
import socket
import json

def get_json_fromfile(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def arg_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, help="UDP source ip address", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, help="UDP receiving port on this machine", default=5005)
    parser.add_argument("-f", "--file", type=str, help="Json file to send via UDP", default="./grasshopper_output.json")
    return parser.parse_args()

def udp_socket_init():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return sock


def main():
    args = arg_init()
    send_msg = get_json_fromfile(args.file)
    send_msg_str = json.dumps(send_msg)
    print("Sending message: ", json.dumps(send_msg, sort_keys=True, indent=4))
    sock = udp_socket_init()
    sock.sendto(send_msg_str.encode(),(args.ip, args.port))
    print("SENT to --> ", args.ip, " at port ", args.port)
    return 0

if __name__ == '__main__':
    main()