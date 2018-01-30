import os
import pickle
import string
import nltk

DATASET_PATH = '../dataset/T1-input/train/en-ud-train.conll'
SENTENCES_PATH = '../dataset/Sentences/train/en-ud-train_sentences.txt'
translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))

### Process Dataset file ###
with open(DATASET_PATH) as f:
    data_f = list(f)

lemmatised_words = []
words = []
pos_tag = []

for line in data_f:
	if line != '\n':
		words.append(line.split('\t')[1])
	else:
		lemmatised_words.append(words)
		words = []

print(lemmatised_words[0])
with open('lemmatised_words.pkl', 'wb') as f:
	pickle.dump(lemmatised_words, f)

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
	temp.extend(tagged)
	actual_words.append(temp)

print(actual_words[0])
with open('actual_words.pkl', 'wb') as f:
 	pickle.dump(actual_words, f)