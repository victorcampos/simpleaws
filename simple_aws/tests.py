# -*- coding: utf-8 -*-

import unittest
from mock import patch, call

from managers import OpsWorksInstanceManager, EC2InstanceManager
from main import get_execution_command, connect_to_instance


class OpsWorksManagerTest(unittest.TestCase):

    def test_connection_with_aws_keys(self):
        with patch('managers.OpsWorksConnection') as connection_mock:
            OpsWorksInstanceManager(aws_access_key_id='test',
                                    aws_secret_access_key='test')

            expected = [call(aws_access_key_id='test',
                             aws_secret_access_key='test')]
            self.assertEqual(expected, connection_mock.mock_calls)

    def test_list_instances_calls_describe_instances_with_layer_id(self):
        with patch('managers.OpsWorksConnection') as connection_mock:
            manager = OpsWorksInstanceManager(aws_access_key_id='test',
                                              aws_secret_access_key='test',
                                              layer_id='test')
            manager.list_instances()

            self.assertTrue(
                call().describe_instances(layer_id='test') in
                connection_mock.mock_calls)

    def test_list_instances_generate_list_of_online_instances(self):
        with patch('managers.OpsWorksConnection') as connection_mock:
            conn_instance = connection_mock.return_value
            conn_instance.describe_instances.return_value = {
                'Instances': [
                    {'Status': 'online'},
                    {'Status': 'online'},
                    {'Status': 'offline'}
                ]
            }

            manager = OpsWorksInstanceManager(aws_access_key_id='test',
                                              aws_secret_access_key='test',
                                              layer_id='test')
            instances = manager.list_instances()

            self.assertEqual(2, len(instances))

    def test_list_instances_generate_list_with_offline_instances(self):
        with patch('managers.OpsWorksConnection') as connection_mock:
            conn_instance = connection_mock.return_value
            conn_instance.describe_instances.return_value = {
                'Instances': [
                    {'Status': 'online'},
                    {'Status': 'online'},
                    {'Status': 'offline'}
                ]
            }

            manager = OpsWorksInstanceManager(aws_access_key_id='test',
                                              aws_secret_access_key='test',
                                              layer_id='test', offline=True)
            instances = manager.list_instances()

            self.assertEqual(3, len(instances))


class EC2InstanceManagerTests(unittest.TestCase):

    def test_list_instances_named(self):
        with patch('managers.EC2Connection') as connection_mock:
            manager = EC2InstanceManager(aws_access_key_id='test',
                                         aws_secret_access_key='test')

            manager.list_instances_named('test')

            self.assertTrue(call().get_only_instances(
                filters={'tag:Name': 'test*'}) in connection_mock.mock_calls)


class MainTests(unittest.TestCase):

    def test_get_execution_command(self):
        config = {'ssh': {'user': 'test', 'key_path': 'test_path'}}

        command = get_execution_command('test', config)
        self.assertEqual('ssh -i test_path test@test', command)

    def test_connect_to_instance_command_execution(self):
        with patch('main.os') as mocked_os:
            config = {'ssh': {'user': 'test',
                              'key_path': 'test_path',
                              'command': 'command_test $ssh_command'}}

            connect_to_instance('test', config)
            self.assertTrue(
                call.system('command_test ssh -i test_path test@test') in
                mocked_os.mock_calls)


if __name__ == '__main__':
    unittest.main()