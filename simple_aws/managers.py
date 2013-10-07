#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from boto.opsworks.layer1 import OpsWorksConnection


class OpsWorksInstanceManager:

    def __init__(self, aws_access_key_id=None,
                 aws_secret_access_key=None,
                 layer_id=None,
                 offline=False):
        self.connection = OpsWorksConnection(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)
        self.layer_id = layer_id
        self.show_offline = offline

        self.instances = []

    def list_instances(self):
        self.instances = self.connection.describe_instances(
            layer_id=self.layer_id)['Instances']

        return self.instances

    def print_instances(self):
        instances = self.list_instances(self.layer_id)

        for (counter, instance) in enumerate(instances):
            if not self.show_offline and instance['Status'] == 'online':
                print "%d) %s" % (counter, instance[u'Hostname'])