# RoboScope
## System Diagram
![image](./docs/sys-diagram.png)
## Network Configuration
### Method 1 - Connect through a Router 
- Both Grasshopper computer and Raspberry Pi connect to a router.
- Check IP address of the Raspberry Pi.
### Method 2 - Connect through Ethernet cable  
- Connect Grasshopper computer and Raspberry Pi via a Ethernet cable directly and follow the cofiguration below to set up a network:
  | Device |   IP  |  Mask | Gateway |
  |  ---   |  ---  |  ---  |   ---   |
  | Grasshopper computer | 192.168.0.2 | 255.255.255.0| 0.0.0.0|
  | Raspberry Pi | 192.168.0.1 | 255.255.255.0 | 0.0.0.0 |
## Rhino Grasshopper
### Install Plugin
1. Networking plugin: `gHowl` can be downloaded from [here](https://www.food4rhino.com/en/app/ghowl). And check [this instruction](https://www.food4rhino.com/en/faq#users-install-grasshopper-plugin) to install the plugin.

### Set up Raspberry Pi IP address on Grasshopper
Here we assume that Raspberry Pi is hosted at `10.100.2.97`

![image](./docs//Grasshopper_ip_setup.png)

## CanbusController (run at Raspberry Pi)
### Installation
``` bash
sudo apt-get install can-utils
cd CanbusController
pip3 install -r requirements.txt
```
### Quick Start
1. Plug in CANDO and start interface.
    ``` bash
    sudo ip link set can0 up type can bitrate 1000000
    ```
2. Start `UdpServer2CANbus.py` service.
    
    Here, we assume the ip of Raspberry Pi is `192.168.0.1`, and the ip address of Grasshopper computer is `192.168.0.2`
    ``` bash
    ./UdpServer2CANbus.py -i 192.168.0.1 -p 5005 -gi 192.168.0.2 -gp 5005 -c can0
    ```
3. You can see CAN bus raw data by:
    ``` bash
    candump can0
    ```
4. Drag slider bars (in Grasshopper) then you will see something similar to this:

    ![image](./docs/vcan_test.png)

### Record CAN bus message
1. Setup SocketCAN interface on `can0` with bitrate 1 Mbps.
    ``` bash
    sudo ip link set can0 up type can bitrate 1000000
    ```
2. Record CAN log.    
    ``` bash
    candump -L can0 > can.log
    ```

## UDP data format
We use JSON format to transmit data between Grasshopper and Raspberry Pi.
``` json
{
    "data": [
        {
            "position": {
                "x": 0, // row 
                "y": 0  // column
            },
            "height": 10
        },
        {
            "position": {
                "x": 0,
                "y": 1
            },
            "height": 20
        }
    ]
}
``` 
## CAN Bus ID and Filter setting
### ID mapping 
A row-major order is adapted in this system. 
A ID in a $n\times n$ matrix system can be calculated with: 
$$ID = nx+y+\theta$$
$\theta$ is the offset of CAN ID (default $\theta=$ `0x100`)
### Filter setting
| Device | ID | Mask |
| --- | --- | --- |
| Raspberry Pi | 0x000 | 0xF00 |

## Component Testing 
### Send JSON to Grasshopper through UDP
We assume the ip address of Grasshopper computer is `192.168.0.2`.
``` bash
cd CanbusController/test
./Json2UdpClient.py -i 192.168.0.2 -f grasshopper_output.json
```
## Send recorded CAN bus data to Grasshopper through UDP
1. Start service
    ``` bash
    cd CanbusController
    ./Json2UdpClient.py -i 192.168.0.2 -f grasshopper_output.json -c vcan0
    ```
2. Play recorded CAN bus data on `vcan0`.
    ``` bash
    cd CanbusController/test
    canplayer vcan0=vcan0 -I ./CanbusController/test/can2udp.log
    ```

## Send recorded CAN bus data to control RoboScope
1. Setup SocketCAN interface on `can0` with bitrate 1 Mbps.
    ``` bash
    sudo ip link set can0 up type can bitrate 1000000
    ```
2. Play CAN log.    
    ``` bash
    canplayer can0=vcan0 -I ./CanbusController/test/udp2can.log
    ```