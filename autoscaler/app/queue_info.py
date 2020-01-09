import pika
import time
from log import logger


def get_connection(rabbitmq_url):
    while True:
        try:
            params = pika.ConnectionParameters(rabbitmq_url,
                                               heartbeat=600,
                                               blocked_connection_timeout=300)
            return pika.BlockingConnection(params)
        except Exception:
            logger.error('Retrying to connect to queue', exc_info=True)
            time.sleep(3)


def get_queue_length(rabbitmq_url, queue_name):
    connection = get_connection(rabbitmq_url)

    try:
        channel = connection.channel()
        response = channel.queue_declare(queue=queue_name,
                                         durable=True,
                                         passive=True)
        num_msg_in_queue = response.method.message_count
    finally:
        connection.close()

    return num_msg_in_queue
