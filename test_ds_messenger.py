# Edward Zhang
# junz23@uci.edu
# 42058839

import unittest
import ds_protocol
import json
from collections import namedtuple
import ds_messenger
import Profile
from pathlib import Path


class TestDSMessenger(unittest.TestCase):
    def test_connect_to_server(self):
        dsuserver = '168.235.86.101'
        username = 'jason10'
        password = 'jason10'

        direct_messenger = ds_messenger.DirectMessenger(
            dsuserver, username, password)
        self.assertTrue(direct_messenger._connection)

    def test_send_success(self):
        dsuserver = '168.235.86.101'
        username = 'jason10'
        password = 'jason10'

        direct_messenger = ds_messenger.DirectMessenger(
            dsuserver, username, password)
        sent_message = direct_messenger.send('Hello!', 'ohhimark')

        self.assertTrue(sent_message)

    def test_send_fail(self):
        dsuserver = '11213'
        username = 'jason100'
        password = 'jason100'

        direct_messenger = ds_messenger.DirectMessenger(
            dsuserver, username, password)
        sent_message = direct_messenger.send('Hello!', 'ohhimark')

        self.assertFalse(sent_message)

    # THIS ONE IS WRONG!!
    def test_retrieve_new(self):
        dsuserver1 = '168.235.86.101'
        username1 = 'jason10'
        password1 = 'jason10'

        dsuserver2 = '168.235.86.101'
        username2 = 'jason11'
        password2 = 'jason11'

        direct_messenger1 = ds_messenger.DirectMessenger(
            dsuserver1, username1, password1)
        direct_messenger2 = ds_messenger.DirectMessenger(
            dsuserver2, username2, password2)

        sent_message = direct_messenger1.send('Hello!', 'jason11')

        messages, extract_response = direct_messenger2.retrieve_new()
        print('EXTRACT RESPONSE: ', extract_response)
        print('MESSAGES: ', messages)

        self.assertTrue(direct_messenger2.retrieve_new())

    def test_retrieve_new_failure(self):
        dsuserver1 = '123'
        username1 = 'jason10'
        password1 = 'jason10'

        dsuserver2 = '123'
        username2 = 'jason11'
        password2 = 'jason11'

        direct_messenger1 = ds_messenger.DirectMessenger(
            dsuserver1, username1, password1)
        direct_messenger2 = ds_messenger.DirectMessenger(
            dsuserver2, username2, password2)

        sent_message = direct_messenger1.send('Hello!', 'jason11')

        messages, extract_response = direct_messenger2.retrieve_new()
        print('EXTRACT RESPONSE: ', extract_response)
        print('MESSAGES: ', messages)

        self.assertFalse(direct_messenger2.retrieve_new())


if __name__ == '__main__':
    unittest.main()
