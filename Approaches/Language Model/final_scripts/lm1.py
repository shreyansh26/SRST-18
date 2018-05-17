import kenlm
import pickle
from itertools import permutations
from math import inf
from copy import copy

model = kenlm.Model("../kenlm-master/lm/test2.lm")


# print(model.score('hello my name is avi'))

# print(model.score('HELLO MY NAME IS AVI'))

# quit()

with open('real_jum_test.pickle','rb') as h:
		real_jum = pickle.load(h)


real_pred = []
for idx,i in enumerate(real_jum):
		real_jum[idx] = i.upper()


# list_to_run =[104,152,431,825,906,959,968,976,979,1003]

sent_list = []

for idx, i in enumerate(real_jum):
		x=i.split()
		if len(x) >=23:
			sent_list.append([x,idx])



list_correct = []


n_sentences = len(sent_list)

count = 1

print(sent_list)

for idx,i in enumerate(sent_list):
	print(count, "/", n_sentences)
	count += 1
	if not i[0]:
		real_pred.append(['',i[1]])
		continue
	temp_scores = []

	

	list_permutation = list(permutations(i[0], 4))
	top_4_scores = []
	for entry in list_permutation:
		string = entry[0] + " " + entry[1] + " " + entry[2] + " " + entry[3]
		top_4_scores.append([model.score(string), string])
	sentence = max(top_4_scores)[1]

	list_remaining_words = i[0].copy()
	list_temp = sentence.split()
	for temp_word in list_temp:
		list_remaining_words.remove(i[0][i[0].index(temp_word)])


	
	while list_remaining_words:
		scores = []
		for idx, word in enumerate(list_remaining_words):
			scores.append([idx, word, model.score(sentence + " " + word)])
		max_probab = max(scores, key = lambda x: x[2])
		list_remaining_words.remove(list_remaining_words[max_probab[0]])
		sentence = sentence + " " + max_probab[1]
	
	real_pred.append([sentence,i[1]])




with open('greater22.pickle', 'wb') as f:
    pickle.dump(real_pred, f)