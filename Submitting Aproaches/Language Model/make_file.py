import pickle

combined_list = pickle.load(open("real_pred.pickle","rb"))

# print(combined_list[:10])

real_file = open("real_sent.txt", "w")
pred_file = open("pred_sent.txt", "w")

for i, sent in enumerate(combined_list):
	real_file.write('# sent_id = ' + str(i+1) + '\n')
	pred_file.write('# sent_id = ' + str(i+1) + '\n')
	real_file.write('# text = ' + str(sent[0]) + '\n\n')
	pred_file.write('# text = ' + str(sent[1]) + '\n\n')

real_file.close()
pred_file.close()