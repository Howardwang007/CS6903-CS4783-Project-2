from Crypto.Util import number

for n in range(5, 10):
	if n == 65:
		n = 64
	print("Number of bits",n)
	server_x = number.getRandomNBitInteger(n)
	server_y = number.getRandomNBitInteger(n)
	print("Server:",server_x,server_y)
	alice_d = number.getRandomNBitInteger(n)
	alice_x = number.getRandomNBitInteger(n)
	alice_y = number.getRandomNBitInteger(n)
	print("Alice:",alice_d,alice_x,alice_y)
	bob_d = number.getRandomNBitInteger(n)
	bob_x = number.getRandomNBitInteger(n)
	bob_y = number.getRandomNBitInteger(n)
	print("Bob:",bob_d,bob_x,bob_y)
	p = number.getPrime(n)
	q = number.getPrime(n)
	e = 17
	d = pow(e,-1,(p-1)*(q-1))
	print("Key:",e,d,p*q)