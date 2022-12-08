#!/usr/bin/python3
from socket import *
from threading import Thread
from config import client_user, alice, bob, HOST, PORT, ADDRESS, BUFSIZE, get_all_time
from datetime import datetime
import time
import math
import csv

# To hold clients

mydict = {}


class ClientHandler(Thread):

  def set_is_link_bob(self, value):
    for k, v in alice.items():
      if v['bob'] == self.user_name:
        alice[k]['is_link_bob'] = value

  def set_is_link_alice(self, value):
    for k, v in bob.items():
      if v['alice'] == self.user_name:
        bob[k]['is_link_alice'] = value

  def set_client_user_id(self):
    if self.clientname == 'Alice':
      # Assigning accounts to access from alice
      for name in alice:
        if alice[name].get('address') == None and self.user_name == '':
          self.user_name = name
          alice[name].setdefault('address', self._address[1])
          alice[name].setdefault('client', self._client)
          self.set_is_link_bob(True)
    if self.clientname == 'Bob':
      # Assigning accounts to access from bob
      for name in bob:
        if bob[name].get('address') == None and self.user_name == '':
          self.user_name = name
          bob[name].setdefault('address', self._address[1])
          bob[name].setdefault('client', self._client)
          self.set_is_link_alice(True)

  def __init__(self, client, address):
    global sockets
    global addresses
    Thread.__init__(self)
    self._client = client
    self._address = address
    self.user_name = ''
    self._close_time = None
    self._open_time = datetime.timestamp(datetime.now())

    sockets.append(self._client)
    addresses.append(self._address)

  def set_close_time(self):
    if self._close_time == None:
      self._close_time = datetime.timestamp(datetime.now())

  def send_other_client(self, data, start_time):

    if self.clientname == 'Alice':
      bob_name = alice[self.user_name]['bob']
      self.save_msg(start_time, name=bob_name, data=data)
      bob[bob_name]['client'].send(data)

    if self.clientname == 'Bob':
      alice_name = bob[self.user_name]['alice']
      self.save_msg(start_time, name=alice_name, data=data)
      alice[alice_name]['client'].send(data)

  def save_msg(self, start_time, name, data):
    global history_message
    end_time = datetime.timestamp(datetime.now())
    if history_message.get(self.user_name) == None:
      history_message.setdefault(self.user_name, [])
    history_message[self.user_name].append({
      'from': self.user_name,
      'to': name,
      'data': data,
      'start_time': start_time,
      'end_time': end_time,
      'delay': math.ceil(end_time - start_time)
    })

  def run(self):
    global all_time
    global history_message
    global server_x
    global server_y

    self._client.send(str.encode('Waiting for Clients : '))
    self.clientname = self._client.recv(BUFSIZE).decode()

    # Store and assign the name of the customer
    self.set_client_user_id()
    # Informs the user of the currently assigned name
    self._client.send(str.encode('name:{}'.format(self.user_name)))
    time.sleep(0.1)
    # Notification of linked client server coordinates
    self._client.send(str.encode('{0}'.format(server_x)))
    time.sleep(0.1)
    self._client.send(str.encode('{0}'.format(server_y)))
    # self._client.send(str.encode(server_y))

    time.sleep(0.2)
    # Matching Linked Information
    mydict[self.clientname] = self._address
    message = self._client.recv(BUFSIZE)  # Wait for ONLINE message
    message = message.decode()
    if not message:
      print('Client disconnected.')
      addIndex = sockets.index(self._client)
      del sockets[addIndex]
      del addresses[addIndex]
      self._client.close()
    else:
      try:
        if 'ONLINE#' in message:  # if client online
          while True:
            start_time = datetime.timestamp(datetime.now())
            data = self._client.recv(BUFSIZE)
            if data:
              time.sleep(0.5)
              # Sending data to associated objects
              self.send_other_client(data, start_time)
            else:
              # Set socket disconnect time
              self.set_close_time()
              self._client.close()
          else:
            # Set socket disconnect time
            self.set_close_time()
            self._client.close()
      except:
        if self._close_time:
          all_time[self.user_name] = math.ceil(self._close_time - self._open_time)
          print(history_message[self.user_name])
          print('Cumulative system delay time: {} s'.format(get_all_time(all_time)))
          with open('msg.csv', newline='', mode='w') as csvfile:
            fieldnames = ['from', 'to', 'data', 'start_time', 'end_time', 'delay']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for name in history_message:
              list = history_message[name]
              for city_info in list:
                writer.writerow(city_info)

server_x = int(input('Enter server x coordinates:'))
server_y = int(input('Enter server y coordinates:'))

server = socket(AF_INET, SOCK_STREAM)
print(ADDRESS)
server.bind(ADDRESS)
server.listen(20)
sockets = []
addresses = []
all_time = {}
history_message = {}
while True:
  print('Waiting for connection...')
  (client, address) = server.accept()
  print('...client connected from: ', client, address)
  handler = ClientHandler(client, address)
  handler.start()
server.close()