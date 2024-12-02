import tempfile

from . import cli
from . import workspace
from . import types


def main():
    ansible = cli.parse()
    with tempfile.TemporaryDirectory(prefix='preset-') as workdir:
        ws = types.Workspace(workdir, ansible)
        workspace.clone(ws)
        workspace.execute(ws)

if __name__ == '__main__':
    main()
