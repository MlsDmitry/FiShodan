from os.path import join, dirname
from re import template
from flask import Blueprint, json, render_template, request, jsonify
from flask.wrappers import Response
from fish_shodan.app import celery

from fish_shodan.rpadml.index import verify_domain


bp = Blueprint('main_page', __name__)


@bp.route('/', methods=['GET'])
def root():
    print(request.method)
    if request.method == 'GET':
        return render_template('index.html')
    

@bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    if 'domains' not in data:
        return jsonify({}), 422
    ids = []
    for domain in data['domains'].split('\n'):
        task = verify_domain.apply_async([domain])
        ids.append(task.id)
        
    return jsonify({'task_ids': ids}), 201

    
@bp.route('/tasks/<string:task_ids>', methods=['GET'])
def task_status(task_ids):
    task = celery.AsyncResult(task_ids)
    results = {}
    for task_id in task_ids.split(';'):
        results[task_id] = {
            "task_id": task_id,
            "task_status": task.status,
            "task_result": task.result
        }
    return jsonify(results), 201