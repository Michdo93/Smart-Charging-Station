from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import os
import string
import random

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

class ChargingPort(object):
    def __init__(self, port_id: int):
        self._port_id: int = port_id
        self._state: str = ""
        self._battery_level: int = None
        self._device_name: str = ""

    def getPortId(self):
        return self._port_id

    def getState(self):
        return self._state

    def setState(self, value):
        self._state = value

    def getBatteryLevel(self):
        return self._battery_level

    def setBatteryLevel(self, value):
        self._battery_level = value

    def getDeviceName(self):
        return self._device_name

    def setDeviceName(self, value):
        self._device_name = value

class SmartCharger(object):

    def __init__(self, api_port: int, broker_protocol: str = "tcp", broker_ip: str = "127.0.0.1", broker_port: int = 1883, client_id: str = "SmartCharger", tls_path: str = "", tls_version: str = "", broker_user: str = "", broker_password: str = "", broker_qos: int = 0, broker_retain: bool = False, broker_async: bool = False):
        self.app = Flask(__name__)
        self.port: int = api_port
        self.brokerTransport = broker_protocol
        self.brokerIP = broker_ip
        self.brokerPort = broker_port
        self.clientId = client_id
        self.tlsPath = tls_path
        self.tlsVersion = tls_version
        self.brokerUser = broker_user
        self.brokerPWD = broker_password
        self.brokerQOS = broker_qos
        self.retain = broker_retain
        self.brokerAsync = broker_async

        self.mqtt_topic_state = client_id.lower() + "/port/{}/state"
        self.mqtt_topic_devicename = client_id.lower() + "/port/{}/device"
        self.mqtt_topic_batterylevel = client_id.lower() + "/port/{}/batterylevel"

        self.ports = {}
        for port_id in range(1, 17):
            self.ports[port_id] = ChargingPort(port_id)

        self.setup_routes()

        rand = "".join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(3))

        if self.brokerQOS not in range(0, 3):
            self.brokerQOS = 0

        self.auth = None
        if self.brokerUser is not None:
            if self.brokerPWD is not None:
                self.auth = {'username': self.brokerUser,
                             'password': self.brokerPWD}
            else:
                self.auth = {'username': self.brokerUser,
                             'password': ""}
        else:
            self.auth = None

        if self.brokerUser == "" or self.brokerUser == None:
            self.auth = None

        self.broker_tls = None
        if self.brokerPort != 1883:
            if self.tlsPath is not None or self.tlsPath != "":
                if self.tlsVersion is not None or self.tlsVersion != "":
                    self.broker_tls = (self.tlsPath, self.tlsVersion)
                else:
                    self.broker_tls = self.tlsPath
            else:
                self.broker_tls = None

        self.client = mqtt.Client(client_id=self.clientId[:20]+rand, clean_session=True,
                                  userdata=None, protocol=mqtt.MQTTv311, transport=self.brokerTransport)

        if self.broker_tls is not None:
            self.client.tls_set(self.broker_tls)

        if self.retain == True:
            self.retain = True
        else:
            self.retain = False

        if self.brokerAsync == True:
            self.brokerAsync = True
        else:
            self.brokerAsync = False

        self.client.username_pw_set(self.auth)
        self.client.connect(self.brokerIP, self.brokerPort)

        for port_id in range(1, 17):
            self.__powerOn(port_id)

    def setup_routes(self):
        self.app.add_url_rule("/api/smartcharger/state/<int:port_id>", methods=["GET"], view_func=self.getState)
        self.app.add_url_rule("/api/smartcharger/command/<int:port_id>", methods=["POST"], view_func=self.setCommand)

    def setCommand(self, port_id: int):
        cmd = request.json["command"]
        device_name = request.json["device_name"]
        battery_level = request.json["battery_level"]

        if port_id not in self.ports:
            return jsonify({"error": "The port_id is not available."}), 404

        self.ports[port_id].setDeviceName(device_name)
        self.ports[port_id].setBatteryLevel(battery_level)

        if(cmd == "ON"):
            self.__powerOn(port_id)
        elif(cmd == "OFF"):
            self.__powerOff(port_id)
        else:
            return jsonify({"error": "Command is not available. Please send ON or OFF."}), 404

        state: str = self.__getState(port_id)

        return jsonify(state), 200

    def getState(self, port_id: int):
        if(self.__checkPortNumber(port_id) == False):
            return jsonify({"error": "The port_id is not available."}), 404

        return jsonify(self.__getState(port_id))

    def run(self):
            self.app.run(port=self.port)

    def run(self):
        self.app.run(port=self.port)

    def publish_state(self, port_id: int):
        topic_state = self.mqtt_topic_state.format(port_id)
        topic_device_name = self.mqtt_topic_devicename.format(port_id)
        topic_battery_level = self.mqtt_topic_batterylevel.format(port_id)

        state = self.ports[port_id].getState()
        device_name = self.ports[port_id].getDeviceName()
        battery_level = self.ports[port_id].getBatteryLevel()

        self.client.publish(topic_state, state)
        self.client.publish(topic_device_name, device_name)
        self.client.publish(topic_battery_level, battery_level)

    def __checkPortNumber(self, port: int):
        if 1 <= port <= 16:
            return True
        else:
            return False

    def __powerOn(self, port_id: int):
        print(str(port_id) + " received command on")

        commandSuffix: str = self.__getCommandSuffix(port_id)
        self.__setState(port_id, "ON")
        self.__executeCommand("uhubctl -a on " + commandSuffix)
        self.publish_state(port_id)

    def __powerOff(self, port_id: int):
        print(str(port_id) + " received command off")
        commandSuffix: str = self.__getCommandSuffix(port_id)

        self.__setState(port_id, "OFF")
        self.__executeCommand("uhubctl -a off " + commandSuffix)
        self.publish_state(port_id)

    def __executeCommand(self, command):
        os.system(command)

    def __getCommandSuffix(self, port_id: int):
        port_mapping = {
            1: PORTS[1],
            2: PORTS[2],
            3: PORTS[3],
            4: PORTS[4],
            5: PORTS[5],
            6: PORTS[6],
            7: PORTS[7],
            8: PORTS[8],
            9: PORTS[9],
            10: PORTS[10],
            11: PORTS[11],
            12: PORTS[12],
            13: PORTS[13],
            14: PORTS[14],
            15: PORTS[15],
            16: PORTS[16]
        }

        return port_mapping.get(port_id, "")

    def __getState(self, port_id: int):
        state: str = ""

        if self.__checkPortNumber(port_id):
            state = self.ports[port_id].getState()

        return state

    def __setState(self, port_id: int, state: str):
        if(self.__checkPortNumber(port_id)):
            self.ports[port_id].setState(state)

if __name__ == "__main__":
    charger = SmartCharger(api_port=5000, broker_ip="<broker_ip>")
    charger.run()
