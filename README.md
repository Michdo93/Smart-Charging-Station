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



## openHAB Integration

To integrate it in openHAB you can use following thing file:

```

```

The items file could look like this:

```

```
