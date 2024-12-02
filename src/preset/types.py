import collections

Ansible = collections.namedtuple('Ansible', ['collection', 'playbook', 'extra_vars'])
Workspace = collections.namedtuple('Workspace', ['path', 'preset'])
