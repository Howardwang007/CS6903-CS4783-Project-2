from subprocess import Popen, PIPE
import numpy as np
import matplotlib.pyplot as plt
import random, time, os, signal

def test():
	alice = Popen('python3 alice.py', stdin=PIPE, text=True, shell=True)
	alice.stdin.write('700\n')
	alice.stdin.flush()
	alice.stdin.write('523\n')
	alice.stdin.flush()
	alice.stdin.write('846\n')
	alice.stdin.flush()
	bob = Popen('python3 bob.py', stdin=PIPE, text=True, shell=True)
	bob.stdin.write('776\n')
	bob.stdin.flush()
	bob.stdin.write('863\n')
	bob.stdin.flush()
	bob.stdin.write('974\n')
	bob.stdin.flush()
	bob.stdin.write('17\n')
	bob.stdin.flush()
	bob.stdin.write('405233\n')
	bob.stdin.flush()
	bob.stdin.write('531389\n')
	bob.stdin.flush()
	time.sleep(300)
	alice.stdin.close()
	bob.stdin.close()
	alice.kill()
	bob.kill()

max_tests = 10
avg_time = []
num_bits = []
for n in range(10,11):
	running_time = []
	i = 0
	server = Popen(['python3','server.py'], stdin=PIPE, text=True, shell=False)
	server.stdin.write('702\n')
	server.stdin.flush()
	server.stdin.write('514\n')
	server.stdin.flush()
	time.sleep(0.5)
	test()
	server.kill()
	'''while i < max_tests:
		start = time.time()
		worked = test(random.randint(2**(n-1),(2**n)-1), random.randint(2**(n-1),(2**n)-1))
		end = time.time()
		if worked:
			running_time.append(end-start)
			print(f"\tThe run-time for the round is{running_time[-1]: .4f}s")
			i += 1
	avg_time.append(np.average(running_time))
	num_bits.append(n)
	print(f"The average run-time for {n:d}-bit number is{avg_time[-1]: .4f}s\n")'''
'''fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Number\'s Bit Length')
ax.set_ylabel('Time to compute [s]', color = 'red')
ax.plot(num_bits, avg_time, marker='o', linestyle='--', color = 'red')
ax.tick_params(axis ='y', labelcolor = 'red')
ax.set_ylim([0, max(avg_time)*1.1])
plt.title("Yao's Algorithm")
plt.savefig('performance.png')'''