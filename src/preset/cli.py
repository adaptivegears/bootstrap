import re
import sys
import json

from . import types

REGEX_KEY = re.compile(r'^--?([a-zA-Z0-9_\-]+)=?')


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
    args = sys.argv[1:]
    collection = args[0]
    playbook = args[1]
    variables = parse_arguments(sys.argv[2:])
    variables = json.dumps(variables)
    return types.Ansible(collection, playbook, variables)
