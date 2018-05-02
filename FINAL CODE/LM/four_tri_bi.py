import kenlm
import pickle
from itertools import permutations
from math import inf
from copy import copy

model = kenlm.Model("../kenlm-master/lm/test2.lm")


def find_n_gram(jumbled_split,length_perm):
			best_n_gram = None
			list_permutation = list(permutations(jumbled_split, length_perm))
			maximum = -inf
			# print(list_permutation)
			for entry in list_permutation:
				temp_sent = " ".join(list(entry))
				temp_sent_score = model.score(temp_sent)
				if temp_sent_score > maximum:
					maximum = temp_sent_score
					best_n_gram = temp_sent

			return best_n_gram

try:
	with open('real_jum.pickle','rb') as h:
		real_jum = pickle.load(h)

except:

	f = open("jumbled_upper.txt")
	g = open("new_sent.txt")

	real_jum = [[i.strip(),j.strip()] for i,j in zip(g,f)]

	with open('real_jum.pickle','wb') as h:
			pickle.dump(real_jum,h)

	f.close()
	g.close()		
# print(real_jum[1:5])

real_pred = []

for idx,i in enumerate(real_jum):
	print(idx,len(real_jum))

	sentence = real_jum[idx][0]
	jumbled = real_jum[idx][1]
	jumbled_split = jumbled.split()
	sentence_split = sentence.split()

	if not jumbled or len(jumbled_split) > 20:
		continue

	else:
		all_n_grams = []
		if len(jumbled_split) < 4:
			best_sent = None
			list_permutation = list(permutations(jumbled_split, len(i)))
			maximum = -inf
			# print(list_permutation)
			for entry in list_permutation:
				temp_sent = " ".join(list(entry))
				temp_sent_score = model.score(temp_sent)
				if temp_sent_score > maximum:
					maximum = temp_sent_score
					best_sent = temp_sent
			real_jum[idx][1] = best_sent
			real_pred.append(real_jum[idx])
			continue
		
		

		elif len(jumbled_split) <= 10:
			
			best_three_gram = find_n_gram(jumbled_split,3)		

			all_n_grams.append(best_three_gram)

			for j in best_three_gram.split():
				jumbled_split.remove(j)


			if len(jumbled_split) == 0:
				continue
			
			if len(jumbled_split) <= 2 :
				all_n_grams.append(" ".join(jumbled_split))

			else:
				
				best_bi_gram = find_n_gram(jumbled_split,2)

				all_n_grams.append(best_bi_gram)

				for j in best_bi_gram.split():
					jumbled_split.remove(j)

				if len(jumbled_split) == 0:
					continue
				
				if len(jumbled_split) <= 3:
					all_n_grams.append(" ".join(jumbled_split))
				elif len(jumbled_split):
					all_n_grams.append(" ".join(jumbled_split))


		elif len(jumbled_split) <= 15:
			
			best_four_gram = find_n_gram(jumbled_split,4)		

			all_n_grams.append(best_four_gram)

			for j in best_four_gram.split():
				jumbled_split.remove(j)

			if len(jumbled_split) <= 3 :
				all_n_grams.append(" ".join(jumbled_split))

			else:
				
				best_three_gram = find_n_gram(jumbled_split,3)

				all_n_grams.append(best_three_gram)

				for j in best_three_gram.split():
					jumbled_split.remove(j)

				if len(jumbled_split) <= 3 :
					all_n_grams.append(" ".join(jumbled_split))


				best_bi_gram = find_n_gram(jumbled_split,2)

				all_n_grams.append(best_bi_gram)

				for j in best_bi_gram.split():
					jumbled_split.remove(j)

				if len(jumbled_split) <= 2:
					all_n_grams.append(" ".join(jumbled_split))

				else:
					best_bi_gram = find_n_gram(jumbled_split,2)

					all_n_grams.append(best_bi_gram)

					for j in best_bi_gram.split():
						jumbled_split.remove(j)

					if len(jumbled_split) == 0:
						continue

					elif len(jumbled_split) <= 2 :
						all_n_grams.append(" ".join(jumbled_split))

					else:

						best_bi_gram = find_n_gram(jumbled_split,2)

						all_n_grams.append(best_bi_gram)

						for j in best_bi_gram.split():
							jumbled_split.remove(j)

						if len(jumbled_split) == 0:
							continue

						elif len(jumbled_split) <= 2 :
							all_n_grams.append(" ".join(jumbled_split))

						else:
							
							best_bi_gram = find_n_gram(jumbled_split,2)

							all_n_grams.append(best_bi_gram)

							for j in best_bi_gram.split():
								jumbled_split.remove(j)

							if len(jumbled_split) == 0:
								continue

							all_n_grams.append(" ".join(jumbled_split))

		elif len(jumbled_split) <= 20:
			
			best_four_gram = find_n_gram(jumbled_split,4)		

			all_n_grams.append(best_four_gram)

			for j in best_four_gram.split():
				jumbled_split.remove(j)

			if len(jumbled_split) <= 3 :
				all_n_grams.append(" ".join(jumbled_split))

			else:
				
				best_three_gram = find_n_gram(jumbled_split,3)

				all_n_grams.append(best_three_gram)

				for j in best_three_gram.split():
					jumbled_split.remove(j)

				if len(jumbled_split) <= 3 :
					all_n_grams.append(" ".join(jumbled_split))

				best_three_gram = find_n_gram(jumbled_split,3)

				all_n_grams.append(best_three_gram)

				for j in best_three_gram.split():
					jumbled_split.remove(j)

				if len(jumbled_split) <= 3 :
					all_n_grams.append(" ".join(jumbled_split))	

				best_bi_gram = find_n_gram(jumbled_split,2)

				all_n_grams.append(best_bi_gram)

				for j in best_bi_gram.split():
					jumbled_split.remove(j)

				if len(jumbled_split) <= 2:
					all_n_grams.append(" ".join(jumbled_split))

				else:
					best_bi_gram = find_n_gram(jumbled_split,2)

					all_n_grams.append(best_bi_gram)

					for j in best_bi_gram.split():
						jumbled_split.remove(j)

					if len(jumbled_split) == 0:
						continue

					elif len(jumbled_split) <= 2 :
						all_n_grams.append(" ".join(jumbled_split))

					else:

						best_bi_gram = find_n_gram(jumbled_split,2)

						all_n_grams.append(best_bi_gram)

						for j in best_bi_gram.split():
							jumbled_split.remove(j)

						if len(jumbled_split) == 0:
							continue

						elif len(jumbled_split) <= 2 :
							all_n_grams.append(" ".join(jumbled_split))

						else:
							
							best_bi_gram = find_n_gram(jumbled_split,2)

							all_n_grams.append(best_bi_gram)

							for j in best_bi_gram.split():
								jumbled_split.remove(j)

							if len(jumbled_split) == 0:
								continue

							elif len(jumbled_split) <= 2 :
								all_n_grams.append(" ".join(jumbled_split))

							else:
								
								best_bi_gram = find_n_gram(jumbled_split,2)

								all_n_grams.append(best_bi_gram)

								for j in best_bi_gram.split():
									jumbled_split.remove(j)

								if len(jumbled_split) == 0:
									continue

								all_n_grams.append(" ".join(jumbled_split))		


		final_sentence_formed = find_n_gram(all_n_grams,len(all_n_grams))

		real_jum[idx][1] = final_sentence_formed
		real_pred.append(real_jum[idx])



with open('real_pred.pickle','wb') as h:
	pickle.dump(real_pred,h)


