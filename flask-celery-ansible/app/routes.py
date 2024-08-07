from flask import Blueprint, render_template, jsonify
from .tasks import run_ansible_playbook

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/start_task', methods=['POST'])
def start_task():
    task = run_ansible_playbook.apply_async()
    return jsonify({ 'task_id': task.id }), 202

@main.route('/task_status/<task_id>')
def task_status(task_id):
    task = run_ansible_playbook.AsyncResult(task_id)
    response = {
        'state': task.state,
        'info': task.info if task.state == 'PROGRESS' else str(task.info)
    }
    return jsonify(response)
