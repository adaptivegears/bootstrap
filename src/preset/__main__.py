import os
import sys
import tempfile
import subprocess
import json
import ansible_runner

from . import cli
from . import workspace
from . import types


PYTHONBIN = os.environ['PYTHONBIN']
ANSIBLE_GALAXY = os.path.join(PYTHONBIN, 'ansible-galaxy')
ANSIBLE_PLAYBOOK = os.path.join(PYTHONBIN, 'ansible-playbook')

def execute(ws):
    if os.path.exists(os.path.join(ws.workdir, 'requirements.yml')):
        rc = subprocess.run(
            f'{ANSIBLE_GALAXY} collection install -r requirements.yml',
            cwd=ws,
            env=os.environ,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            bufsize=1
        ).returncode
        if rc != 0:
            raise RuntimeError('Failed to install collection dependencies')

    os.environ['ANSIBLE_INVENTORY'] = os.path.join(ws.workdir, 'hosts')

    with open(os.path.join(ws.workdir, 'variables.json'), 'w') as f:
        f.write(json.dumps(ws.ansible.variables))

    ansible_runner.run(
        private_data_dir=ws.workdir,
        playbook=ws.ansible.playbook,
        extravars=ws.ansible.variables,
        inventory=ws.workdir,
        rotate_artifacts=1,
        quiet=False,
        json_mode=True
    )

    return 0


def main():
    ansible = cli.parse()
    with tempfile.TemporaryDirectory(prefix='preset-') as workdir:
        ws = types.Workspace(workdir, ansible)
        workspace.clone(ws)
        execute(ws)

if __name__ == '__main__':
    main()
