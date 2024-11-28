import re

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
    return r
