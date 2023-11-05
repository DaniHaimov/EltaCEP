import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection


def _connect(connection_params, name: str) -> (BlockingConnection, BlockingChannel):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=name)
    return connection, channel


class ProducerMessageBroker:
    def __init__(self, connection_params, name: str):
        self.__channel = None
        self.__connection = None
        self.__connection_params = connection_params
        self.__name = name

    def publish(self, body) -> None:
        self.__channel.basic_publish(exchange="", routing_key=self.__name, body=body)

    def open_connection(self) -> None:
        (self.__connection, self.__channel) = _connect(self.__connection_params, self.__name)

    def close_connection(self) -> None:
        self.__connection.close()


class ConsumerMessageBroker:
    def __init__(self, connection_params, name: str, callback):
        self.__channel = None
        self.__connection = None
        self.__connection_params = connection_params
        self.__name = name
        self.__callback = callback

    def start_consume(self) -> None:
        self.__channel.basic_consume(queue=self.__name, on_message_callback=self.__callback, auto_ack=True)
        self.__channel.start_consuming()

    def stop_consume(self) -> None:
        self.__channel.stop_consuming()

    def open_connection(self) -> None:
        (self.__connection, self.__channel) = _connect(self.__connection_params, self.__name)

    def close_connection(self) -> None:
        self.__connection.close()
