import os
import time
from app import queue_info
from app import k8s_wrapper
from app import job_info
from log import logger


rabbitmq_url = os.getenv('AMQP_URL')
logger.info('Connecting to RabbitMQ at {}'.format(rabbitmq_url))

scale_out_cooldown_seconds = int(os.getenv('SCALE_OUT_COOLDOWN_SECONDS'))
scale_in_cooldown_seconds = int(os.getenv('SCALE_IN_COOLDOWN_SECONDS'))
max_replicas = int(os.getenv('MAX_REPLICAS'))

autoscaler = k8s_wrapper.K8sAutoScaler({
    'kubernetes_namespace': os.getenv('K8S_NAMESPACE'),
    'kubernetes_deployment': 'worker',
})

last_scale_in_time = 0
last_scale_out_time = 0

while True:
    try:
        num_msg_in_queue = queue_info.get_queue_length(rabbitmq_url, 'jobs')
        num_replicas = autoscaler.get_current_replica_count()
        num_jobs_incomplete = job_info.get_incomplete_jobs_count()

        logger.info('Jobs incomplete/Messages in queue/Available replicas: {}/{}/{}'.format(num_jobs_incomplete, num_msg_in_queue, num_replicas))

        current_time = time.time()
        if num_msg_in_queue > 0:
            scale_out = True

            if num_replicas >= max_replicas:
                scale_out = False
            if current_time - last_scale_out_time <= scale_out_cooldown_seconds:
                scale_out = False
            if num_replicas >= num_jobs_incomplete:
                # This would be the case when the deployment was scaled, the node pool scaled out but the node isn't ready yet
                scale_out = False

            if scale_out:
                autoscaler.scale_out()
                last_scale_out_time = time.time()

        if num_msg_in_queue == 0:
            scale_in = True

            if num_replicas == 0:
                scale_in = False
            if current_time - last_scale_in_time <= scale_in_cooldown_seconds:
                scale_in = False
            if num_jobs_incomplete > 0:
                # Until we've figured out how to avoid killing work in progress
                scale_in = False

            if scale_in:
                autoscaler.scale_in()
                last_scale_in_time = time.time()

        time.sleep(1)
    except Exception:
        logger.error('Error', exc_info=True)
        time.sleep(3)
