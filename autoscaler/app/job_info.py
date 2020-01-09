import requests
import os
from log import logger


jobs_api_host = os.getenv('JOB_API_HOST')
logger.info('Job API host: {}'.format(jobs_api_host))


def get_incomplete_jobs_count():
    response = requests.get(jobs_api_host + '/jobs')
    jobs = response.json()

    return len([job for job in jobs if job['status'] in ['created', 'in_progress']])
