f = open("dataset/en-out-complete-test", "r")

f2 = open("jumbled_sent.txt", "w")

sent = []
for l in f:
	if not l.strip():
		f2.write(' '.join(sent))
		f2.write("\n\n")
		sent = []
		continue
	else:
		x, y = l.split(u'\t')
		if y.strip() == 'PUNCT':
			#print(x)
			continue
		else:
			sent.append(x.strip())

f.close()
f2.close()
