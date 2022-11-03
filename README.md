# Cheerlights with Redis Streams

## Overview

This was a small project I made for a Redis live stream.  It uses the CheerLights MQTT server and a Redis Stream to control a Pimoroni Unicorn Hat LED light matrix attached to a Raspberry Pi.

* [Watch a video presentation of this project](https://www.youtube.com/watch?v=j0TphaKoEVg) from the Simon's Things on Thursdays live stream series.
* [Read the CheerLights blog entry](https://cheerlights.com/learn-redis-streams-with-the-cheerlights-iot-project/) for this project.

## Shopping List

If you want to use the code provided as is, you'll need to buy or acquire:

* Any [Raspberry Pi](https://www.raspberrypi.com/products/) with 40 pin header and wifi (e.g. Pi 3A+, 3B, 3B+, 4) -- or a Raspberry Pi 2 with a USB wifi adapter.  Don't get a Raspberry Pi 400 all in one or a Pico.
* A Raspberry Pi power supply (USB C if you are using the Pi 4, otherwise micro USB).
* A micro SD card (8Gb or bigger).
* A [Pimoroni Unicorn Hat](https://shop.pimoroni.com/products/unicorn-hat?variant=932565325).

You'll also need these things that don't cost anything:

* [A copy of Raspberry Pi OS](https://www.raspberrypi.com/software/).
* [A Redis database in the cloud](https://redis.com/try-free/).  Once you've signed up and created a database, make a note of the host, port, and password... you'll need these later.

Optional:

This is optional, and free, but worth using if you want to see what's happening in your Redis database:

* [A copy of RedisInsight](https://redis.com/redis-enterprise/redis-insight/) - once you've installed RedisInsight use the host, port and password for your Redis database to connect.

## Hardware Build / Raspberry Pi Setup

* Attach the Unicorn Hat to the Raspberry Pi's GPIO pins.  Press it firmly down to ensure a good fit.  Do this with the Raspberry Pi turned off.
* Copy Raspberry Pi OS to your micro SD card ([instructions from Raspberry Pi here](https://www.raspberrypi.com/documentation/computers/getting-started.html)).
* Insert the micro SD card into the Raspberry Pi, and attach a USB keyboard and HDMI monitor to it.
* Attach the power supply to the Raspberry Pi and turn it on.
* Once the Pi has booted, set up your wifi credentials to connect to your network ([guide](https://www.raspberrypi.com/documentation/computers/getting-started.html)).
* Start a Terminal session on the Pi.  You'll need this to install the software, configure and run it.

## Getting Started with the Software

There are two parts to the software, both written in Python.  The MQTT Reader component can run on the Raspberry Pi or any other computer that has Python 3.10 or higher installed and a network connection.

The Pi Consumer component must run on the Raspberry Pi.

### Running the MQTT Reader

From the terminal, get a copy of this repository:

```bash
git clone https://github.com/simonprickett/cheerlights-with-redis-streams.git
```

Then, change directory to the folder containing the MQTT Reader:

```bash
cd cheerlights-with-redis-streams/mqtt_reader
```

Now, create a Python virtual environment and activate it:

```bash
python3 -m venv venv
. ./venv/bin/activate
```

Next, install the libraries we need to run the code:

```bash
pip install -r requirements.txt
```

Finally, use the provided example environment file to create a `.env` file that the code will load configuration and secrets from:

```bash
cp env.sample .env
```

Then open `.env` in your text editor and make it look like this:

```
MQTT_HOST=mqtt.cheerlights.com
MQTT_PORT=1883
REDIS_URL=redis://default:REDIS_PASSWORD@REDIS_HOST:REDIS_PORT?decode_responses=True
```

Replace `REDIS_PASSWORD`, `REDIS_HOST` and `REDIS_PORT` with the values you noted down when you created your Redis cloud database.

Save your changes.

Now, start the MQTT reader:

```bash
python mqtt_reader.py
```

The code should start, and put the latest CheerLights color into a Redis Stream.  You should see output that looks something like this:

```
Connected to MQTT server with result code 0.
New color: magenta.
Added to Redis stream as 1667506837856-0.
```

If you opted to install RedisInsight, use it to connect to your database and verify that a key named `cheerlights` was created in Redis, and that it's a stream with a value in it.

Leave the MQTT Reader component running.  It will receive new CheerLights colors as they are published, and store them in the Redis Stream.

### Running the Pi Consumer Component

This component must run on the Raspberry Pi!

From the terminal, get a copy of this repository:

```bash
git clone https://github.com/simonprickett/cheerlights-with-redis-streams.git
```

Then, change directory to the folder containing the Pi Consumer:

```bash
cd cheerlights-with-redis-streams/pi_consumer
```

Use the `sudo` command to start a root shell... this extra level of privilege is required due to the way the Unicorn Hat works:

```
sudo bash
```

Now, create a Python virtual environment and activate it:

```bash
python3 -m venv venv
. ./venv/bin/activate
```

Next, install the libraries we need to run the code:

```bash
pip install -r requirements.txt
```

Finally, use the provided example environment file to create a `.env` file that the code will load configuration and secrets from:

```bash
cp env.sample .env
```

Then open `.env` in your text editor and make it look like this:

```
REDIS_URL=redis://default:REDIS_PASSWORD@REDIS_HOST:REDIS_PORT?decode_responses=True
```

Replace `REDIS_PASSWORD`, `REDIS_HOST` and `REDIS_PORT` with the values you noted down when you created your Redis cloud database.

Save your changes.

Now, start the Pi Consumer:

```bash
python stream_consumer.py
```

You should see the consumer code start up and log its actions.  You should also see the LEDs light up!  The code should output something like this:

```
[['cheerlights', [('1667506837856-0', {'color': 'magenta', 'r': '255', 'g': '0', 'b': '255'})]]]
{'color': 'magenta', 'r': '255', 'g': '0', 'b': '255'}
```

Leave the code running to enjoy the light show!

## Updating the CheerLights Color

There's a couple of ways you can update the CheerLights color yourself... this should change the color on all the CheerLights worldwide!

* Tweet `@cheerlights COLOR_NAME` or `#cheerlights COLOR_NAME`.
* Use the [CheerLights Discord](https://discord.com/invite/G7Q5UjDT7K) and type `/cheerlights COLOR_NAME`.

See the list of [valid CheerLights colors on their website](https://cheerlights.com/learn/) (scroll down to the "Supported Colors" section).

You should see the MQTT reader receive a message with your new color shortly after you tweet or post on Discord, then the Pi should update the LEDs to the new color within 1-5 seconds.
