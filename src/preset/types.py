import collections

Ansible = collections.namedtuple('Ansible', ['collection', 'playbook', 'variables'])
Workspace = collections.namedtuple('Workspace', ['workdir', 'ansible'])
