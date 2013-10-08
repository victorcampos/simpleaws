# -*- coding: utf-8 -*-

from operator import itemgetter

from boto.opsworks.layer1 import OpsWorksConnection
from boto.ec2.connection import EC2Connection


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

    def get_instance(self, instance_index):
        return self.instances[instance_index]

    def list_instances(self):
        instances = self.connection.describe_instances(
            layer_id=self.layer_id)['Instances']

        counter = 0
        for instance in instances:
            if self.show_offline or instance['Status'] == 'online':
                self.instances.append(instance)
                counter += 1

        self.instances = sorted(self.instances, key=itemgetter(u'Hostname'))

        return self.instances

    def print_instances(self):
        instances = self.list_instances()

        for counter, instance in enumerate(instances):
            print "%d) %s" % (counter + 1, instance[u'Hostname'])


class EC2InstanceManager:

    def __init__(self, aws_access_key_id=None,
                 aws_secret_access_key=None):
        self.connection = EC2Connection(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

        self.instances = []

    def get_instance(self, instance_index):
        return self.instances[instance_index]

    def list_instances_named(self, name, partial=True):
        instance_name = "%s*" % name if partial else name

        instances = self.connection.get_only_instances(
            filters={'tag:Name': instance_name})

        self.instances = sorted(instances, key=lambda k: k.tags['Name'])

        return self.instances

    def print_instances(self, name):
        instances = self.list_instances_named(name)

        for counter, instance in enumerate(instances):
            print "%d) %s" % (counter + 1, instance.tags['Name'])


