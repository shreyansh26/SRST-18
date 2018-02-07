import os
import pickle

with open('pretrain/dev_lemma_words_map.pkl', 'rb') as f:
	lemma_words_map = pickle.load(f)

print(len(lemma_words_map))

with open('pretrain/dev_conll_dataset', 'w') as f:
	for lemma_word, word in lemma_words_map[:-1]:
		if lemma_word == '\n':
			f.write('\n')
		else:
			f.write(lemma_word)
			f.write('\t')
			f.write(word)
			f.write('\n')
	f.write(lemma_words_map[-1][0])
	f.write('\t')
	f.write(lemma_words_map[-1][1])
