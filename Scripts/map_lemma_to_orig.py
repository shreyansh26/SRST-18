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

with open('lemmatised_words.pkl', 'rb') as f:
	lemmatised_words = pickle.load(f)

with open('actual_words.pkl', 'rb') as f:
	actual_words = pickle.load(f)

lemmatised_words = lemmatised_words[:-1]

lemma_words_map = []

for i in range(len(actual_words)):
	lemma_sent = lemmatised_words[i]
	actual_sent = actual_words[i]
	for word, tag in actual_sent:
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
				continue

with open('lemma_words_map.pkl', 'wb') as f:
	pickle.dump(lemma_words_map, f)