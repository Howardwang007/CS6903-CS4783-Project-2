from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import struct
import socket
import json
import time
import os

number_size = 0
with open('number_size', 'r') as f:
	number_size = int(f.read())

def randint(upper): #generate random number from 0 - upper
	upper += 1 #include upper
	num = 0
	while(num < upper):
		num <<= 32
		num += struct.unpack('I', os.urandom(4))[0]
	return num % (upper)

def generate_random_number(size):
	return randint((1 << size) - 1)

def replace(number, position, bit):
	if(bit == 1):
		return number | (1 << position)
	else:
		return number & ~(1 << position)

def setRandom(number, lower, upper):
	for i in range(lower, upper):
		number = replace(number, i, randint(1))
	return number

def getBit(number, position):
	return (number >> position) & 1

def calcBit(S, d, k, A):
	bit = 1
	for i in range(0, d - 1):
		bit ^= getBit(S[i], k - 1)
	for i in range(0, d):
		bit ^= getBit(A[i][1], k - 1)
	S[d - 1] = replace(S[d - 1], k - 1, bit)

	bit = 1
	for i in range(0, d - 1):
		bit ^= getBit(S[i], k - 2)
	for i in range(0, d):
		bit ^= getBit(A[i][1], k - 2)
	S[d - 1] = replace(S[d - 1], k - 2, bit)

	return S

def leftrot(number, bit, size):
	bit %= size
	return ((number << bit) | (number >> (size - bit))) & ((1 << size) - 1)

def calcS(S, r, d, k):
	res = 0
	for i in range(0, d):
		res ^= S[i]

	return leftrot(res, r, k)

def getAnswerBit(number):
	max_zeros = 0
	zeros = 0
	answer_bit = 0
	for i in range(len(number)):
		if(number[i] == '0'):
			zeros +=1
		else:
			if(zeros > max_zeros):
				max_zeros = zeros
				answer_bit = number[(i + 1) % len(number)]
			zeros = 0

	return answer_bit

class Bob:
	def __init__(self, num):
		self.d = number_size
		self.num = num
		self.cur = 0
		self.res = 0

	def init(self):
		self.k = generate_random_number(128)

	def getX(self, X):
		self.X = X

	def getInfo(self, info):
		self.public_key = info[0]
		self.module = info[1]
		self.key_size = info[2]
		self.S_xor = info[3]

	def sendV(self):
		self.b = getBit(self.num, self.cur)
		self.cur += 1
		return ((self.X[self.b]
				+pow(self.k,
					 self.public_key,
					 self.module))
				%self.module)

	def getMsg(self, msg):
		self.res ^= ((msg[self.b] - self.k))

	def getSxor(self, Sxor):
		self.S_xor = Sxor

	def getResult(self):
		self.res ^= self.S_xor

		self.res = bin(self.res)[2:]
		while(len(self.res) < self.key_size):
			self.res = '0' + self.res

		if(getAnswerBit(self.res) == '1'):
			return 'Alice'
		else:
			return 'Bob'

	def getNumber(self):
		return self.num

def main():
	B = Bob(int(input('Input Bob\'s number: ')))
	
	s = socket.socket()
	port = 0
	with open('port_number', 'r') as f:
		port = int(f.read())
	s.connect(('127.0.0.1', port))

	B.getInfo(json.loads(s.recv(2048).decode()))

	for i in range(number_size):
		B.init()
		B.getX(json.loads(s.recv(2048).decode()))
		s.send(str(B.sendV()).encode('UTF-8'))
		B.getMsg(json.loads(s.recv(2048).decode()))
		time.sleep(0.01)

	result = B.getResult()
	s.send(result.encode('UTF-8'))
	s.close()

	#print(f'Bob Number: {B.getNumber()}')
	print(f'{result} is larger')

if __name__ == '__main__':
	main()
