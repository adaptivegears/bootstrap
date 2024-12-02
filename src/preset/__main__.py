import tempfile

from . import cli
from . import workspace


def main():
    with tempfile.TemporaryDirectory(prefix='preset-tmp-') as tempdir:
        ansible = cli.parse(tempdir=tempdir)
        with tempfile.TemporaryDirectory(prefix='preset-') as workdir:
            ws = workspace.Workspace(workdir, ansible)
            workspace.clone(ws)
            workspace.execute(ws)

if __name__ == '__main__':
    main()
