import pika
import os
import time
import json
from log import logger

rabbitmq_url = os.getenv('AMQP_URL')
logger.info('Connecting to RabbitMQ at {}'.format(rabbitmq_url))

connection = None
channel = None

while connection is None:
    try:
        params = pika.ConnectionParameters(rabbitmq_url,
                                           heartbeat=600,
                                           blocked_connection_timeout=300)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='jobs',
                              durable=True)
    except Exception:
        logger.warning('Retrying to connect to queue', exc_info=False)
        time.sleep(3)


def publish_job(job):
    channel.basic_publish(exchange='', routing_key='jobs', body=json.dumps(job))
    logger.debug('Sent message!')
