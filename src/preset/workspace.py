import os
import shutil
import sys


def clone(workspace, collection, playbook):
    if os.path.exists(playbook):
        shutil.copy2(playbook, os.path.join(workspace, 'playbook.yml'))
    else:
        raise FileNotFoundError(f'Playbook not found: {playbook}')

    requirements = None
    for r in ['requirements.yml', 'requirements.yaml']:
        if os.path.exists(os.path.join(collection, r)):
            requirements = os.path.join(collection, r)
            break
    if requirements:
        shutil.copy2(requirements, os.path.join(workspace, 'requirements.yml'))

    roles = os.path.join(collection, 'roles')
    if os.path.exists(roles):
        shutil.copytree(roles, os.path.join(workspace, 'roles'))

    plugins = os.path.join(collection, 'plugins')
    if os.path.exists(plugins):
        shutil.copytree(plugins, os.path.join(workspace, 'plugins'))

    os.makedirs(os.path.join(workspace, 'host_vars'), exist_ok=True)
    with open(os.path.join(workspace, 'host_vars', 'localhost.yml'), 'w') as f:
        f.write('---\n')
        f.write('ansible_connection: local\n')
        f.write(f'ansible_python_interpreter: {sys.executable}')

    with open(os.path.join(workspace, 'hosts'), 'w') as f:
        f.write('localhost')
