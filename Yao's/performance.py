from subprocess import Popen, PIPE
import numpy as np
import matplotlib.pyplot as plt
import random, time, os, signal

def test():
	alice = Popen('python3 alice.py', stdin=PIPE, text=True, shell=True)
	alice.stdin.write('23\n')
	alice.stdin.flush()
	alice.stdin.write('28\n')
	alice.stdin.flush()
	alice.stdin.write('16\n')
	alice.stdin.flush()
	bob = Popen('python3 bob.py', stdin=PIPE, text=True, shell=True)
	bob.stdin.write('30\n')
	bob.stdin.flush()
	bob.stdin.write('28\n')
	bob.stdin.flush()
	bob.stdin.write('22\n')
	bob.stdin.flush()
	bob.stdin.write('17\n')
	bob.stdin.flush()
	bob.stdin.write('233\n')
	bob.stdin.flush()
	bob.stdin.write('437\n')
	bob.stdin.flush()
	time.sleep(30)
	alice.stdin.close()
	bob.stdin.close()
	alice.kill()
	bob.kill()
	return True

max_tests = 10
avg_time = []
num_bits = []
for n in range(10,11):
	running_time = []
	i = 0
	server = Popen(['python3','server.py'], stdin=PIPE, text=True, shell=False)
	server.stdin.write('21\n')
	server.stdin.flush()
	server.stdin.write('30\n')
	server.stdin.flush()
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