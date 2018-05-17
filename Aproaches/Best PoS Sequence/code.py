import pickle
from itertools import permutations
from nltk import pos_tag,word_tokenize
import spacy
nlp=spacy.load('en')
with open('dict.pickle','rb') as h:
	a=pickle.load(h)
with open('sent.pickle','rb') as h:
	b=pickle.load(h)

sent_set=[i[0] for i in b]
sent_set = sent_set[:3000]
top_sents_for_each=[]


for idx1,i in enumerate(sent_set):
	print(idx1,len(sent_set))
	# test_sent = pos_tag(word_tokenize(i))
	x=nlp(i)
	if len(x) > 9:
		top_sents_for_each.append('not found')
		continue

	test_sent=[]
	for j in x:
		test_sent.append((j,j.pos_))
	all_perms = list(permutations(test_sent))
	scores=[]
	for idx,j in enumerate(all_perms):
		pred = a['###'][all_perms[idx][0][1]]
		# pred = 1
		for idx1,k in enumerate(j[1:]):
			pred = pred * a[j[idx1-1][1]][k[1]]

		pred *= a[j[-1][1]]['###']

		scores.append((pred,idx))
		
	scores = sorted(scores,key=lambda x:x[0])

	x=[]
	for j in (scores[-10:])[::-1]:
		temp=[]
		for k in all_perms[j[1]]:
				temp.append(str(k[0]))
		x.append(temp)

	top_sents_for_each.append(x)	

with open('extracted_sent.pickle','wb') as h:
	pickle.dump(top_sents_for_each,h)


	
			
