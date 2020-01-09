from app import app
import json
from flask import request
from app import work_queue
import datetime
from log import logger

next_id = 0
jobs = []


@app.route('/status')
def status():
    return '{}', 200


def get_next_id():
    global next_id
    next_id = next_id + 1
    return next_id


@app.route('/', methods=['GET'])
def get_root():
    return '', 200


@app.route('/jobs', methods=['GET'])
def get_jobs():
    return json.dumps(jobs, indent=3), 200


@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job = {
        'id': get_next_id(),
        'name': data['name'],
        'status': 'created',
        'parameters': data['parameters']
    }
    work_queue.publish_job(job)
    job['created_utc'] = datetime.datetime.now().replace(microsecond=0).isoformat()

    jobs.append(job)
    return json.dumps(job, indent=3), 201


@app.route('/jobs', methods=['DELETE'])
def delete_jobs():
    jobs.clear()
    return '', 204


@app.route('/jobs/<job_id>', methods=['PATCH'])
def update_status(job_id):
    data = request.get_json()
    logger.debug('Updating job {}'.format(job_id))
    job = [job for job in jobs if job['id'] == int(job_id)][0]
    job['status'] = data['status']
    job['updated_utc'] = datetime.datetime.now().replace(microsecond=0).isoformat()
    if 'metadata' in data:
        job['metadata'] = data['metadata']
    if job['status'] == 'done':
        job['done_utc'] = datetime.datetime.now().replace(microsecond=0).isoformat()
    return json.dumps(job, indent=3), 200
