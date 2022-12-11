#!/usr/bin/python3
import socket
import pickle
import random
import time
import math

from config import BUFSIZE, ADDRESS, encryptDecrypt
from Crypto.Util import number

# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))

client.connect(ADDRESS)
# get: 1
response = client.recv(BUFSIZE)
print(response.decode())

# send client name
# send: 2
client.send(str.encode('Bob'))
# response = client.recv(BUFSIZE)
# response = client.recv(BUFSIZE)
# Current User ID
# get: 3
response = client.recv(BUFSIZE)
user_name = str(response.decode())
if user_name != None and user_name.find('name:') > -1:
  user_name = user_name.replace(r'name:', '')
print('user name: {}'.format(user_name))

# Server coordinates
server_x = client.recv(BUFSIZE).decode()
server_x = int(server_x)
server_y = client.recv(BUFSIZE).decode()
server_y = int(server_y)
print(server_x)
print(server_y)

# send online message

client.send(str.encode('ONLINE#'))

bob_distance = int(input('Enter bob distance between server(RSU): '))
# Compare distances
# bob_y = int(input('Enter bob y of Alice bob_y (within 1 <= x <= {0}) :'.format(bob_distance)))
# bob_x = int(input('Enter bob y of Alice bob_x (within 1 <= x <= {0}) :'.format(bob_distance)))

bob_x = int(input('Enter bob y coordinate (within 1 <= x): '))
bob_y = int(input('Enter bob y coordinate (within 1 <= y): '))

# bob_z = int(input('Enter bob y of Alice bob_z (within 1 <=x<= 300) :'))

# y = math.ceil(math.sqrt(bob_y * bob_y + bob_x * bob_x + bob_z * bob_z))
# if y > 300:
#     client.send(str.encode(str('faraway')))
# else:
#     client.send(str.encode(str('step')))
if abs(bob_x - server_x) > bob_distance or abs(bob_y - server_y) > bob_distance:
  time.sleep(0.3)
  client.send(str.encode(str('faraway')))
else:
  time.sleep(0.3)
  client.send(str.encode(str('step')))

# Input global range
r1 = 1
r2 = 10

# Input y, secret value

# y = int(input('Enter value of Bob secret y (within 1 <=x<= 20) :  '))

# Input e

e = int(input('Enter public key of Bob e = '))

# Send e
time.sleep(0.3)
client.send(str.encode(str(e)))
print('Public key e sent ...')
d = int(input('Enter private key of Bob d = '))

# Send n
n = int(input('Enter n  (within x>= {0}) '.format(bob_distance)))
if n < bob_distance:
  print('n < {0}'.format(bob_distance))
  client.close()
time.sleep(0.2)
print(90, n)
client.send(str.encode('{}'.format(n)))
print('Public key n sent ...')
time.sleep(0.2)

# Public key of Bob

publicKeyBob = [e, n]

# Private key of Bob

privateKeyBob = [d, n]

# Receive size of random number to generate prime
m1 = client.recv(BUFSIZE)
m1 = m1.decode()
m1 = int(m1)
# Receive C = C-X


# c_z1 = client.recv(BUFSIZE)
# c_z1 = int(c_z1.decode())
# time.sleep(0.5)
c_x1 = client.recv(BUFSIZE)
c_x1 = int(c_x1.decode())
print('c_x1', c_x1)

c_y1 = client.recv(BUFSIZE)
c_y1 = int(c_y1.decode())
print('c_y1', c_y1)
print('Received c from Alice ...', )
time.sleep(0.4)
client.send(str.encode(user_name))
print('Received size of prime number ... ')


# time.sleep(0.5)

# Send sequence
def secret_num(num, a_c):
  rangeN = r2 + r1 - 1
  n = [0] * (rangeN + 1)
  for i in range(1, len(n)):
    n[i] = encryptDecrypt(a_c + i, privateKeyBob)
  m = n[1:]
  # Choose a large prime p (<M1); Bob can know the size of M1
  primes = [number.getPrime(m1 - 1) for i in range(100)]
  z = [0] * rangeN
  prime = random.choice(primes)
  primes.remove(prime)
  for i in range(0, len(m)):
    z[i] = m[i] % prime
  condt = 0
  while condt == 0:
    for i in range(0, len(m)):
      for j in range(i + 1, len(m)):
        if abs(z[i] - z[j]) < 2:
          condt = 0
    if condt == 1:
      for i in range(0, len(m)):
        if z[i] >= prime or z[i] <= 0:
          condt = 0
    if condt == 0:
      if primes:
        prime = random.choice(primes)
        # If conditions fails repeat the process
        primes.remove(prime)
        for i in range(0, len(m)):
          z[i] = m[i] % prime
      else:
        break
    for i in range(num, len(z)):
      z[i] = z[i] + 1
    z.insert(len(z), prime)
  return pickle.dumps(z)
  # sequence

print(c_x1)
print(c_y1)
x1 = secret_num(num=bob_x, a_c=c_x1)
print('x1', x1)
y1 = secret_num(num=bob_y, a_c=c_y1)
print('y1', y1)
# z1 = secret_num(bob_z, c_z1)
# z1 = secret_num(y)
# Large amount of data, pass encrypted data sequentially
time.sleep(0.3)
client.send(x1)
time.sleep(0.3)
client.send(y1)

# client.send(z1)
# time.sleep(0.5)
# client.send(secret_num(y))
print('Sequence sent to Alice ...')

# Send offline message
print('Received result : \n')
result = client.recv(BUFSIZE)
print(result.decode())
client.close()
