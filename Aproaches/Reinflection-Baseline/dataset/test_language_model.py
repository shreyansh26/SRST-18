import kenlm
model = kenlm.LanguageModel('lm/test.arpa')
sentence = 'this is a sentence .'
print(model.score(sentence))