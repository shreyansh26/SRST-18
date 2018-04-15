correct = []
jumbled = []

with open('./dataset/actual_sentences_processed.txt', 'r') as f:
	for line in f:
		correct.append(line.strip().split())

with open('./dataset/jumbled_sentences.txt', 'r') as f:
	for line in f:
		jumbled.append(line.strip().split())

#print(correct[3])
#print(jumbled[3])
assert len(jumbled) == len(correct)

count = 0
for i in range(len(correct)):
	try:
		assert len(correct[i]) == len(jumbled[i])
	except AssertionError:
		print(i)
		print(' '.join(correct[i]))
		print(' '.join(jumbled[i]))
		count+=1

print(count)