# -*- coding: utf-8 -*-

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

        return self.instances

    def print_instances(self):
        instances = self.list_instances(self.layer_id)

        for counter, instance in enumerate(instances):
            print "%d) %s" % (counter, instance[u'Hostname'])