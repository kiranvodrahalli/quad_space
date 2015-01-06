# Independent Work 2014
# Kiran Vodrahalli
# building noun compound chosen set
# also build a dictionary for part of speeches for individual nouns (/nn, /nns)


from home_path import path 
from home_path import path_ending as pe 

nc_list = path + "IW_code" + pe + "99_nouncompounds.txt"

def gen_word_list():
	word_set = set()
	with open(nc_list, 'r') as f:
		for line in f:
			line = line.strip().split(" ")
			word_set.add(line[0])
			word_set.add(line[1])
	return word_set

plurals = set(['skills', 'squads', 'women','lilies','rights','sciences','events','students','savings'])

# just be sure to add /NN or /NNS, accordingly
word_pos_dict = dict()

for w in gen_word_list():
	if w in plurals:
		if w not in word_pos_dict:
			word_pos_dict[w] = w + "/NNS"
	else:
		if w not in word_pos_dict:
			word_pos_dict[w] = w + "/NN"

# noun compound representations

# noun compounds will be represented as a tuple of strings
# (modifier, head)

# generate the tuple representations
def gen_nc_list():
	word_set = set()
	with open(nc_list, 'r') as f:
		for line in f:
			line = line.strip().split(' ')
			tup = (line[0], line[1])
			word_set.add(tup)
	return word_set

ncs = gen_nc_list()
'''
nc_iter = [nc for nc in ncs]

nc_pairs = [] 

for i in range(0, len(nc_iter)):
	for j in range(i+1, len(nc_iter)):
		nc_pairs.append((nc_iter[i], nc_iter[j]))

'''
