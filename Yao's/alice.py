#!/usr/bin/python3
import socket
import pickle
import random
import time
import math
from config import BUFSIZE, ADDRESS, encryptDecrypt

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(ADDRESS)
client.connect(ADDRESS)
response = client.recv(BUFSIZE)
client.send(str.encode('Alice'))
# Current User ID
response = client.recv(BUFSIZE)
user_name = str(response.decode())
if user_name != None and user_name.find('name:') > -1:
  user_name = user_name.replace(r'name:', '')
print('user name: {}'.format(user_name))

# Server coordinates
server_x = client.recv(BUFSIZE).decode()
server_x = int(server_x)
print(server_x)
server_y = client.recv(BUFSIZE).decode()
server_y = int(server_y)
print(server_y)

client.send(str.encode('ONLINE#'))

r1 = 1
r2 = 10
isFaraway = False
# Input value for Alice's secret
alice_distance = int(input('Enter bob distance between server(RSU): '))
# Compare distances
alice_x = int(input('Enter alice x coordinate (within 1 <= x ): '))
alice_y = int(input('Enter alice y coordinate (within 1 <= y ): '))
# alice_z = int(input('Enter alice y of Alice alice_z (within 1 <=x<= 300) :'))

# x = math.ceil(math.sqrt(alice_y * alice_y + alice_x * alice_x + alice_z * alice_z))
# if x > 300:
#     client.close()
if abs(alice_x - server_x) > alice_distance or abs(alice_y - server_y) > alice_distance:
  client.close()
# x = int(input('Enter value of Alice secret x (within 1 <=x<= 20) : '))
# client.send(str.encode('Alice。{}'.format(x)))
# time.sleep(0.3)
is_step = client.recv(BUFSIZE).decode()
if is_step == 'faraway':
  client.close()

print('test: ', is_step)
# bob Encryption
e = client.recv(BUFSIZE)
e = e.decode()
# Receive public key

print('Value of e received ... ', e)
time.sleep(0.2)
n = client.recv(BUFSIZE)
n = n.decode()
print('Value of n received ...')
e = int(e)
n = int(n)
publicKeyBob = [e, n]
print(('Received Public Key : ', publicKeyBob))

# Generate and send length of random number M1
N = n.bit_length()
m1 = random.SystemRandom().randint(0, (1 << N))
while m1 >= n:
  m1 = random.SystemRandom().randint(0, (1 << N))
N = m1.bit_length()
s = str(N)
client.send(str.encode(s))
print('size of random number shared ...')


def get_c(num):
  return str(abs(encryptDecrypt(m1, publicKeyBob) - num))


time.sleep(0.5)
c_x1 = get_c(alice_x)
print('c_x1', c_x1)
client.send(str.encode(c_x1))
time.sleep(0.5)
c_y1 = get_c(alice_y)
client.send(str.encode(c_y1))
print('c_y1', c_y1)
# Alice encrypts mi using publicKeyBob RSA

print('Value of C sent ...')

bob_name = client.recv(BUFSIZE)
try:
  bob_name = bob_name.decode()
except:
  print('')
# x1
x1 = client.recv(BUFSIZE)
x1 = pickle.loads(x1)
print('x1: ', x1)

# y1
y1 = client.recv(BUFSIZE)
y1 = pickle.loads(y1)
print('y1: ', y1)
# # z1
# z1 = client.recv(BUFSIZE)
# z1 = pickle.loads(z1)

# seq = client.recv(BUFSIZE)
# print(111, seq)
# seq = pickle.loads(seq)
# print(seq)
# prime = seq[len(seq) - 1]
print('Result : ')


def verify(s_m1, s_seq, numm):
  prime = s_seq[len(s_seq) - 1]
  return s_m1 % prime == s_seq[numm - 1]


result = ''
try:
  if verify(s_m1=m1, s_seq=x1, numm=alice_x) and verify(s_m1=m1, s_seq=y1, numm=alice_y):
    result = 'F'
    print(result)
  else:
    result = 'T'
    print(result)
except:
  result = 'F'
  print(result)
client.send(str.encode(result))
client.close()
