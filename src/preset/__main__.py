import os
import sys
import tempfile
import subprocess
import json
import ansible_runner

from . import cli
from . import workspace
from . import types


def execute(ws):
    if os.path.exists(os.path.join(ws.workdir, 'requirements.yml')):
        stdout, stderr, rc = ansible_runner.run_command(
            host_cwd=ws.workdir,
            executable_cmd='ansible-galaxy',
            cmdline_args=['collection', 'install', '-r', 'requirements.yml'],
            input_fd=sys.stdin,
            output_fd=sys.stdout,
            error_fd=sys.stderr,
            envvars=os.environ,
        )
        if rc != 0:
            raise RuntimeError('Failed to install collection dependencies')

    with open(os.path.join(ws.workdir, 'variables.json'), 'w') as f:
        f.write(json.dumps(ws.ansible.variables))

    ansible_runner.run(
        private_data_dir=ws.workdir,
        playbook='playbook.yml',
        extravars=ws.ansible.variables,
        limit='localhost',
        rotate_artifacts=1,
        quiet=False,
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
