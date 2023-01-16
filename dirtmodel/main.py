import threading
import time
import mosquitto
import sys

from soil import Soil, SoilParameters

soil_lock = threading.Lock()
params = SoilParameters(humus_level=0.5, looseness=0.5,
                        volume=100, plant_absorb=1)
soil = Soil(params)

shouldIrrigate = False
shouldIrrigateLock = threading.Lock()

is_connected = False

mqttc = mosquitto.Mosquitto()


def soil_thread():
    while True:
        soil_lock.acquire()
        try:
            soil.tick()
            if (is_connected and soil.tick_ % 4 == 0) or shouldIrrigate:
                mqttc.publish('brain', soil.get_water_level())
                print('water level: ', soil.get_water_level())
                mqttc.publish('weather', soil.get_weather())

                sys.stdout.flush()
        except Exception as e:
            print('soil thread error', e)
            sys.stdout.flush()
        finally:
            soil_lock.release()
        time.sleep(2)


def irrigator_thread_func():
    while True:
        soil_lock.acquire()
        try:
            shouldIrrigateLock.acquire()
            if shouldIrrigate:
                soil.irrigate(10)
        finally:
            shouldIrrigateLock.release()
            soil_lock.release()
        time.sleep(2)


def on_connect(mqttc, obj, rc):
    print('connected')
    global is_connected
    is_connected = True


irrigator_thread = threading.Thread(target=irrigator_thread_func)


def on_message(mqttc, obj, msg):
    global shouldIrrigate
    print("___________received_msg___________")
    received_msg = msg.payload.decode('ASCII')
    # msg.payload can be commands: water_level and start_irrigation, stop_irrigation
    print("RECEIVED MSG: ", received_msg)
    try:
        if received_msg == 'water_level':
            soil_lock.acquire()
            try:
                mqttc.publish('brain', soil.get_water_level())
            finally:
                soil_lock.release()
        elif received_msg == 'start_irrigation':
            print("_________received_start_msg_________")
            if irrigator_thread.is_alive():
                print("_________received_start_msg_IM_IN_________")
                try:
                    shouldIrrigateLock.acquire()
                    shouldIrrigate = True
                finally:
                    shouldIrrigateLock.release()
        elif received_msg == 'stop_irrigation':
            print("_________received_stop_msg_________")
            try:
                shouldIrrigateLock.acquire()
                shouldIrrigate = False
            finally:
                shouldIrrigateLock.release()

    except:
        print('error')
        sys.stdout.flush()


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


if __name__ == '__main__':
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    mqttc.on_log = on_log

    mqttc.connect("mqtt-broker", 1883, 60)

    mqttc.subscribe("soil", 0)

    mqttc.subscribe("ui", 0)

    # publishing message on topic with QoS 0 and the message is not Retained
    mqttc.publish("brain", "20", 0, False)

    threading.Thread(target=soil_thread).start()
    irrigator_thread.start()
    mqttc.loop_start()
