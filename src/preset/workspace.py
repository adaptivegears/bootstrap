import os
import shutil
import sys

WORKSPACE_INVENTORY = lambda w: os.path.join(w.workdir, 'inventory')
WORKSPACE_HOSTS = lambda w: os.path.join(w.workdir, 'inventory', 'hosts')
WORKSPACE_HOSTVARS = lambda w: os.path.join(w.workdir, 'inventory', 'host_vars')
WORKSPACE_LOCALHOST = lambda w: os.path.join(w.workdir, 'inventory', 'host_vars', 'localhost.yml')

WORKSPACE_PROJECT = lambda w: os.path.join(w.workdir, 'project')
WORKSPACE_PLAYBOOK = lambda w: os.path.join(w.workdir, 'project', 'playbook.yml')
WORKSPACE_ROLES = lambda w: os.path.join(w.workdir, 'project', 'roles')
WORKSPACE_PLUGINS = lambda w: os.path.join(w.workdir, 'project', 'plugins')

WORKSPACE_REQUIREMENTS = lambda w: os.path.join(w.workdir, 'requirements.yml')



def clone(ws):
    # requirements
    requirements = None
    for r in ['requirements.yml', 'requirements.yaml']:
        if os.path.exists(os.path.join(ws.ansible.collection, r)):
            requirements = os.path.join(ws.ansible.collection, r)
            break
    if requirements:
        shutil.copy2(requirements, WORKSPACE_REQUIREMENTS(ws))

    # inventory
    os.makedirs(WORKSPACE_INVENTORY(ws), exist_ok=True)
    with open(WORKSPACE_HOSTS(ws), 'w') as f:
        f.write('localhost')
    os.makedirs(WORKSPACE_HOSTVARS(ws), exist_ok=True)
    with open(WORKSPACE_LOCALHOST(ws), 'w') as f:
        f.write('---\n')
        f.write('ansible_connection: local\n')
        f.write(f'ansible_python_interpreter: {sys.executable}')

    # project
    os.makedirs(WORKSPACE_PROJECT(ws), exist_ok=True)
    shutil.copy2(ws.ansible.playbook, WORKSPACE_PLAYBOOK(ws))

    roles = os.path.join(ws.ansible.collection, 'roles')
    if os.path.exists(roles):
        shutil.copytree(roles, WORKSPACE_ROLES(ws))

    plugins = os.path.join(ws.ansible.collection, 'plugins')
    if os.path.exists(plugins):
        shutil.copytree(plugins, WORKSPACE_PLUGINS(ws))
