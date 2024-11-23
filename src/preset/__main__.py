import os
import argparse

WORKDIR = os.environ['WORKDIR']
USERDIR = os.environ['USER_PWD']

def main():
    parser = argparse.ArgumentParser(description='Preset')
    parser.add_argument('ansible_collection', type=str, help='Path to the Ansible Collection')
    parser.add_argument('ansible_playbook', type=str, help='Path to the Ansible Playbook')
    args = parser.parse_args()
    print(args.ansible_collection)
    print(args.ansible_playbook)

if __name__ == '__main__':
    main()
