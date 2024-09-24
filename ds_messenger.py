# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Edward Zhang
# junz23@uci.edu
# 42058839

import socket
import ds_protocol 
import json

# SERVER_ADDRESS = "168.235.86.101"

PORT_NUMBER = 3021

MY_TOKEN = '3890d3f-5fa1-46ea-a07c-9754a502826f'

class DirectMessage(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently 
    supports two features : A timestamp property that is set upon instantiation and 
    when the entry object is set and an entry property that stores the post message.

    """
    def __init__(self, recipient= None, message:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self._message = message
        self.recipient = recipient

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, recipient=self.recipient, message=self._message, timestamp=self._timestamp)


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self._connection = self.connect_to_server(dsuserver)
    self._token = self._get_token(username, password)
    self._dsuserver = dsuserver


  def connect_to_server(self, dsuserver):
      server_address = (dsuserver, PORT_NUMBER)
      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect(server_address)
      return client_socket

  def _get_token(self, username, password):
      join_method = ds_protocol.join(username, password)
      print('Join Method: ' , join_method)

      # ---------
      self._connection.sendall(join_method)
      response1 = self._connection.recv(1024)
      decoded_response = response1.decode('utf-8')
      response = ds_protocol.extract_json(decoded_response)
      print(response)
      print("DATATUPLE: " , response)
      return response.token


  def _send_data(self, message):
    self._connection.sendall(message)


  def _receive_data(self):
    data = self._connection.recv(1024)
    return data


  def send(self, message:str, recipient:str) -> bool:
    try:
      message = ds_protocol.directmessage(self._token, message, recipient)
      self._send_data(message)

      response1 = self._receive_data()

      decoded_response = response1.decode('utf-8')
      
      extract_response = ds_protocol.extract_json(decoded_response)
      print(f"Received response:\n{response1.decode('utf-8')}")

      if extract_response.type_response == 'ok':
        return True
      
      else:
        return False
      
    except:
      return False

  def retrieve_new(self) -> list:
      message = ds_protocol.unread_messages(self._token)

      response1 = self._send_data(message)

      response1 = self._receive_data()

      extract_response = ds_protocol.extract_json(response1).message
      messages = []

      extract_response = json.loads(response1)
      extract_response = extract_response['response']['messages']
      for message in extract_response:
        direct_message = DirectMessage(message['from'], message['message'], message['timestamp'])
        messages.append(direct_message)
      
      return messages, extract_response
 
  def retrieve_all(self) -> list:
    message = ds_protocol.all_messages(self._token)

    response1 = self._send_data(message)

    response1 = self._receive_data()

    decoded_response = response1.decode('utf-8')
    print(decoded_response)
    extract_response = ds_protocol.extract_json(decoded_response).message
    print(extract_response)

    messages = []
    
    for message in extract_response:
      direct_message = DirectMessage()
      direct_message.recipient = message['from']
      direct_message._entry = message['message']
      direct_message._timestamp = message['timestamp']
      messages.append(direct_message)
   
    return messages
