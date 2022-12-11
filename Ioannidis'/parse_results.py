import pandas as pd

with open('result.txt','r') as f:
	data = f.read().split('\n')

runtime_data = []
for line in data:
	stuff = line.split()
	if 'run-time' in stuff:
		runtime_data.append(stuff)

all_rounds = []
for i in range(len(runtime_data)//11):
	rounds = [i+1]
	for j in range(11):
		rounds.append(float(runtime_data[(11*i)+j][-1][:-1]))
	all_rounds.append(rounds)
df = pd.DataFrame(all_rounds)
df.to_csv('result.csv', index=False, header=['Number of Bits','Round 1', 'Round 2', 'Round 3', 'Round 4', 'Round 5', 'Round 6', 'Round 7', 'Round 8', 'Round 9', 'Round 10', 'Average'])