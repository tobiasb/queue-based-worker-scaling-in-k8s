import pika
import os
import time
import json
import requests

jobs_api_host = os.getenv('JOBS_API_HOST')
print('Jobs API host: {}'.format(jobs_api_host))


def callback(ch, method, properties, body):
    data = json.loads(body)
    print('Received [{}]'.format(data))

    if 'delay' in data['parameters']:
        time.sleep(int(data['parameters']['delay']))

    job_id = str(data['id'])

    print('Notifying jobs API')
    response = requests.patch(jobs_api_host + '/jobs/' + job_id,
                               headers={'Content-Type': 'application/json'},
                               json={'status': 'done', 'result': 'https://cloud-storage-sample/' + job_id})

    print('API responded with ' + str(response.status_code))


rabbitmq_url = os.getenv('AMQP_URL')
print('Connecting to RabbitMQ at {}'.format(rabbitmq_url))

connection = None
channel = None

while connection is None:
    try:
        params = pika.ConnectionParameters(rabbitmq_url,
                                           heartbeat=600,
                                           blocked_connection_timeout=300)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue='jobs')
    except:
        print('Retrying to connect to queue')
        time.sleep(3)

channel.basic_consume(queue='jobs', auto_ack=True, on_message_callback=callback)
channel.start_consuming()
