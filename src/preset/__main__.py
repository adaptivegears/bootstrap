import tempfile

from . import cli
from . import workspace


def main():
    ansible = cli.parse()
    with tempfile.TemporaryDirectory(prefix='preset-') as workdir:
        ws = workspace.Workspace(workdir, ansible)
        workspace.clone(ws)
        workspace.execute(ws)

if __name__ == '__main__':
    main()
