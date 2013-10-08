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

from managers import OpsWorksInstanceManager, EC2InstanceManager


def main():
    args = vars(parse_args())

    config = read_config(args['config_path'])

    conn_type = args['service']

    if conn_type == 'ec2':
        ec2(args, config)
    elif conn_type == 'opsworks':
        opsworks(args, config)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Connect to OpsWorks instances.')

    parser.add_argument('service',
                        help='service to connect', choices=['ec2', 'opsworks'])
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


def ec2(args, config):
    manager = EC2InstanceManager(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'])

    search_query = raw_input("Search for name: ")
    manager.print_instances(search_query)

    instance_index = input("Choose an instance to connect: ")
    instance = manager.get_instance(instance_index - 1)

    connect_to_instance(instance.public_dns_name, config)


def opsworks(args, config):
    layer_id = config['layer_id'] if not args['layer_id'] else args['layer_id']

    manager = OpsWorksInstanceManager(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        layer_id=layer_id,
        offline=args['offline'])

    manager.print_instances()

    instance_index = input("Choose an instance to connect: ")
    instance = manager.get_instance(instance_index - 1)

    connect_to_instance(instance[u'PublicDns'], config)


def connect_to_instance(host, config):
    ssh_command = get_execution_command(host, config)
    command_template = Template(config['ssh']['command'])
    command = command_template.substitute(ssh_command=ssh_command)

    os.system(command)


def get_execution_command(host, config):
    hostname = "%s@%s" % (config['ssh']['user'], host,)
    ssh_key_path = config['ssh']['key_path']

    ssh_command = "ssh -i %s %s" % (ssh_key_path, hostname)

    return ssh_command


if __name__ == "__main__":
    main()