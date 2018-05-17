import os
import pickle
import string
import nltk
import re

DATASET_PATH = '../dataset/T1-input/dev/en-ud-dev.conll'
SENTENCES_PATH = '../dataset/Sentences/dev/en-ud-dev_sentences.txt'
translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))

### Process Dataset file ###
with open(DATASET_PATH) as f:
    data_f = list(f)

lemmatised_words = []
words = []
pos_tag = []
tags = []
lemma_tags = []

def has_numbers(input_str):
	return bool(re.search('\d', input_str))

for line in data_f:
	if line != '\n':
		a = line.split('\t')[3]
		b = line.split('\t')[4]
		w = line.split('\t')[1]
		if a=='PUNCT' or a=='NUM':
			continue
		if b=='NNP' or b.startswith('PRP'):
			continue
		if has_numbers(w):
			continue
		words.append(w.lower())
		tags.append(b)
	else:
		words.append('\n')
		tags.append('\n')
		lemmatised_words.append(words)
		lemma_tags.append(tags)
		tags = []
		words = []

print(lemmatised_words[6])
with open('pretrain/dev_lemmatised_words.pkl', 'wb') as f:
	pickle.dump(lemmatised_words, f)
with open('pretrain/dev_lemma_tags.pkl', 'wb') as f:
	pickle.dump(lemma_tags, f)

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
	for c in sent:
		if c in string.punctuation:
			temp.append(((c, c)))
	sent2 = sent.translate(translator)
	sent_split = sent2.split()
	tagged = nltk.pos_tag(sent_split)
	for i in range(len(tagged)):
		tagged[i] = list(tagged[i])
		tagged[i][0] = tagged[i][0].lower()
		tagged[i] = tuple(tagged[i])
	tagged.append((('\n', '\n')))
	temp.extend(tagged)
	actual_words.append(temp)

print(actual_words[6])
with open('pretrain/dev_actual_words.pkl', 'wb') as f:
 	pickle.dump(actual_words, f)
