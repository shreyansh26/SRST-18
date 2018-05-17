import os
import pickle
import string
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None # for easy if-statement 

with open('pretrain/dev_lemmatised_words.pkl', 'rb') as f:
	lemmatised_words = pickle.load(f)

with open('pretrain/dev_actual_words.pkl', 'rb') as f:
	actual_words = pickle.load(f)

with open('pretrain/dev_lemma_tags.pkl', 'rb') as f:
	lemma_tags = pickle.load(f)

lemmatised_words = lemmatised_words[:-1]

lemma_words_map = []

#print(actual_words[:10])

for i in range(len(actual_words)):
	lemma_sent = lemmatised_words[i]
	actual_sent = actual_words[i]
	tags = lemma_tags[i]
	lemma_lemma_sent = []
	lemma_actual_sent = []
	for j in range(len(lemma_sent)-1):
		wntag = get_wordnet_pos(tags[j])
		if wntag is None:
			lemma_lemma_sent.append(lemmatizer.lemmatize(lemma_sent[j]))
		else:
			lemma_lemma_sent.append(lemmatizer.lemmatize(lemma_sent[j], pos=wntag))
	for j in range(len(actual_sent)-1):
		lemma_actual_sent.append(lemmatizer.lemmatize(actual_sent[j][0]))
	assert len(lemma_sent) == len(lemma_lemma_sent)+1
	# if 'following' in lemma_sent:
	# 	print(lemma_lemma_sent)
	#print(lemma_lemma_sent)
	for word, tag in actual_sent:
		if word == '\n':
			lemma_words_map.append(((word, word)))
			continue
		if word in string.punctuation:
			continue
		else:
			wntag = get_wordnet_pos(tag)
			if wntag is None:
				lemma = lemmatizer.lemmatize(word) 
			else:
				lemma = lemmatizer.lemmatize(word, pos=wntag)
			if lemma in lemma_sent:
				lemma_words_map.append(((lemma, word)))
			else:
				if lemma in lemma_lemma_sent:
					ind = lemma_lemma_sent.index(lemma)
					lemma_words_map.append(((lemma_sent[ind], word)))
				else:
					pass
				
with open('pretrain/dev_lemma_words_map.pkl', 'wb') as f:
	pickle.dump(lemma_words_map, f)
