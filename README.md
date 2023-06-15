# Smart-Charging-Station
A Python REST API with which you can control the RSH-A16 USB Hub using flask and uhubctl. A device connected via USB sends its battery status to the REST API. If this falls below a threshold, the charging cycle is activated. If it is above a threshold, the charging cycle is deactivated. The status of this activation, the battery status and the device name are also published via MQTT.

## Installation

You have to install following dependencies:

```
python3 -m pip install flask
python3 -m pip install paho-mqtt
```

Then you have to download following:

```

```

## Usage



## openHAB Integration

To integrate it in openHAB you can use following rule:

```

```
