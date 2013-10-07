#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from string import Template

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from managers import OpsWorksInstanceManager


def main():
    args = vars(parse_args())

    config = read_config(args['config_path'])
    manager = OpsWorksInstanceManager(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_key_id'])

    manager.print_instances()

    instance_index = input("Choose an instance to connect: ")
    instance = manager.get_instance(instance_index)

    connect_to_instance(instance, config)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Connect to OpsWorks instances.')
    parser.add_argument('-c', '--config',
                        dest='config_path',
                        help='path to configuration file', required=True)
    parser.add_argument('-l', '--layer',
                        dest='layer_id',
                        help="""
                        layer id to search for instances
                        if different from specified in config.yml
                        """)
    parser.add_argument('--offline',
                        dest='offline',
                        type=bool, help='return offline instances?')

    args = parser.parse_args()

    return args


def read_config(config_path):
    return load(open(config_path), Loader=Loader)


def connect_to_instance(instance, config):
    ssh_command = get_execution_command(instance, config)
    command_template = Template(config['ssh']['command'])
    command = command_template.substitute(ssh_command=ssh_command)

    os.system(command)


def get_execution_command(instance, config):
    hostname = "%s@%s" % (config['ssh']['user'], instance[u'PublicDns'],)
    ssh_key_path = config['ssh']['key_path']

    ssh_command = "ssh -i %s %s" % (ssh_key_path, hostname)

    return ssh_command


if __name__ == "__main__":
    main()