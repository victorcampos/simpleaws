# -*- coding: utf-8 -*-

import unittest
from mock import patch, call

from managers import OpsWorksInstanceManager
from main import get_execution_command, connect_to_instance


class OpsWorksManagerTest(unittest.TestCase):

    def test_connection_with_aws_keys(self):
        with patch('managers.OpsWorksConnection') as connection_mock:
            OpsWorksInstanceManager(aws_access_key_id='test',
                                    aws_secret_access_key='test')

            expected = [call(aws_access_key_id='test',
                             aws_secret_access_key='test')]
            self.assertEqual(expected, connection_mock.mock_calls)

    def test_list_instances(self):
        with patch('managers.OpsWorksConnection') as connection_mock:
            manager = OpsWorksInstanceManager(aws_access_key_id='test',
                                              aws_secret_access_key='test',
                                              layer_id='test')
            manager.list_instances()

            self.assertTrue(
                call().describe_instances(layer_id='test') in
                connection_mock.mock_calls)


class MainTests(unittest.TestCase):

    def test_get_execution_command(self):
        instance = {u'PublicDns': 'test'}
        config = {'ssh': {'user': 'test', 'key_path': 'test_path'}}

        command = get_execution_command(instance, config)
        self.assertEqual('ssh -i test_path test@test', command)

    def test_connect_to_instance_command_execution(self):
        with patch('main.os') as mocked_os:
            instance = {u'PublicDns': 'test'}
            config = {'ssh': {'user': 'test',
                              'key_path': 'test_path',
                              'command': 'command_test $ssh_command'}}

            connect_to_instance(instance, config)
            self.assertTrue(
                call.system('command_test ssh -i test_path test@test') in
                mocked_os.mock_calls)


if __name__ == '__main__':
    unittest.main()