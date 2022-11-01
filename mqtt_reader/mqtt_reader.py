import os
import redis
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv()

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}.")
    client.subscribe("color")

def on_message(client, userdata, msg):
    color = msg.payload.decode('utf-8')

    print(f"New color: {color}.")

    stream_payload = {
        "color": color
    }

    match color:
        case "red":
            stream_payload["r"] = 255
            stream_payload["g"] = 0
            stream_payload["b"] = 0
        case "green":
            stream_payload["r"] = 0
            stream_payload["g"] = 128
            stream_payload["b"] = 0
        case "blue":
            stream_payload["r"] = 0
            stream_payload["g"] = 0
            stream_payload["b"] = 255
        case "cyan":
            stream_payload["r"] = 0
            stream_payload["g"] = 255
            stream_payload["b"] = 255
        case "white":
            stream_payload["r"] = 255
            stream_payload["g"] = 255
            stream_payload["b"] = 255
        case "oldlace":
            stream_payload["r"] = 253
            stream_payload["g"] = 245
            stream_payload["b"] = 230
        case "purple":
            stream_payload["r"] = 128
            stream_payload["g"] = 0
            stream_payload["b"] = 128
        case "magenta":
            stream_payload["r"] = 255
            stream_payload["g"] = 0
            stream_payload["b"] = 255
        case "yellow":
            stream_payload["r"] = 255
            stream_payload["g"] = 255
            stream_payload["b"] = 0
        case "orange":
            stream_payload["r"] = 255
            stream_payload["g"] = 165
            stream_payload["b"] = 0
        case "pink":
            stream_payload["r"] = 255
            stream_payload["g"] = 192
            stream_payload["b"] = 203

    new_entry_timestamp = redis_client.xadd(name = "cheerlights", fields = stream_payload, maxlen = 10000, approximate = True)
    print(f"Added to Redis stream as {new_entry_timestamp}.")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")), 60)
mqtt_client.loop_forever()