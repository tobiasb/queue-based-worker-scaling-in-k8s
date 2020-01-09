from app import app
import json
from flask import request
from app import work_queue


@app.route('/status')
def status():
    return '{}'


next_id = 0
jobs = []


def get_next_id():
    global next_id
    next_id = next_id + 1
    return next_id


@app.route('/jobs', methods=['GET'])
def get_jobs():
    return json.dumps(jobs)


@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job = {
        'id': get_next_id(),
        'name': data['name'],
        'status': 'new',
        'parameters': data['parameters']
    }
    work_queue.publish_job(job)

    jobs.append(job)
    return json.dumps(data, indent=3)


@app.route('/jobs/<job_id>', methods=['PATCH'])
def update_status(job_id):
    data = request.get_json()
    print('Updating job {}'.format(job_id))
    job = [job for job in jobs if job['id'] == int(job_id)][0]
    job['status'] = data['status']
    job['result'] = data['result']
    return json.dumps(job)
