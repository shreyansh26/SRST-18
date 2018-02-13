import os
import pickle
import string
import nltk
import re

SENTENCES_PATH = './dataset/actual_sentences.txt'
punct_list = list(string.punctuation)
punct_list.remove("'")
punct_list = ''.join(punct_list)
translator = str.maketrans(punct_list, ' '*len(punct_list))

### Process Senetences file ###
with open(SENTENCES_PATH) as f:
    sent_f = list(f)

actual_words = []
sentences = []

for line in sent_f:
	if line != '\n':
		if line.split(' ')[1] == 'text':
			sentences.append(line.rstrip()[9:])
	else:
		continue

for sent in sentences:
	temp = []
	punctl = re.findall("[!\"#$%&\()*+,-./:;<=>?@\[^\]_\\`{|}~]+", sent)
	temp.extend(punctl)
	sent2 = sent.translate(translator)
	sent_split = sent2.split()
	temp.extend(sent_split)
	# for c in sent:
	# 	if c in string.punctuation:
	# 		temp.append(c)
	actual_words.append(temp)

#print(actual_words[6])
with open('./dataset/actual_sentences_processed.txt', 'w') as f:
 	for i in actual_words:
 		#print(i)
 		f.write(' '.join(i))
 		f.write('\n')
