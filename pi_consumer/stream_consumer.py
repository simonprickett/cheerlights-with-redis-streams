import os
import redis
import time
import unicornhat
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

last_id = redis_client.get("last_displayed_id")

unicornhat.set_layout(unicornhat.AUTO)
unicornhat.rotation(180)
unicornhat.brightness(0.19)
unicorn_width, unicorn_height = unicornhat.get_shape()
unicornhat.off()

if last_id is None:
    last_id = "0-0"

while True:
    stream_response = redis_client.xread(streams = {"cheerlights": last_id}, count = 1, block = 5000)
    print(stream_response)

    if len(stream_response) == 0:
        print("Nothing new to display yet.")
    else:
        new_colors = stream_response[0][1][0][1]
        print(new_colors)

        unicornhat.set_all(int(new_colors['r']), int(new_colors['g']), int(new_colors['b']))
        unicornhat.show()

        last_id = stream_response[0][1][0][0]
        redis_client.set("last_displayed_id", last_id)
        time.sleep(5)