import asyncio
import sys
import logging
import atexit
import json
import paho.mqtt.client as mqtt
import datetime as dt

logger = logging.getLogger()
logger.setLevel(logging.INFO)
QOS = 2
MILESTONE = 500

MESSAGE_COUNT = [0]
start_time = dt.datetime.now()

config = 'settings.json'
if len(sys.argv) < 2:
    logging.warning(f'no config file provided. reading default {config}')
if len(sys.argv) == 2:
    logging.info(f'reading config file {sys.argv[1]}')

try:
    with open(config, 'r') as f:
        settings = json.loads(f.read())
        HOST, PORT = settings['host'], settings['port']
        CREDENTIALS = settings['login'], settings['password']
        TOPIC = settings['topic']
        PAYLOAD = settings['messagePayload']
        DELAY = settings['messageDelay']
        USERS = settings['parallelUsers']
except:
    logging.error('error in reading config file. Please check file exists and format correct')


@atexit.register
def exit_handler():
    print('\n\n\n================')
    print(f'total messages sent = {MESSAGE_COUNT[0]}')
    print(f'total test time = {(dt.datetime.now() - start_time).seconds} sec')


async def publisher(client_id: int):
    logging.info(f'publisher {client_id} started')
    client = mqtt.Client()
    client.username_pw_set(*CREDENTIALS)
    client.connect(host=HOST, port=PORT)
    client.loop_start()
    logging.info(f'connection status id {client_id} - {client.is_connected()}')

    while True:
        MESSAGE_COUNT[0] += 1
        result = client.publish(topic=TOPIC, payload=PAYLOAD, qos=QOS)
        logging.debug(f'pub result - {result.rc}')
        if MESSAGE_COUNT[0] % MILESTONE == 0:
            delta = dt.datetime.now() - start_time
            logging.warning(f'{MESSAGE_COUNT[0]} messages sent. Rate = {MESSAGE_COUNT[0] / delta.seconds}')

        if MESSAGE_COUNT[0] == 100 * 1000 * 1000:
            exit()
        await asyncio.sleep(DELAY)


async def main():
    logging.info(f'test started at {start_time.strftime("%H:%M:%S")}')

    tasks = list()
    for i in range(USERS):
        tasks.append(publisher(i))
    await asyncio.gather(*tasks)


asyncio.run(main())
