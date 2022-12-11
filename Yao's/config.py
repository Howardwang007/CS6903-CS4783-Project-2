import datetime


class client_user:
  def __init__(self, name, start_time):
    self.name = name
    self.start_time = datetime.datetime.now()
    self.end_time = None

  def set_end_time(self):
    self.end_time = datetime.datetime.now()

  def get_time(self):
    return self.end_time - self.start_time


alice = {
  'a': {
    'bob': 'a1',
    'is_link_bob': False
  },
  'b': {
    'bob': 'b1',
    'is_link_bob': False
  },
  'c': {
    'bob': 'c1',
    'is_link_bob': False
  },
  'd': {
    'bob': 'd1',
    'is_link_bob': False
  },
  'e': {
    'bob': 'e1',
    'is_link_bob': False
  },
  'f': {
    'bob': 'f1',
    'is_link_bob': False
  },
  'g': {
    'bob': 'g1',
    'is_link_bob': False
  },
  'h': {
    'bob': 'h1',
    'is_link_bob': False
  },
  'i': {
    'bob': 'i1',
    'is_link_bob': False
  },
  'j': {
    'bob': 'j1',
    'is_link_bob': False
  }
}
bob = {
  'a1': {
    'alice': 'a',
    'is_link_alice': False
  },
  'b1': {
    'alice': 'b',
    'is_link_alice': False
  },
  'c1': {
    'alice': 'c',
    'is_link_alice': False
  },
  'd1': {
    'alice': 'd',
    'is_link_alice': False
  },
  'e1': {
    'alice': 'e',
    'is_link_alice': False
  },
  'f1': {
    'alice': 'f',
    'is_link_alice': False
  },
  'g1': {
    'alice': 'g',
    'is_link_alice': False
  },
  'h1': {
    'alice': 'h',
    'is_link_alice': False
  },
  'i1': {
    'alice': 'i',
    'is_link_alice': False
  },
  'j1': {
    'alice': 'j',
    'is_link_alice': False
  }
}

HOST = '127.0.0.1'
PORT = 1234
ADDRESS = (HOST, PORT)
BUFSIZE = 1024


def get_all_time(time_obj):
  new_time  = 0
  for k,v in time_obj.items():
    if len(k) == 2 and time_obj[k[0:1]]:
      if time_obj[k[0:1]] > v:
        new_time = new_time + v
      else:
        new_time = new_time + time_obj[k[0:1]]
  return new_time

def encryptDecrypt(message, key):
    c = pow(message, key[0]) % key[1]
    return c