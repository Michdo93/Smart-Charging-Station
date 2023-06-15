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
Bridge mqtt:broker:localBroker "Local MQTT Broker" [ 
    host="<broker_ip>",
    port=1883,
    secure=false,
    username="",
    password=""
] {
    Thing topic smartCharger "Smart Charger" {
        Channels:
            Type switch : port1 "Port 1" [ stateTopic="SmartCharger/port/1/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port2 "Port 2" [ stateTopic="SmartCharger/port/2/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port3 "Port 3" [ stateTopic="SmartCharger/port/3/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port4 "Port 4" [ stateTopic="SmartCharger/port/4/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port5 "Port 5" [ stateTopic="SmartCharger/port/5/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port6 "Port 6" [ stateTopic="SmartCharger/port/6/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port7 "Port 7" [ stateTopic="SmartCharger/port/7/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port8 "Port 8" [ stateTopic="SmartCharger/port/8/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port9 "Port 9" [ stateTopic="SmartCharger/port/9/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port10 "Port 10" [ stateTopic="SmartCharger/port/10/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port11 "Port 11" [ stateTopic="SmartCharger/port/11/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port12 "Port 12" [ stateTopic="SmartCharger/port/12/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port13 "Port 13" [ stateTopic="SmartCharger/port/13/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port14 "Port 14" [ stateTopic="SmartCharger/port/14/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port15 "Port 15" [ stateTopic="SmartCharger/port/15/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            Type switch : port16 "Port 16" [ stateTopic="SmartCharger/port/16/state", transformationPattern="JSONPATH:$.state", on="ON", off="OFF" ]
            
            Type string : port1_device "Port 1 Device" [ stateTopic="SmartCharger/port/1/device" ]
            Type string : port2_device "Port 2 Device" [ stateTopic="SmartCharger/port/2/device" ]
            Type string : port3_device "Port 3 Device" [ stateTopic="SmartCharger/port/3/device" ]
            Type string : port4_device "Port 4 Device" [ stateTopic="SmartCharger/port/4/device" ]
            Type string : port5_device "Port 5 Device" [ stateTopic="SmartCharger/port/5/device" ]
            Type string : port6_device "Port 6 Device" [ stateTopic="SmartCharger/port/6/device" ]
            Type string : port7_device "Port 7 Device" [ stateTopic="SmartCharger/port/7/device" ]
            Type string : port8_device "Port 8 Device" [ stateTopic="SmartCharger/port/8/device" ]
            Type string : port9_device "Port 9 Device" [ stateTopic="SmartCharger/port/9/device" ]
            Type string : port10_device "Port 10 Device" [ stateTopic="SmartCharger/port/10/device" ]
            Type string : port11_device "Port 11 Device" [ stateTopic="SmartCharger/port/11/device" ]
            Type string : port12_device "Port 12 Device" [ stateTopic="SmartCharger/port/12/device" ]
            Type string : port13_device "Port 13 Device" [ stateTopic="SmartCharger/port/13/device" ]
            Type string : port14_device "Port 14 Device" [ stateTopic="SmartCharger/port/14/device" ]
            Type string : port15_device "Port 15 Device" [ stateTopic="SmartCharger/port/15/device" ]
            Type string : port16_device "Port 16 Device" [ stateTopic="SmartCharger/port/16/device" ]
            
            Type number : port1_batterylevel "Port 1 Battery Level" [ stateTopic="SmartCharger/port/1/batterylevel" ]
            Type number : port2_batterylevel "Port 2 Battery Level" [ stateTopic="SmartCharger/port/2/batterylevel" ]
            Type number : port3_batterylevel "Port 3 Battery Level" [ stateTopic="SmartCharger/port/3/batterylevel" ]
            Type number : port4_batterylevel "Port 4 Battery Level" [ stateTopic="SmartCharger/port/4/batterylevel" ]
            Type number : port5_batterylevel "Port 5 Battery Level" [ stateTopic="SmartCharger/port/5/batterylevel" ]
            Type number : port6_batterylevel "Port 6 Battery Level" [ stateTopic="SmartCharger/port/6/batterylevel" ]
            Type number : port7_batterylevel "Port 7 Battery Level" [ stateTopic="SmartCharger/port/7/batterylevel" ]
            Type number : port8_batterylevel "Port 8 Battery Level" [ stateTopic="SmartCharger/port/8/batterylevel" ]
            Type number : port9_batterylevel "Port 9 Battery Level" [ stateTopic="SmartCharger/port/9/batterylevel" ]
            Type number : port10_batterylevel "Port 10 Battery Level" [ stateTopic="SmartCharger/port/10/batterylevel" ]
            Type number : port11_batterylevel "Port 11 Battery Level" [ stateTopic="SmartCharger/port/11/batterylevel" ]
            Type number : port12_batterylevel "Port 12 Battery Level" [ stateTopic="SmartCharger/port/12/batterylevel" ]
            Type number : port13_batterylevel "Port 13 Battery Level" [ stateTopic="SmartCharger/port/13/batterylevel" ]
            Type number : port14_batterylevel "Port 14 Battery Level" [ stateTopic="SmartCharger/port/14/batterylevel" ]
            Type number : port15_batterylevel "Port 15 Battery Level" [ stateTopic="SmartCharger/port/15/batterylevel" ]
            Type number : port16_batterylevel "Port 16 Battery Level" [ stateTopic="SmartCharger/port/16/batterylevel" ]
    }
}

```

Please note that you have to replace `<broker_ip>` with the IP address of your MQTT broker.

The items file could look like this:

```
Group gSmartCharger "Smart Charger"

Switch port1_state "Port 1 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/1/state:state:default]" }
Switch port2_state "Port 2 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/2/state:state:default]" }
Switch port3_state "Port 3 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/3/state:state:default]" }
Switch port4_state "Port 4 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/4/state:state:default]" }
Switch port5_state "Port 5 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/5/state:state:default]" }
Switch port6_state "Port 6 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/6/state:state:default]" }
Switch port7_state "Port 7 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/7/state:state:default]" }
Switch port8_state "Port 8 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/8/state:state:default]" }
Switch port9_state "Port 9 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/9/state:state:default]" }
Switch port10_state "Port 10 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/10/state:state:default]" }
Switch port11_state "Port 11 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/11/state:state:default]" }
Switch port12_state "Port 12 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/12/state:state:default]" }
Switch port13_state "Port 13 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/13/state:state:default]" }
Switch port14_state "Port 14 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/14/state:state:default]" }
Switch port15_state "Port 15 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/15/state:state:default]" }
Switch port16_state "Port 16 State" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/16/state:state:default]" }

