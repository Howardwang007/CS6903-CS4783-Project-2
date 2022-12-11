from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import struct
import socket
import time
import json
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

class Alice:
	def __init__(self, num):
		with open("./keypair.pem", "rb") as key_file:
		    self.private_key = serialization.load_pem_private_key(
		        key_file.read(),
		        password=None,
		    )

		with open("./publickey.crt", "rb") as key_file:
		    self.public_key = serialization.load_pem_public_key(
		        key_file.read(),
		    )


		self.d = number_size #max size of the number
		self.k = self.private_key.key_size #key size of oblivious transfer protocol
		self.num = num #alice's number

		self.A = [[0, 0] for _ in range(self.d)] #create 2*d matrix, each cell holds a k-bit number
		self.A_p = [[0, 0] for _ in range(self.d)]
		self.S = [0] * self.d;

		self.r = randint(2 * self.k - 1)
		self.s = randint(self.k >> 1) + (self.k >> 1) #choose a large enough s <= k

		for i in range(0, self.d):
			self.A[i][0] = (setRandom(self.A[i][0], self.s, self.k))
			self.A[i][1] = (setRandom(self.A[i][1], self.s, self.k)) #step 2.1

			l = (0 if (getBit(self.num, i) == 1) else 1)
			self.A[i][l] = (setRandom(self.A[i][l], 0, 2 * i)) #step 2.2

			self.A[i][l] = (replace(self.A[i][l], 2 * i + 1, 1))
			self.A[i][l] = (replace(self.A[i][l], 2 * i, getBit(self.num, i))) #step 2.3

			self.S[i] = generate_random_number(self.k) #step 2.4

		self.S = calcBit(self.S, self.d, self.k, self.A) #step 2.4

		for i in range(0, self.d):
			self.A_p[i][0] = (leftrot(self.A[i][0] ^ self.S[i], self.r, self.k))
			self.A_p[i][1] = (leftrot(self.A[i][1] ^ self.S[i], self.r, self.k))

		self.S_xor = calcS(self.S, self.r, self.d, self.k)
		self.cur = 0

	def init(self):
		self.x0 = generate_random_number(128)
		self.x1 = generate_random_number(128)

	def sendX(self):
		return (self.x0, self.x1)

	def sendInfo(self):
		return [self.public_key.public_numbers().e,
				self.public_key.public_numbers().n,
				self.public_key.key_size,
				self.S_xor]

	def getV(self, V):
		self.V = V

	def sendSxor(self):
		return self.S_xor

	def sendMsg(self):
		k0 = pow((self.V - self.x0),
				  self.private_key.private_numbers().d,
				  self.public_key.public_numbers().n)
		k1 = pow((self.V - self.x1),
				  self.private_key.private_numbers().d,
				  self.public_key.public_numbers().n)

		m0 = (self.A_p[self.cur][0]) + k0
		m1 = (self.A_p[self.cur][1]) + k1
		self.cur += 1

		return (m0, m1)

	def getNumber(self):
		return self.num

def main():
	A = Alice(int(input('Input Alice\'s number: ')))
	
	s = socket.socket()
	try:
		port = 0
		with open('port_number', 'r') as f:
			port = int(f.read())
	
		s.bind(('', port))
		 
		s.listen(5)
	
		(c, addr) = s.accept()
		c.send(json.dumps(A.sendInfo()).encode('UTF-8'))
		#print(addr)
		time.sleep(0.01)
	
		for i in range(number_size):
			A.init()
			c.send(json.dumps(A.sendX()).encode('UTF-8'))
			time.sleep(0.01)
			A.getV(int(c.recv(2048).decode()))
			c.send(json.dumps(A.sendMsg()).encode('UTF-8'))
			time.sleep(0.01)
	
		result = c.recv(2048).decode()
		c.close()
	
		#print(f'Alice Number: {A.getNumber()}')
		print(f'{result} is larger')
	finally:
		s.close()


if __name__ == '__main__':
	main()
