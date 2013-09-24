#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from managers.opsworks import OpsWorksInstanceManager


def main():
    args = vars(parse_args())

    manager = OpsWorksInstanceManager(layer_id=args['layer_id'])
    manager.print_instances()
    instance_index = input("Choose an instance to connect: ")
    manager.connect_to_instance(instance_index)


def parse_args():
    parser = argparse.ArgumentParser(description='Connect to OpsWorks instances.')
    parser.add_argument('--layer', dest='layer_id', help='layer id to search for instances', required=True)
    parser.add_argument('--offline', dest='offline', type=bool, help='return offline instances?')

    args = parser.parse_args()

    return args
