from os.path import join, dirname
from re import template
from flask import Blueprint, render_template, request, jsonify
from flask.wrappers import Response
from fish_shodan.app import celery

from fish_shodan.tasks import whois


bp = Blueprint('main_page', __name__)
# html_folder = join(dirname(dirname(__file__)), 'static')


@bp.route('/', methods=['GET'])
def root():
    print(request.method)
    if request.method == 'GET':
        return render_template('index.html')
    

@bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = whois.apply_async([1])
    print('created', data, task)
    return jsonify({'task_id': task.id}), 201

    
@bp.route('/tasks/<string:task_id>', methods=['GET'])
def task_status(task_id):
    print(task_id)
    task = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task.status,
        "task_result": task.result
    }
    return jsonify(result)