String port1_device "Port 1 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/1/device:state:default]" }
String port2_device "Port 2 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/2/device:state:default]" }
String port3_device "Port 3 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/3/device:state:default]" }
String port4_device "Port 4 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/4/device:state:default]" }
String port5_device "Port 5 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/5/device:state:default]" }
String port6_device "Port 6 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/6/device:state:default]" }
String port7_device "Port 7 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/7/device:state:default]" }
String port8_device "Port 8 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/8/device:state:default]" }
String port9_device "Port 9 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/9/device:state:default]" }
String port10_device "Port 10 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/10/device:state:default]" }
String port11_device "Port 11 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/11/device:state:default]" }
String port12_device "Port 12 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/12/device:state:default]" }
String port13_device "Port 13 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/13/device:state:default]" }
String port14_device "Port 14 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/14/device:state:default]" }
String port15_device "Port 15 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/15/device:state:default]" }
String port16_device "Port 16 Device" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/16/device:state:default]" }

Number port1_batterylevel "Port 1 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/1/batterylevel:state:default]" }
Number port2_batterylevel "Port 2 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/2/batterylevel:state:default]" }
Number port3_batterylevel "Port 3 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/3/batterylevel:state:default]" }
Number port4_batterylevel "Port 4 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/4/batterylevel:state:default]" }
Number port5_batterylevel "Port 5 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/5/batterylevel:state:default]" }
Number port6_batterylevel "Port 6 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/6/batterylevel:state:default]" }
Number port7_batterylevel "Port 7 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/7/batterylevel:state:default]" }
Number port8_batterylevel "Port 8 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/8/batterylevel:state:default]" }
Number port9_batterylevel "Port 9 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/9/batterylevel:state:default]" }
Number port10_batterylevel "Port 10 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/10/batterylevel:state:default]" }
Number port11_batterylevel "Port 11 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/11/batterylevel:state:default]" }
Number port12_batterylevel "Port 12 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/12/batterylevel:state:default]" }
Number port13_batterylevel "Port 13 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/13/batterylevel:state:default]" }
Number port14_batterylevel "Port 14 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/14/batterylevel:state:default]" }
Number port15_batterylevel "Port 15 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/15/batterylevel:state:default]" }
Number port16_batterylevel "Port 16 Battery Level" (gSmartCharger) { mqtt="<[<broker_ip>:SmartCharger/port/16/batterylevel:state:default]" }
```

Replace `<broker_ip>` with the IP address of your broker so that the connection can be established properly.

And a rule could look like this:

```
rule "SmartCharger State Control"
when
    Item gSmartCharger received update
then
    val baseUrl = "http://<smartcharger_ip>:<smartcharger_port>/api/smartcharger/state/"
    
    gSmartCharger.members.forEach[switchItem |
        val portId = Integer::parseInt(switchItem.name.split("_").get(0).replace("port", ""))
        val switchState = switchItem.state.toString
        
        var command = ""
        if (switchState == "ON") {
            command = "ON"
        } else if (switchState == "OFF") {
            command = "OFF"
        }
        
        val url = baseUrl + portId
        
        sendHttpPutRequest(url, "text/plain", command)
    ]
end
```

Please replace `<smartcharger_ip>:<smartcharger_port>` with the IP and Port of your Smart Charger.
