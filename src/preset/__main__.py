import os
import sys
import tempfile
import subprocess

from . import cli
from . import workspace


USERDIR = os.environ['USER_PWD']
PYTHONBIN = os.environ['PYTHONBIN']


def execute(ws, variables):
    if os.path.exists(os.path.join(ws, 'requirements.yml')):
        galaxy = os.path.join(PYTHONBIN, 'ansible-galaxy')
        rc = subprocess.run(
            f'{galaxy} collection install -r requirements.yml',
            cwd=ws,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            bufsize=1
        ).returncode
        if rc != 0:
            raise RuntimeError('Failed to install collection dependencies')

    os.environ['ANSIBLE_INVENTORY'] = os.path.join(ws, 'hosts')

    ansible = os.path.join(PYTHONBIN, 'ansible-playbook')
    playbook = os.path.join(ws, 'playbook.yml')

    rc = subprocess.run(
        f'{ansible} {playbook} --extra-vars \'{variables}\'',
        cwd=ws,
        env=os.environ,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        bufsize=1
    ).returncode
    print(f'Ansible return code: {rc}')

    return 0


def process(workdir, ansible):
    if os.path.isabs(ansible.collection):
        collection = ansible.collection
    else:
        collection = os.path.join(USERDIR, ansible.collection)

    if not (os.path.exists(collection) and os.path.isdir(collection)):
        raise FileNotFoundError(f'Collection not found: {collection}')

    if not os.access(collection, os.R_OK):
        raise PermissionError(f'Collection is not readable: {collection}')

    if os.path.isabs(ansible.playbook):
        playbook = ansible.playbook
    else:
        playbook = os.path.join(USERDIR, ansible.playbook)

    if not (os.path.exists(playbook) and os.path.isfile(playbook)):
        raise FileNotFoundError(f'Playbook not found: {playbook}')

    if not os.access(playbook, os.R_OK):
        raise PermissionError(f'Playbook is not readable: {playbook}')

    workspace.clone(workdir, collection, playbook)
    return execute(workdir, ansible.extra_vars)


def main():
    ansible = cli.parse()
    with tempfile.TemporaryDirectory(prefix='preset-') as workdir:
        process(workdir, ansible)

if __name__ == '__main__':
    main()
