# Smart-Charging-Station
A Python REST API with which you can control the [RSH-A16 USB Hub](https://rshtech.com/products/16-ports-aluminum-usb-30-data-hub-with-12v-83a-with-uk-power-adapterrsh-a16) using flask and uhubctl. A device connected via USB sends its battery status to the REST API. If this falls below a threshold, the charging cycle is activated. If it is above a threshold, the charging cycle is deactivated. The status of this activation, the battery status and the device name are also published via MQTT.

## Installation

At first you have to install [uhubctl](https://github.com/mvp/uhubctl):

```
sudo apt-get install libusb-1.0-0-dev
git clone https://github.com/mvp/uhubctl
cd uhubctl
make
sudo make install
```

Maybe you have to create with `sudo nano /etc/udev/rules.d/52-usb.rules` the following `udev rule`:

```
SUBSYSTEM=="usb", DRIVER=="usb", MODE="0666", ATTR{idVendor}=="0bda", ATTR{idProduct}=="0411"
```

Then you have to run:

```
sudo usermod -a -G dialout $USER
sudo udevadm trigger --attr-match=subsystem=usb
```

You have to install following dependencies:

```
python3 -m pip install flask
python3 -m pip install paho-mqtt
```

Then you have to download following:

```
wget https://raw.githubusercontent.com/Michdo93/Smart-Charging-Station/main/smart_charging_station.py
sudo chmod +x smart_charging_station.py
wget https://raw.githubusercontent.com/Michdo93/Smart-Charging-Station/main/smart-charging-station.service
sudo mv smart-charging-station.service /etc/systemd/system
```

Please change in following line (smart_charging_station.py), the `<broker_ip>` to your mqtt client.

```
charger = SmartCharger(api_port=5000, broker_ip="<broker_ip>")
```

In your service file you have to replace `<user>` with the username of your system user.

## Usage

At first run `sudo uhubctl`. You will receive something like this:

```
...
Current status for hub 5-2.4 [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 1: 02a0 power 5gbps Rx.Detect
  Port 2: 02a0 power 5gbps Rx.Detect
  Port 3: 02a0 power 5gbps Rx.Detect
  Port 4: 02a0 power 5gbps Rx.Detect
Current status for hub 5-2.3.4 [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 1: 02a0 power 5gbps Rx.Detect
  Port 2: 02a0 power 5gbps Rx.Detect
  Port 3: 02a0 power 5gbps Rx.Detect
  Port 4: 02a0 power 5gbps Rx.Detect
Current status for hub 5-2.3.3 [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 1: 02a0 power 5gbps Rx.Detect
  Port 2: 02a0 power 5gbps Rx.Detect
  Port 3: 02a0 power 5gbps Rx.Detect
  Port 4: 02a0 power 5gbps Rx.Detect
Current status for hub 5-2.3 [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 1: 02a0 power 5gbps Rx.Detect
  Port 2: 02a0 power 5gbps Rx.Detect
  Port 3: 0263 power 5gbps U3 enable connect [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 4: 0263 power 5gbps U3 enable connect [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
Current status for hub 5-2 [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 1: 02a0 power 5gbps Rx.Detect
  Port 2: 02a0 power 5gbps Rx.Detect
  Port 3: 0263 power 5gbps U3 enable connect [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
  Port 4: 0263 power 5gbps U3 enable connect [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
Current status for hub 5 [1d6b:0003 Linux 5.4.0-150-generic xhci-hcd xHCI Host Controller 0000:04:00.0, USB 3.00, 2 ports, ppps]
  Port 1: 02a0 power 5gbps Rx.Detect
  Port 2: 0263 power 5gbps U3 enable connect [0bda:0411 Generic 4-Port USB 3.1 Hub, USB 3.20, 4 ports, ppps]
...
```

In the python file it is mapped to this:

```
PORTS = {
    1: "-l 5-2 -p 1",
    2: "-l 5-2 -p 2",
    3: "-l 5-2.4 -p 1",
    4: "-l 5-2.4 -p 2",
    5: "-l 5-2.4 -p 3",
    6: "-l 5-2.4 -p 4",
    7: "-l 5-2.3 -p 1",
    8: "-l 5-2.3 -p 2",
    9: "-l 5-2.3.4 -p 1",
    10: "-l 5-2.3.4 -p 2",
    11: "-l 5-2.3.4 -p 3",
    12: "-l 5-2.3.4 -p 4",
    13: "-l 5-2.3.3 -p 1",
    14: "-l 5-2.3.3 -p 2",
    15: "-l 5-2.3.3 -p 3",
    16: "-l 5-2.3.3 -p 4"
}
```

Please test in a terminal how you can controll each port separately and replace this port mapping. Therefore you have to switch on each port and the run:

```
sudo uhubctl -a off -l <mapping_for_port>
```

In your python file you can also use different values for:

```
api_port: int, broker_protocol: str = "tcp", broker_ip: str = "127.0.0.1", broker_port: int = 1883, client_id: str = "SmartCharger", tls_path: str = "", tls_version: str = "", broker_user: str = "", broker_password: str = "", broker_qos: int = 0, broker_retain: bool = False, broker_async: bool = False
```

## openHAB Integration

To integrate it in openHAB you can use following thing file:

```

```

The items file could look like this:

```

```
