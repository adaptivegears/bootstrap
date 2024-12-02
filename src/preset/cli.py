import collections
import os
import re
import sys

Ansible = collections.namedtuple('Ansible', ['collection', 'playbook', 'variables'])

REGEX_KEY = re.compile(r'^--?([a-zA-Z0-9_\-]+)=?')
USERDIR = os.environ['USER_PWD']


def parse_arguments(argv):
    r = {}

    key = None
    while argv:
        arg = argv.pop(0)

        m = REGEX_KEY.match(arg)
        if m:
            if key:
                r[key] = True
            key = m.group(1)

            arg = arg.replace(m.group(0), "")
            if arg:
                argv.insert(0, arg)
        else:
            if key:
                r[key] = arg
                key = None
                continue
            else:
                # noop: value without key
                pass

    if key:
        r[key] = True

    out = {}
    for k, v in r.items():
        k = k.replace('-', '_')

        if isinstance(v, str) and v.isdigit():
            v = int(v)
        elif v == 'true':
            v = True
        elif v == 'false':
            v = False
        out[k] = v

    return out


def parse():
    if len(sys.argv) < 3:
        print('Usage: preset <collection> <playbook> [extra_vars]')
        sys.exit(1)
    argv = sys.argv[1:]

    collection = argv[0]
    if not os.path.isabs(collection):
        collection = os.path.join(USERDIR, collection)
    if not (os.path.exists(collection) and os.path.isdir(collection)):
        raise FileNotFoundError(f'Collection not found: {collection}')
    if not os.access(collection, os.R_OK):
        raise PermissionError(f'Collection is not readable: {collection}')

    playbook = argv[1]
    if not os.path.isabs(playbook):
        playbook = os.path.join(USERDIR, playbook)
    if not (os.path.exists(playbook) and os.path.isfile(playbook)):
        raise FileNotFoundError(f'Playbook not found: {playbook}')
    if not os.access(playbook, os.R_OK):
        raise PermissionError(f'Playbook is not readable: {playbook}')

    variables = parse_arguments(argv[2:])
    return Ansible(collection, playbook, variables)
