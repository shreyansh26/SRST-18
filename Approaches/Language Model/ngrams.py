import kenlm
import pickle
from itertools import permutations
from math import inf
from copy import copy
from nltk import pos_tag,word_tokenize

model = kenlm.Model("../kenlm-master/lm/test2.lm")

with open('dict.pickle','rb') as h:
	tag_to_tag = pickle.load(h)



sent_map ={1:[[1]],
2:[[2]],
3:[[2,1]],
4:[[2,2],[3,1]],
5:[[3,2],[4,1],[2,2,1]],
6:[[3,2,1],[2,2,2],[3,3]],
7:[[3,2,2],[2,2,2,1],[3,3,1]],
8:[[2,2,2,2],[3,3,2],[3,2,2,1]],
9:[[3,3,3],[3,3,2,1],[3,2,2,2],[3,2,2,1,1]],
10:[[3,3,2,2],[3,3,2,1,1],[3,3,3,1],[2,2,2,2,2],[4,3,2,1]],
11:[[4,3,2,1,1],[4,2,2,2,1],[3,3,3,2],[3,2,2,2,2],[3,3,2,2,1]],
12:[[4,2,2,2,2],[4,3,3,2],[4,3,2,1,2],[3,3,3,3],[3,3,2,2,2],[3,3,2,2,1,1]],
13:[[4,3,3,3],[4,3,3,2,1],[4,3,2,2,2],[3,3,3,2,2],[3,3,3,2,1,1]],
14:[[4,4,3,3],[4,4,3,2,1],[4,3,3,2,2],[3,3,3,3,2],[4,3,2,1,2,2],[3,3,2,2,2,2]],
15:[[4,4,3,3,1],[4,3,2,2,2,2],[4,3,3,2,2,1],[3,3,3,3,3],[3,3,2,2,2,2,1],[3,3,3,2,2,2]],
16:[[4,4,3,3,2],[4,3,3,3,2,1],[4,3,3,2,2,2],[4,3,3,3,3],[4,4,4,4],[4,3,2,2,2,2,1]],
17:[[4,4,3,3,2,1],[4,3,3,3,3,1],[4,3,3,2,2,2,1],[4,3,2,2,2,2,2],[4,3,3,3,2,2]],
18:[[4,4,3,3,2,2],[4,3,3,3,3,2],[4,3,3,3,2,2,1],[4,4,4,2,2,2],[4,3,3,2,2,2,2]],
19:[[4,3,3,3,3,3],[3,3,3,3,3,2,1,1],[4,4,3,3,3,2],[3,3,3,3,2,2,2,1],[4,4,3,3,2,2,1]],
20:[[4,4,3,3,3,3],[4,3,3,3,3,2,2],[4,4,4,3,3,2],[4,3,3,3,3,2,1,1],[3,3,3,3,3,3,2],[3,3,3,3,2,2,2,2]]}


def find_n_gram(jumbled_split,length_perm,check =True):
			best_n_gram = None
			list_permutation = list(permutations(jumbled_split, length_perm))
			maximum = -inf
			# print(list_permutation)
			for entry in list_permutation:
				temp_sent = " ".join(list(entry))
				
				# print("entry ",entry)
				pos_score = 1
				


				temp_sent_score = model.score(temp_sent)
				temp_sent_score *= pos_score

				if temp_sent_score > maximum:
					maximum = temp_sent_score
					best_n_gram = temp_sent

			return best_n_gram

def find_best_sent(possible_sentences):
			best_sent = None
			
			maximum = -inf
			# print(list_permutation)
			for entry in possible_sentences:

				
				pos_score = 1
				
				temp_sent_score = model.score(entry)
				temp_sent_score *= pos_score

				if temp_sent_score > maximum:
					maximum = temp_sent_score
					best_sent = entry

			return best_sent			

try:
	with open('real_jum.pickle','rb') as h:
		real_jum = pickle.load(h)


except:

	f = open("jumbled_upper.txt")
	g = open("new_sent.txt")

	real_jum = [[i.strip(),j.strip()] for i,j in zip(g,f)]

	with open('real_jum.pickle','wb') as h:
			pickle.dump(real_jum,h)

	f.close()
	g.close()		
# print(real_jum[1:5])

real_pred = []


for idx,i in enumerate(real_jum):
	print(idx,len(real_jum))

	sentence = real_jum[idx][0]
	jumbled = real_jum[idx][1]
	jumbled_split = jumbled.split()
	sentence_split = sentence.split()
	split_list_len = len(jumbled_split)

	if not jumbled or split_list_len > 20:
		continue

	else:

		possible_ngrams = sent_map[split_list_len] ## list of list

		possible_sentences=[] # stores some of the best possible sentences for the given words
		for j in possible_ngrams:  # j is the ngram list in which the sentence is to be divided eg:[4,3,2,1]
			word_list = jumbled_split.copy()
			all_n_grams=[]
			for k in j:
				best_n_gram = find_n_gram(word_list,k)
				
				for l in best_n_gram.split():
					word_list.remove(l)
				
				all_n_grams.append(best_n_gram)


			best_sentence = find_n_gram(all_n_grams,len(all_n_grams),check = False)
			possible_sentences.append(best_sentence)	


		real_pred.append([sentence,find_best_sent(possible_sentences)])


		

with open('real_pred_n_grams.pickle','wb') as h:
	pickle.dump(real_pred,h)


		