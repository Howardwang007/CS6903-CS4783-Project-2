from subprocess import Popen, PIPE
import numpy as np
import matplotlib.pyplot as plt
import random, time, os, signal

def test(alice_num, bob_num):
	alice = Popen('python3 alice.py', stdin=PIPE, text=True, shell=True, stdout=PIPE, stderr=PIPE)
	alice.stdin.write(str(alice_num)+'\n')
	alice.stdin.flush()
	time.sleep(0.5)
	bob = Popen('python3 bob.py', stdin=PIPE, text=True, shell=True, stdout=PIPE, stderr=PIPE)
	bob.stdin.write(str(bob_num)+'\n')
	bob.stdin.flush()
	if 'Traceback' in bob.stderr.readline() or 'Traceback' in alice.stderr.readline():
		alice.stdin.close()
		alice.stdout.close()
		alice.stderr.close()
		bob.stdin.close()
		bob.stdout.close()
		bob.stderr.close()
		alice.kill()
		bob.kill()
		return False
	alice.stdout.readline()
	bob.stdout.readline()
	alice.stdin.close()
	alice.stdout.close()
	alice.stderr.close()
	bob.stdin.close()
	bob.stdout.close()
	bob.stderr.close()
	print('\t',alice_num, bob_num)
	alice.kill()
	bob.kill()
	return True

max_tests = 10
avg_time = []
num_bits = []
for n in range(1,65):
	running_time = []
	i = 0
	with open('number_size', 'w') as f:
		f.write(str(n))
	while i < max_tests:
		with open('port_number', 'w') as f:
			f.write(str(random.randint(50000,60000)))
		start = time.time()
		worked = test(random.randint(2**(n-1),(2**n)-1), random.randint(2**(n-1),(2**n)-1))
		end = time.time()
		if worked:
			running_time.append(end-start)
			print(f"\tThe run-time for the round is{running_time[-1]: .4f}s")
			i += 1
	avg_time.append(np.average(running_time))
	num_bits.append(n)
	print(f"The average run-time for {n:d}-bit number is{avg_time[-1]: .4f}s\n")
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Number\'s Bit Length')
ax.set_ylabel('Time to compute [s]', color = 'red')
ax.plot(num_bits, avg_time, marker='o', linestyle='--', color = 'red')
ax.tick_params(axis ='y', labelcolor = 'red')
ax.set_ylim([0, max(avg_time)*1.1])
plt.title('Ioannidis Algorithm')
plt.savefig('performance.png')