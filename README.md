# RoboScope
## Network Configuration
### Method 1 - Connect through a Router 
- Both Grasshopper computer and Raspberry Pi connect to a router.
- Check IP address of the Raspberry Pi.
### Method 2 - Ethernet Cable direct connect 
- Connect Grasshopper computer and Raspberry Pi via a Ethernet cable and the network setting:
  Device | IP | Mask | gateway
  | --- | --- | --- | --- |
  Grasshopper computer | 192.168.0.2 | 255.255.255.0| 0.0.0.0
  Raspberry Pi | 192.168.0.1 | 255.255.255.0 | 0.0.0.0
## Rhino Grasshopper
### Plugin Installation
1. Networking plugin: `gHowl` can be downloaded from [here](https://www.food4rhino.com/en/app/ghowl). And check [this instruction](https://www.food4rhino.com/en/faq#users-install-grasshopper-plugin) to install the plugin.

### Set up Raspberry Pi IP address on Grasshopper
Here we assume that Raspberry Pi is hosted at `10.100.2.97`
![image](./docs//Grasshopper_ip_setup.png)

## CanbusController (run at Raspberry Pi)
1. Install requirements
    ``` bash
    cd CanbusController
    pip3 install -r requirements.txt
    ```
2. Plug in CANDO and start interface
    ``` bash
    sudo ip link set can0 up type can bitrate 1000000
    ```
3. Start `UdpServer2CANbus.py`
    ``` bash
    ./UdpServer2CANbus.py -i 10.100.2.97 -p 5005 -c can0
    ```
4. Show CAN bus raw data.
    ``` bash
    candump can0
    ```