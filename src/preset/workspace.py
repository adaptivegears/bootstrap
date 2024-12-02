import os
import shutil
import sys

WORKSPACE_PLAYBOOK = lambda w: os.path.join(w.workdir, 'playbook.yml')
WORKSPACE_REQUIREMENTS = lambda w: os.path.join(w.workdir, 'requirements.yml')
WORKSPACE_ROLES = lambda w: os.path.join(w.workdir, 'roles')
WORKSPACE_PLUGINS = lambda w: os.path.join(w.workdir, 'plugins')
WORKSPACE_HOSTVARS = lambda w: os.path.join(w.workdir, 'host_vars')
WORKSPACE_LOCALHOST = lambda w: os.path.join(w.workdir, 'host_vars', 'localhost.yml')
WORKSPACE_INVENTORY = lambda w: os.path.join(w.workdir, 'hosts')


def clone(ws):
    shutil.copy2(ws.ansible.playbook, WORKSPACE_PLAYBOOK(ws))

    requirements = None
    for r in ['requirements.yml', 'requirements.yaml']:
        if os.path.exists(os.path.join(ws.ansible.collection, r)):
            requirements = os.path.join(ws.ansible.collection, r)
            break
    if requirements:
        shutil.copy2(requirements, WORKSPACE_REQUIREMENTS(ws))

    roles = os.path.join(ws.ansible.collection, 'roles')
    if os.path.exists(roles):
        shutil.copytree(roles, WORKSPACE_ROLES(ws))

    plugins = os.path.join(ws.ansible.collection, 'plugins')
    if os.path.exists(plugins):
        shutil.copytree(plugins, os.path.join(ws.workdir, 'plugins'))

    os.makedirs(os.path.join(ws.workdir, 'host_vars'), exist_ok=True)
    with open(os.path.join(ws.workdir, 'host_vars', 'localhost.yml'), 'w') as f:
        f.write('---\n')
        f.write('ansible_connection: local\n')
        f.write(f'ansible_python_interpreter: {sys.executable}')

    with open(os.path.join(ws.workdir, 'hosts'), 'w') as f:
        f.write('localhost')
