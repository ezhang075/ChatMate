# Edward Zhang
# junz23@uci.edu
# 42058839

import unittest
import ds_protocol
import json
from collections import namedtuple


class TestProtocol(unittest.TestCase):
    def test_directmessage(self):
        user_token = 'token'
        entry = 'Hi alien!'
        recipient = 'jack'

        expected_result = json.dumps(
            {"token": user_token, "directmessage":
                {"entry": entry,
                    "recipient": recipient,
                    "timestamp": '1603167689.3928561'}}).encode('utf-8')
        self.assertEqual(ds_protocol.directmessage(
            user_token, entry, recipient), expected_result)

    def test_unread_messagse(self):
        user_token = 'token'

        expected_result = json.dumps(
            {"token": user_token, "directmessage": "new"}).encode('utf-8')
        self.assertEqual(
            ds_protocol.unread_messages(user_token), expected_result)

    def test_all_messages(self):
        user_token = 'token'

        expected_result = json.dumps(
            {"token": user_token,
                "directmessage": "all"}).encode('utf-8')
        self.assertEqual(ds_protocol.all_messages(user_token), expected_result)

    def test_extract_json(self):
        json_message = ('{"response": {"token": "123", "type": "success", '
                        '"messages": "Hi Alien!"}}')
        DataTuple = namedtuple(
            'DataTuple',
            ['token', 'type_response', 'message'])
        expected_result = DataTuple('123', 'success', 'Hi Alien!')
        self.assertEqual(ds_protocol.extract_json
                         (json_message), expected_result)


if __name__ == '__main__':
    unittest.main()
