import pika
import os
from dotenv import load_dotenv

from message_broker import ConsumerMessageBroker

load_dotenv()

_channel = None


def _def_callback(ch, method, properties, body):
    print(f'WARNING: {body.decode()}')


if __name__ == '__main__':
    msg_broker_host = os.getenv("MESSAGE_BROKER_HOST")
    msg_broker_port = int(os.getenv("MESSAGE_BROKER_PORT"))
    msg_broker_user = os.getenv("MESSAGE_BROKER_USER")
    msg_broker_pass = os.getenv("MESSAGE_BROKER_PASS")
    msg_broker_name = os.getenv("MESSAGE_BROKER_NAME")

    amqp_url = f'amqp://{msg_broker_user}:{msg_broker_pass}@{msg_broker_host}:{msg_broker_port}/%2F'
    params = pika.URLParameters(amqp_url)

    msg_broker = ConsumerMessageBroker(params, msg_broker_name, _def_callback)

    msg_broker.open_connection()

    print("Starting Consume")
    try:
        msg_broker.start_consume()
    finally:
        msg_broker.stop_consume()
        msg_broker.close_connection()
