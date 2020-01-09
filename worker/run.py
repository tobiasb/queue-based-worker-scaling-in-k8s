import pika
import os
import time
import json
import requests
import datetime
from log import logger

jobs_api_host = os.getenv('JOB_API_HOST')
logger.info('Job API host: {}'.format(jobs_api_host))

rabbitmq_url = os.getenv('AMQP_URL')
logger.info('Connecting to RabbitMQ at {}'.format(rabbitmq_url))


def update_job(job_id, body):
    response = requests.patch(jobs_api_host + '/jobs/' + job_id,
                              headers={'Content-Type': 'application/json'},
                              json=body)
    logger.debug('API responded with ' + str(response.status_code))


def callback(body):
    if body is None:
        return

    data = json.loads(body)
    job_id = str(data['id'])
    logger.debug('Received job [{}]'.format(job_id))

    update_job(job_id, {
        'status': 'in_progress',
    })

    received_utc = datetime.datetime.now()

    if 'delay' in data['parameters']:
        time.sleep(int(data['parameters']['delay']))

    update_job(job_id, {
        'status': 'done',
        'metadata': {
            'result': 'https://cloud-storage-sample/' + job_id,
            'worker_received_utc': received_utc.replace(microsecond=0).isoformat(),
        }
    })


connection = None
channel = None

while connection is None:
    try:
        params = pika.ConnectionParameters(rabbitmq_url,
                                           heartbeat=600,
                                           blocked_connection_timeout=300)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)

    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:
        logger.warning('Retrying to connect to queue', exc_info=False)
        time.sleep(3)


def consume_individually():
    while True:
        queue_state = channel.queue_declare(queue='jobs', durable=True)
        queue_empty = queue_state.method.message_count == 0

        if queue_empty:
            time.sleep(1)
        else:
            method, properties, body = channel.basic_get(queue='jobs', auto_ack=False)

            try:
                callback(body)
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception:
                logger.error('Error processing job: [{}]'.format(body), exc_info=True)


consume_individually()
