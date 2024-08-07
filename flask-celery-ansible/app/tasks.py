import subprocess
import yaml
from pathlib import Path
from .extensions import celery

@celery.task(bind=True)
def run_ansible_playbook(self):
    playbook_path = Path('app/playbooks/playbook.yml')

    try:
        with playbook_path.open() as f:
            playbook_data = yaml.safe_load(f)
            total_tasks = sum(len(play.get('tasks', [])) for play in playbook_data)
    except Exception as e:
        raise Exception(f"Error loading playbook: {e}")

    try:
        process = subprocess.Popen(
            ['ansible-playbook', str(playbook_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        raise Exception(f"Error running playbook: {e}")

    completed_tasks = 0

    for line in process.stdout:
        if 'TASK [' in line:
            completed_tasks += 1
            task_name = line.split('TASK [')[1].split(']')[0].strip()
            progress = int((completed_tasks / total_tasks) * 100)
            self.update_state(state='PROGRESS', meta={'output': f"Running task: {task_name}", 'progress': progress})

    process.wait()

    if process.returncode != 0:
        error_output = process.stderr.read()
        raise Exception(f"Playbook failed: {error_output}")

    return {'status': 'Playbook completed successfully!', 'progress': 100}
