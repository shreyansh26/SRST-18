import pickle

with open('dev_data.pickle', 'rb') as f:
	dev_data = pickle.load(f)

with open('train_data.pickle', 'rb') as f:
	train_data = pickle.load(f)

train_data_print = []
dev_data_print = []

f = open('en-train', 'w')
for i in train_data:
	for a in range(len(i)-1):
		f.write(str(i[a]))
		f.write('\t')
	f.write(i[-1])
	f.write('\n')
f.close()

f = open('en-dev', 'w')
for i in dev_data:
	for a in range(len(i)-1):
		f.write(str(i[a]))
		f.write('\t')
	f.write(i[-1])
	f.write('\n')
f.close()