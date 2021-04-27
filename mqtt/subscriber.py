import logging
import time
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
TOPIC = 'topic/01'
QOS = 2
HOST, PORT = '1.1.1.1', 1883
CREDENTIALS = 'login', 'password'
LIFETIME = 10 * 60  # 10 minutes

MESSAGE_COUNT = [0]


def message_handler(client, userdata, message: MQTTMessage):
    MESSAGE_COUNT[0] += 1
    logging.debug(
        f'message id = {message.mid} message #{MESSAGE_COUNT[0]:05} qos={message.qos}, payload={message.payload}')
    if message.mid != MESSAGE_COUNT[0]:
        logging.error(f'message id = {message.mid} message #{MESSAGE_COUNT[0]:05}')
        exit()


client = mqtt.Client()
client.username_pw_set(*CREDENTIALS)
client.on_message = message_handler
client.connect(host=HOST, port=PORT)
client.subscribe(topic=TOPIC, qos=QOS)
client.loop_start()
logging.info(f'connection status - {client.is_connected()}')

time.sleep(10 * 60)

client.disconnect()
