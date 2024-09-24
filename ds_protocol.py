# ds_protocol.py

# Starter code for assignment 4
# in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Edward Zhang
# junz23@uci.edu
# 42058839

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['token', 'type_response', 'message'])


def join(username, password):
    join_method = {"join": {"username": username,
                            "password": password, "token": ""}}
    join_method = json.dumps(join_method).encode('utf-8')
    return join_method


def post(user_token, entry, timestamp):
    post_method = {"token": user_token,
                   "post": {"entry": entry, "timestamp": timestamp}}
    post_method = json.dumps(post_method).encode('utf-8')
    return post_method


def bio(user_token, entry, timestamp):
    post_method = {"token": user_token,
                   "bio": {"entry": entry, "timestamp": timestamp}}
    post_method = json.dumps(post_method).encode('utf-8')
    return post_method


def directmessage(user_token, entry, recipient):
    message = {"token": user_token, "directmessage":
               {"entry": entry, "recipient": recipient,
                "timestamp": "1603167689.3928561"}}
    message = json.dumps(message).encode('utf-8')
    return message


def unread_messages(user_token):
    unread_message = {"token": user_token, "directmessage": "new"}
    unread_message = json.dumps(unread_message).encode('utf-8')
    return unread_message


def all_messages(user_token):
    all_message = {"token": user_token, "directmessage": "all"}
    all_message = json.dumps(all_message).encode('utf-8')
    return all_message


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string
    and convert it to a DataTuple object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''

    try:
        json_obj = json.loads(json_msg)

        token = json_obj['response'].get('token', '')
        type_response = json_obj['response']['type']
        message = json_obj['response'].get('messages', '')

        if message is None:
            message = json_obj['response'].get('messages', '')

    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(token, type_response, message)
