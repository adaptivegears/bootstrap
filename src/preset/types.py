import collections

Preset = collections.namedtuple('Preset', ['collection', 'playbook', 'extra_vars'])

Workspace = collections.namedtuple('Workspace', ['path', 'preset'])
