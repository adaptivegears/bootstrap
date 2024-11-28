import collections
import os
import sys
import tempfile
import shutil
import subprocess
import json

from .arguments import parse_arguments

Preset = collections.namedtuple('Preset', ['collection', 'playbook', 'extra_vars'])

USERDIR = os.environ['USER_PWD']
PYTHONBIN = os.environ['PYTHONBIN']


def parse_preset():
    if len(sys.argv) < 3:
        print('Usage: preset <collection> <playbook> [extra_vars]')
        sys.exit(1)
    args = sys.argv[1:]
    collection = args[0]
    playbook = args[1]
    extra_vars = parse_arguments(sys.argv[2:])
    extra_vars = json.dumps(extra_vars)
    return Preset(collection, playbook, extra_vars)


def execute(workspace, extra_vars):
    if os.path.exists(os.path.join(workspace, 'requirements.yml')):
        galaxy = os.path.join(PYTHONBIN, 'ansible-galaxy')
        rc = subprocess.run(
            f'{galaxy} collection install -r requirements.yml',
            cwd=workspace,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            bufsize=1
        ).returncode
        if rc != 0:
            raise RuntimeError('Failed to install collection dependencies')

    os.environ['ANSIBLE_INVENTORY'] = os.path.join(workspace, 'hosts')

    ansible = os.path.join(PYTHONBIN, 'ansible-playbook')
    playbook = os.path.join(workspace, 'playbook.yml')

    rc = subprocess.run(
        f'{ansible} {playbook} --extra-vars \'{extra_vars}\'',
        cwd=workspace,
        env=os.environ,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        bufsize=1
    ).returncode
    print(f'Ansible return code: {rc}')

    return 0


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


def process(workspace, preset):
    if os.path.isabs(preset.collection):
        collection = preset.collection
    else:
        collection = os.path.join(USERDIR, preset.collection)

    if not (os.path.exists(collection) and os.path.isdir(collection)):
        raise FileNotFoundError(f'Collection not found: {collection}')

    if not os.access(collection, os.R_OK):
        raise PermissionError(f'Collection is not readable: {collection}')

    if os.path.isabs(preset.playbook):
        playbook = preset.playbook
    else:
        playbook = os.path.join(USERDIR, preset.playbook)

    if not (os.path.exists(playbook) and os.path.isfile(playbook)):
        raise FileNotFoundError(f'Playbook not found: {playbook}')

    if not os.access(playbook, os.R_OK):
        raise PermissionError(f'Playbook is not readable: {playbook}')

    clone(workspace, collection, playbook)
    return execute(workspace, preset.extra_vars)


def main():
    preset = parse_preset()
    with tempfile.TemporaryDirectory(prefix='preset-') as workspace:
        process(workspace, preset)

if __name__ == '__main__':
    main()
