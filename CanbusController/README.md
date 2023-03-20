# CanbusController
## Hardwares
1. Raspberry Pi
2. Cando USB To CAN Module 

## UDP Testing with virtual CAN network (Linux only)
To create a virtual can interface using SocketCAN run the following:
```
sudo modprobe vcan
# Create a vcan network interface with a specific name(vcan0)
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```
