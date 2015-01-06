# Kiran Vodrahalli
# Independent Work 2014
# Parsing VSM (Fyshe paper)
# citation: see Fyshe2013
# downloaded from the link in the paper

import h5py as h
import numpy as np 

from util import cosine_dist

from noun_compound_set import word_pos_dict
from noun_compound_set import ncs

from home_path import path 
from home_path import path_ending as pe 

f = h.File(path + 'fyshe_vsm' + pe + 'doc2Dep20MWU57k_1000concat2000.mat', 'r')


count_matrix = f['count_matrix']
words_ = f['words']

# each vector of the vsm can be divided into two halves
# the first half is the domain space, the second half is the relational space (effectively)
# they call it document space and dependency space

# first 1000 are document dimensions
# second 1000 are dependency dimensions
# this makes read-access way faster
vsm = np.matrix(count_matrix.value).T

w_size = np.shape(words_)[1]


#wi is the index of the ith word
def build_entry(wi):
	s = u''
	for c in f[words_[0, wi]]:
		s += unichr(c)
	return s

# maps words to their full 2000-dim vector representation 
#fyshe_dict = {build_entry(i): vsm[i] for i in range(0, w_size)}


#takes in a noun compound,
#returns modifier vector and head vector
# according to Fyshe paper, they tested addition, dilation, and observed 
# (for our noun compounds, we don't have observed -- the observed ones
#  are adj-noun pairs.)
# of the two addition and dilation, addition did better
# they used the first 25 document dimensions and 600 dependency dimensions
# for both addition and dilation 
# we will implement both 


# first 25 document dimensions (columns)
doc_vsm = vsm[:, :25]
# first 600 dependency dimensions (columns)
dep_vsm = vsm[:, 1000:1600]

relevant_vsm = np.c_[doc_vsm, dep_vsm]

# maps words to their (25 + 600)-dim vector representation 
fyshe_trimmed_dict = {build_entry(i): relevant_vsm[i] for i in range(0, w_size)}

# reperesentation of noun compound
# as the sum of the mod and head
def nc_rep_sum(nc):
	mod = word_pos_dict[nc[0]]
	head = word_pos_dict[nc[1]]

	mod_v = fyshe_trimmed_dict[mod]
	head_v = fyshe_trimmed_dict[head]
	return mod_v + head_v
	

# representation of the noun compound as the dilated sum of mod and head
# (we treat mod as though it's an adjective here)
# s_add = gamma * s_adj + s_noun. we can treat the modifier 
# here as an adjective 
# they did not do elementwise multiplication
# gamma is a parameter they used from another paper
# gamma = 16.7 after tuning. 
def nc_rep_dilation(nc):
	gamma = 16.7 # according to Fyshe paper
	mod = word_pos_dict[nc[0]]
	head = word_pos_dict[nc[1]]

	mod_v = fyshe_trimmed_dict[mod]
	head_v = fyshe_trimmed_dict[head]
	return gamma*mod_v + head_v


# dictionary from noun compounds to their sum representations
nc_sums_dict = {nc: nc_rep_sum(nc) for nc in ncs}

# dictionary from noun compounds to their dilated sum representations
nc_dils_dict = {nc: nc_rep_dilation(nc) for nc in ncs}

#--------------------------------------------------
# SIMILARITY FUNCTION

# fyshe paper uses cosine distance as a distance function for vectors
# Fyshe paper: "Perfomance on these benchmarks is Spearman
# correlation between the aggregate human judgements and pairwise
# cosine distances of word vectors in a VSM"

# similarity functions take in two noun compounds 
# (tuples of (mod, head))
# and spits out their similarity score

# in the fyshe vsm, we compose vectors instead of similarity functions, so there
# is only one vector in the first element (we already composed the mod and head vectors)
# in addition, this makes the similarity functions very simple.
# and we have a similarity function per vector representation 

# similarity function for sum representation of noun compounds
def sim_sum(nc1, nc2):
	v1 = nc_sums_dict[nc1]
	v2 = nc_sums_dict[nc2]
	return cosine_dist(v1, v2)

# similarity function for dilation representation of noun compounds
def sim_dilation(nc1, nc2):
	v1 = nc_dils_dict[nc1]
	v2 = nc_dils_dict[nc2]
	return cosine_dist(v1, v2)


# models are just a similarity function!
# takes in two noun compounds represented as (mod, head) tuples. 
# returns a measure of similarity
sum_model = sim_sum
dilation_model = sim_dilation



