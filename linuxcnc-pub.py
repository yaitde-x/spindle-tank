import random
import time
import sys
import linuxcnc
import json
from paho.mqtt import client as mqtt_client

broker = '192.168.0.100'
port = 1883
topic = "machine-status-response"
client_id = 'linuxcnc-stat-routerx'
# username = 'emqx'
# password = 'public'

connected = False
sent = False

def get_linuxcnc_status():

    try:
        s = linuxcnc.stat()  # create a connection to the status channel
        s.poll()  # get current values
    except linuxcnc.error as detail:
        return {{'status', 'linuxcncerr: {}'.format(detail)}}

    model = {}

    for x in dir(s):
        if not x.startswith('_'):
            attr = getattr(s, x)

            if (x.startswith('paused') or x.startswith('exec_state') or x.startswith('enabled') or x.startswith('estop') or x.startswith('file') or x.startswith('state') or x.startswith('tool_in_spindle')):
                model[x] = attr

    with open('linuxcnc-stat.json', 'w') as outfile:
        json.dump(model, outfile)

    return model

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        global connected
        connected = False
        if rc == 0:
            print("Connected to MQTT Broker!")
            connected = True
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(client, userdata, rc):
        global connected
        connected = False
        print("disconnected from MQTT Broker!")

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client


def run():
    
    global sent

    while not sent:

        try:

            if (not connected):
                client = connect_mqtt()
                client.loop_start()
                time.sleep(3)

            if (connected):
                linuxcncStatus = get_linuxcnc_status()

                msg = json.dumps(linuxcncStatus)
                result = client.publish(topic, msg)

                status = result[0]
                if status == 0:
                    sent = True
                else:
                    print("send to {} failed".format(topic))

            time.sleep(10)

        except err:
            print('error', err)


if __name__ == '__main__':
    run()
