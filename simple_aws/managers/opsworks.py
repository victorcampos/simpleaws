#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from boto.opsworks.layer1 import OpsWorksConnection


class OpsWorksInstanceManager:

    def __init__(self, layer_id=None, offline=False):
        self.layer_id = layer_id
        self.show_offline = offline
        self.instances = []


    def list_instances(self, layer_id):
        connection = OpsWorksConnection(aws_access_key_id='',
                aws_secret_access_key='')

        self.instances = connection.describe_instances(layer_id=self.layer_id)['Instances']

        return self.instances


    def print_instances(self):
        instances = self.list_instances(self.layer_id)

        for (counter, instance) in enumerate(instances):
            if not self.show_offline and instance['Status'] == 'online':
               print "%d) %s" % (counter, instance[u'Hostname'])


    def connect_to_instance(self, instance_index):
        instance = self.instances[instance_index]
        hostname = "ubuntu@%s" % instance[u'PublicDns']
        

        ssh_command = "ssh -i %s %s" % (ssh_key_path, hostname)
        os.system("osascript -e 'tell app \"Terminal\"\n do script \"%s\" \nend tell'" % ssh_command)
#        env = {}
#
#        subprocess.Popen(['ssh', '-i', ssh_key_path, hostname],
#                stdin=subprocess.PIPE,
#                stdout=subprocess.PIPE,
#                stderr=subprocess.PIPE,
#                env=env,
#                preexec_fn=os.setsid
#                )



if __name__ == "__main__":
    main()
