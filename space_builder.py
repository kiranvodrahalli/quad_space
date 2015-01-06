# Independent Work
# Kiran Vodrahalli
# utility for building dualspace model (mine)
# (create matrices and save them)
# read from COCA/ GLobwe

from corpuses import spec_traverse_corpus_coca
from corpuses import traverse_corpus_coca
from corpuses import spec_traverse_corpus_glowbe
from corpuses import traverse_corpus_glowbe
from corpuses import all_traverse_corpus_coca
from corpuses import all_traverse_corpus_glowbe

import numpy as np
from numpy import shape

from noun_compound_set import ncs
from noun_compound_set import gen_word_list

from util import rank_k
from util import ppmi_transform

from home_path import path 
from home_path import path_ending as pe 

# WRITE FUNCTIONS TO BUILD QUALIFIER-MOD SPACE and QUALIFIER-HEAD SPACE
# these are the adjective spaces; adjective is j

# we look for head word (1-grams)
# and then only to the left, we take the first adjective we find with a small window
def fill_row_dict_head_adj(corpus):
	# columns are adjective frequencies
	words = gen_word_list()
	index_head_adj = 0
	# each word is a row
	row_dict_head_adj = dict()
	for w in words: 
		if w not in row_dict_head_adj:
			row_dict_head_adj[w] = [index_head_adj, dict()]
			index_head_adj += 1

	def find_head_adj(n, center, left_bound, right_bound, memory_array):
		word = memory_array[center][0]
		lemma = memory_array[center][1]

		if lemma in row_dict_head_adj:
			freq = row_dict_head_adj[lemma][1]
		elif word in row_dict_head_adj:
			freq = row_dict_head_adj[word][1]
		else:
			return 
		first_adj = ''
		for i in range(left_bound, center):
			w, l, p = memory_array[center - 1 - i + left_bound] # right to left, we want the closest
			if p[0] == 'j': #j = adjective -- iff starts with j is it adjective
				first_adj = l.lower() # use the lemma and lower-case it

		if first_adj not in freq:
			freq[first_adj] = 0
		freq[first_adj] += 1

	# n = 1 since we are only looking at the head word (we treat the noun in the center as a head word)
	if corpus == 'coca':
		traverse_corpus_coca(3, 1, find_head_adj, True)
	elif corpus == 'glowbe':
		traverse_corpus_glowbe(3, 1, find_head_adj, True)
	else:
		print "invalid corpus"
		return

	return row_dict_head_adj, index_head_adj

# we only look for mod word (1-grams)
# with a medium-large window, we take ALL adjectives in the window
def fill_row_dict_mod_adj(corpus):
	# columns are adjective frequencies
	words = gen_word_list()
	index_mod_adj = 0
	# each word is a row
	row_dict_mod_adj = dict()
	for w in words: 
		if w not in row_dict_mod_adj:
			row_dict_mod_adj[w] = [index_mod_adj, dict()]
			index_mod_adj += 1

	def find_mod_adj(n, center, left_bound, right_bound, memory_array):
		word = memory_array[center][0]
		lemma = memory_array[center][1]

		if lemma in row_dict_mod_adj:
			freq = row_dict_mod_adj[lemma][1]
		elif word in row_dict_mod_adj:
			freq = row_dict_mod_adj[word][1]
		else:
			return 

		# get all adjectives in the window 
		for i in range(left_bound, right_bound):
			if i != center:
				w, l, p = memory_array[i] 
				if p[0] == 'j': #j = adjective -- iff starts with j is it adjective
					curr_adj = l.lower() # use the lemma and lower-case it
					if curr_adj not in freq:
						freq[curr_adj] = 0
					freq[curr_adj] += 1

	# n = 1 since we are only looking at the mod word (we treat the noun in the center as a mod word)
	if corpus == 'coca':
		traverse_corpus_coca(10, 1, find_mod_adj, True)
	elif corpus == 'glowbe':
		traverse_corpus_glowbe(10, 1, find_mod_adj, True)
	else:
		print "invalid corpus"
		return

	return row_dict_mod_adj, index_mod_adj



# WRITE FUNCTION TO BUILD ACTION SPACE 
# action space: rows are noun compounds. 
# make window big -- maybe 14 either way. (this is different from the )
# iff both head and modifier are in the window, add the verbs in the window (why we have such a big window: strict requirement)
# take all verbs before the modifier "eat breakfast at the table" -- breakfast table
# (maybe just take all verbs in the window -- but would like to use distinctions of "head" and "modifier" somehow)
# (yes, we do use "head" and "modifier" in the similarity function -- cause we look at head domain and not modifier really (weight in favor of head))
# these verbs are candidate "paraphrase verbs" as per Nakov and Hearst-- they are acting as potential synonynms for the noun compound
# and represent the "action" of the modifier on the head ( you EAT breakfast at the breakfast table)
# which is why we don't necessarily need the verb context patterns that Turney (2012) uses. 
# Turney instead creates a function space out of the individual words in the word pair in his paper, and combines them in ways
# but Noun Compounds are SIMPLER! there is a built in relationship between the two words already, one is a modifier, and one is a head word
# we don't need to go through the work of building a "function" space for each word. what matters a lot more is the "paraphrasing verb" attributed
# to the NOUN COMPOUND AS A WHOLE, not separate! in fact it is possible that Turney (2012)' approach does not get what we want for noun compounds. 
# we are trying to represent the ACTIONS here, as a paraphrasing verb for each whole noun compound. using that and the domain space vectors
# for the two heads, we get all the similarity functions we need for two noun compounds. 
# THEN WE FIGURE OUT HOW TO COMPOSE THESE SIMILARITY FUNCTIONS. we want to weight the ACTION more than the DOMAIN, and we want to use Geometric mean
# or the like in some way. we can also use (i like this idea) the Action similarity comparison as a FILTER for the domain head similarity
# comparison. If the actions are "similar enough", then we proceed on to the head domain to see if it meets another threshold. 

# also make sure that this similarity function satisfies the mathematical relationships given in turney (/ that they make sense) and be
# sure to justify with words 

# going to try to build both at once (domain and action space in one pass) (enable that for glowbe)
# we also want to be able to build action space only (for coca, since we already have domain space for coca)

# for building action space





######################################## LOOK HERE AND NOTE THIS PLEASE ###############################
# potential problem with action space: what if the only time both words are in the window is as a noun compound, together?
# this is probably not always the case since we ahave a large window, but it is something to note
#######################################################################################################



# corpus = 'coca' or 'glowbe'
def fill_row_dict_verbs(corpus):
	index = 0
	word_to_nouncompound = dict() # takes individual words and gives set of noun compounds they're in
	presence_dict = dict() # keys are noun compounds, value is 0, 1, 2: 
						   # if 0: neither words in nc are in mem, if 1: one word is, if 2: both are and we have green light
	#each noun compound is a row
	row_dict = dict()
	for nc in ncs:
		nc_str = nc[0] + "|" + nc[1]

		if nc[0] not in word_to_nouncompound:
			word_to_nouncompound[nc[0]] = set()
		word_to_nouncompound[nc[0]].add(nc_str)
		if nc[1] not in word_to_nouncompound:
			word_to_nouncompound[nc[1]] = set()
		word_to_nouncompound[nc[1]].add(nc_str)

		if nc_str not in presence_dict:
			presence_dict[nc_str] = 0

		if nc_str not in row_dict:
			row_dict[nc_str] = [index, dict()]
			index += 1
	print '# of rows: ' + str(index)


	# data structure recording which noun compounds are yes and which noun compounds are no
	# at any given moment based on the contents of the memory array
	# updated whenever the memory array is updated, quickly and easily 
	#curr_ncs = set() # set of noun compounds active in memory_array (both words are present in the range)


	# the center is now dependent on whether or not the word is a verb
	# we are looking for "paraphrasing verbs"
	# therefore we need to check if both words of a noun compound are in range
	# if both words are in range (we could have a boolean set for each noun compound)
	# then we add the verb to the frequency dictionary for every noun compound for which both words are in range (the boolean is set to true)
	# we will use regualar traverse, not spec_traverse
	# n should always be 1
	def find_verbs(n, center, left_bound, right_bound, memory_array):
		word = memory_array[center][0]
		lemma = memory_array[center][1]
		pos = memory_array[center][2]

		if pos[0] == 'v':
			valid_keys = set()
			for i in range(left_bound, right_bound):
				if i != center:
					w, l, p = memory_array[i]
					nc_key_set = set()
					if l in word_to_nouncompound:
						nc_key_set = word_to_nouncompound[l]
					elif w in word_to_nouncompound:
						nc_key_set = word_to_nouncompound[w]
					for nc_key in nc_key_set:
						presence_dict[nc_key] += 1
						valid_keys.add(nc_key)
						# both parts of noun compound are in memory_array
						if presence_dict[nc_key] >= 2:
							freq_dict = row_dict[nc_key][1]
							if lemma not in freq_dict:
								freq_dict[lemma] = 0
							freq_dict[lemma] += 1
			# reset (since we're doing it per window)
			for key in valid_keys:
				presence_dict[key] = 0
			valid_keys = set()

	# recall that n = 1 since we are looking at one verb at a time
	if corpus == 'coca':
		traverse_corpus_coca(14, 1, find_verbs, True)
	elif corpus == 'glowbe':
		traverse_corpus_glowbe(14, 1, find_verbs, True)
	else:
		print "invalid corpus"
		return

	return row_dict, index



# for building domain space
#corpus = "coca" or "glowbe"
def fill_row_dict_nouns(corpus):
	words = gen_word_list()
	index = 0
	# each word is a row
	# each noun compound is also a row
	row_dict = dict()
	for w in words: 
		if w not in row_dict:
			row_dict[w] = [index, dict()]
			index += 1
	for nc in ncs:
		nc_str = nc[0] + "|" + nc[1]
		if nc_str not in row_dict:
			row_dict[nc_str] = [index, dict()]
			index += 1
	print '# of rows: ' + str(index)

	# we want the first noun to the left
	# and the first noun to the right
	# and their frequencies
	# n is the size of the n-gram at the center
	# n is 1 or 2
	def find_nouns(n, center, left_bound, right_bound, memory_array):
		word_str = memory_array[center][0]
		lemma_str = memory_array[center][1]
		for i in range(center + 1, center + n):
			word, lemma, pos = memory_array[i]
			word_str += "|" + word
			lemma_str += "|" + lemma
		lemma = lemma_str
		word = word_str

		if lemma in row_dict:
			freq = row_dict[lemma][1]
		elif word in row_dict:
			freq = row_dict[word][1]
		else:
			return 
		left_noun = ''
		right_noun = ''
		for i in range(center + n, right_bound):
			w, l, p = memory_array[i]
			if p[0] == 'n':
				right_noun = l.lower() # use the lemma and lower-case it
		for i in range(left_bound, center):
			w, l, p = memory_array[center - 1 - i + left_bound] # right to left, we want the closest
			if p[0] == 'n':
				left_noun = l.lower() # use the lemma and lower-case it
		#print left_noun
		#print right_noun
		if left_noun not in freq:
			freq[left_noun] = 0
		freq[left_noun] += 1
		if right_noun not in freq:
			freq[right_noun] = 0
		freq[right_noun] += 1

	if corpus == 'coca':
		spec_traverse_corpus_coca(4, find_nouns, True)
	elif corpus == 'glowbe':
		spec_traverse_corpus_glowbe(4, find_nouns, True)
	else:
		print "invalid corpus"
		return

	return row_dict, index 


def fill_all_rows_nouns_verbs(corpus):
	# ------ NOUNS SETUP----------
	words = gen_word_list()
	index_noun = 0
	# each word is a row
	# each noun compound is also a row
	row_dict_nouns = dict()
	for w in words: 
		if w not in row_dict_nouns:
			row_dict_nouns[w] = [index_noun, dict()]
			index_noun += 1
	for nc in ncs:
		nc_str = nc[0] + "|" + nc[1]
		if nc_str not in row_dict_nouns:
			row_dict_nouns[nc_str] = [index_noun, dict()]
			index_noun += 1
	# ------- VERBS SETUP----------
	index_verb = 0
	word_to_nouncompound = dict() # takes individual words and gives set of noun compounds they're in
	presence_dict = dict() # keys are noun compounds, value is 0, 1, 2: 
						   # if 0: neither words in nc are in mem, if 1: one word is, if 2: both are and we have green light
	#each noun compound is a row
	row_dict_verbs = dict()
	for nc in ncs:
		nc_str = nc[0] + "|" + nc[1]

		if nc[0] not in word_to_nouncompound:
			word_to_nouncompound[nc[0]] = set()
		word_to_nouncompound[nc[0]].add(nc_str)
		if nc[1] not in word_to_nouncompound:
			word_to_nouncompound[nc[1]] = set()
		word_to_nouncompound[nc[1]].add(nc_str)

		if nc_str not in presence_dict:
			presence_dict[nc_str] = 0

		if nc_str not in row_dict:
			row_dict_verbs[nc_str] = [index_verb, dict()]
			index_verb += 1
	# -------- FUNCTION -------------
	# which_run: are we looking for verbs or nouns
	# which_run = 'verb' or 'noun'
	def function(which_run, n, center, left_bound, right_bound, memory_array):
		word = memory_array[center][0]
		lemma = memory_array[center][1]
		pos = memory_array[center][2]

		# this part of the if doesn't use n at all
		if which_run == 'verb':
			if pos[0] == 'v':
				valid_keys = set()
				for i in range(left_bound, right_bound):
					if i != center:
						w, l, p = memory_array[i]
						nc_key_set = set()
						if l in word_to_nouncompound:
							nc_key_set = word_to_nouncompound[l]
						elif w in word_to_nouncompound:
							nc_key_set = word_to_nouncompound[w]
						for nc_key in nc_key_set:
							presence_dict[nc_key] += 1
							valid_keys.add(nc_key)
							# both parts of noun compound are in memory_array
							if presence_dict[nc_key] >= 2:
								freq_dict = row_dict_verbs[nc_key][1]
								if lemma not in freq_dict:
									freq_dict[lemma] = 0
								freq_dict[lemma] += 1
				# reset (since we're doing it per window)
				for key in valid_keys:
					presence_dict[key] = 0
				valid_keys = set()
		elif which_run == 'noun': # not a verb -> can be a noun compound
			word_str = word
			lemma_str = lemma
			for i in range(center + 1, center + n):
				word, lemma, pos = memory_array[i]
				word_str += "|" + word
				lemma_str += "|" + lemma
			lemma = lemma_str
			word = word_str

			if lemma in row_dict_nouns:
				freq = row_dict_nouns[lemma][1]
			elif word in row_dict:
				freq = row_dict_nouns[word][1]
			else:
				return 
			left_noun = ''
			right_noun = ''
			for i in range(center + n, right_bound):
				w, l, p = memory_array[i]
				if p[0] == 'n':
					right_noun = l.lower() # use the lemma and lower-case it
			for i in range(left_bound, center):
				w, l, p = memory_array[center - 1 - i + left_bound] # right to left, we want the closest
				if p[0] == 'n':
					left_noun = l.lower() # use the lemma and lower-case it
			#print left_noun
			#print right_noun
			if left_noun not in freq:
				freq[left_noun] = 0
			freq[left_noun] += 1
			if right_noun not in freq:
				freq[right_noun] = 0
			freq[right_noun] += 1
		else:
			print "which_run is in error"
			return

	# r1 = 4 (for nouns)
	# r2 = 14 (for verbs)
	if corpus == 'coca':
		all_traverse_corpus_coca(4, 14, function, True)
	elif corpus == 'glowbe':
		all_traverse_corpus_glowbe(4, 14, function, True)
	else:
		print "invalid corpus"
		return

	return row_dict_nouns, index_noun, row_dict_verbs, index_verb


# --------------------------------------- USE THIS CODE BELOW ------------------------------------------#

# fill the noun, verb, and both adjective spaces
def fill_all_rows(corpus):
	# ------ NOUNS SETUP----------
	words = gen_word_list()
	index_noun = 0
	# each word is a row
	# each noun compound is also a row
	row_dict_nouns = dict()
	# ------ ADJECTIVES SETUP----------
	index_head_adj = 0
	index_mod_adj = 0
	# each word is a row
	row_dict_head_adj = dict()
	row_dict_mod_adj = dict()
	# ------ NOUNS AND ADJECTIVES SETUP----------
	for w in words: 
		if w not in row_dict_nouns:
			row_dict_nouns[w] = [index_noun, dict()]
			index_noun += 1
		if w not in row_dict_head_adj:
			row_dict_head_adj[w] = [index_head_adj, dict()]
			index_head_adj += 1
		if w not in row_dict_mod_adj:
			row_dict_mod_adj[w] = [index_mod_adj, dict()]
			index_mod_adj += 1
	for nc in ncs:
		nc_str = nc[0] + "|" + nc[1]
		if nc_str not in row_dict_nouns:
			row_dict_nouns[nc_str] = [index_noun, dict()]
			index_noun += 1
	# ------- VERBS SETUP----------
	index_verb = 0
	word_to_nouncompound = dict() # takes individual words and gives set of noun compounds they're in
	presence_dict = dict() # keys are noun compounds, value is 0, 1, 2: 
						   # if 0: neither words in nc are in mem, if 1: one word is, if 2: both are and we have green light
	#each noun compound is a row
	row_dict_verbs = dict()
	for nc in ncs:
		nc_str = nc[0] + "|" + nc[1]

		if nc[0] not in word_to_nouncompound:
			word_to_nouncompound[nc[0]] = set()
		word_to_nouncompound[nc[0]].add(nc_str)
		if nc[1] not in word_to_nouncompound:
			word_to_nouncompound[nc[1]] = set()
		word_to_nouncompound[nc[1]].add(nc_str)

		if nc_str not in presence_dict:
			presence_dict[nc_str] = 0

		if nc_str not in row_dict_verbs:
			row_dict_verbs[nc_str] = [index_verb, dict()]
			index_verb += 1
	# -------- FUNCTION -------------
	# which_run: are we looking for verbs or nouns
	# which_run = 'verb' or 'noun'
	def function(which_run, n, center, left_bound, right_bound, memory_array):
		word = memory_array[center][0]
		lemma = memory_array[center][1]
		pos = memory_array[center][2]

		# this part of the if doesn't use n at all
		if which_run == 'verb':
			if pos[0] == 'v':
				valid_keys = set()
				for i in range(left_bound, right_bound):
					if i != center:
						w, l, p = memory_array[i]
						nc_key_set = set()
						if l in word_to_nouncompound:
							nc_key_set = word_to_nouncompound[l]
						elif w in word_to_nouncompound:
							nc_key_set = word_to_nouncompound[w]
						for nc_key in nc_key_set:
							presence_dict[nc_key] += 1
							valid_keys.add(nc_key)
							# both parts of noun compound are in memory_array
							if presence_dict[nc_key] >= 2:
								freq_dict = row_dict_verbs[nc_key][1]
								if lemma not in freq_dict:
									freq_dict[lemma] = 0
								freq_dict[lemma] += 1
				# reset (since we're doing it per window)
				for key in valid_keys:
					presence_dict[key] = 0
				valid_keys = set()
		elif which_run == 'noun': # not a verb -> can be a noun compound
			word_str = word
			lemma_str = lemma
			for i in range(center + 1, center + n):
				word, lemma, pos = memory_array[i]
				word_str += "|" + word
				lemma_str += "|" + lemma
			lemma = lemma_str
			word = word_str

			if lemma in row_dict_nouns:
				freq = row_dict_nouns[lemma][1]
			elif word in row_dict_nouns:
				freq = row_dict_nouns[word][1]
			else:
				return 
			left_noun = ''
			right_noun = ''
			for i in range(center + n, right_bound):
				w, l, p = memory_array[i]
				if p[0] == 'n':
					right_noun = l.lower() # use the lemma and lower-case it
			for i in range(left_bound, center):
				w, l, p = memory_array[center - 1 - i + left_bound] # right to left, we want the closest
				if p[0] == 'n':
					left_noun = l.lower() # use the lemma and lower-case it
			#print left_noun
			#print right_noun
			if left_noun not in freq:
				freq[left_noun] = 0
			freq[left_noun] += 1
			if right_noun not in freq:
				freq[right_noun] = 0
			freq[right_noun] += 1
		elif which_run == 'head_adj':

			if lemma in row_dict_head_adj:
				freq = row_dict_head_adj[lemma][1]
			elif word in row_dict_head_adj:
				freq = row_dict_head_adj[word][1]
			else:
				return 
			first_adj = ''
			for i in range(left_bound, center):
				w, l, p = memory_array[center - 1 - i + left_bound] # right to left, we want the closest
				if p[0] == 'j': #j = adjective -- iff starts with j is it adjective
					first_adj = l.lower() # use the lemma and lower-case it

			if first_adj not in freq:
				freq[first_adj] = 0
			freq[first_adj] += 1
		elif which_run == 'mod_adj':	

			if lemma in row_dict_mod_adj:
				freq = row_dict_mod_adj[lemma][1]
			elif word in row_dict_mod_adj:
				freq = row_dict_mod_adj[word][1]
			else:
				return 	

			# get all adjectives in the window 
			for i in range(left_bound, right_bound):
				if i != center:
					w, l, p = memory_array[i] 
					if p[0] == 'j': #j = adjective -- iff starts with j is it adjective
						curr_adj = l.lower() # use the lemma and lower-case it
						if curr_adj not in freq:
							freq[curr_adj] = 0
						freq[curr_adj] += 1
		else:
			print "which_run is in error"
			return

	# r1 = 4 (for nouns)
	# r2 = 14 (for verbs)
	# r3 = 3 (for head_adj)
	# r4 = 10 (for mod_adj)
	if corpus == 'coca':
		all_traverse_corpus_coca(4, 14, 3, 10, function, True)
	elif corpus == 'glowbe':
		all_traverse_corpus_glowbe(4, 14, 3, 10, function, True)
	else:
		print "invalid corpus"
		return

	return row_dict_nouns, index_noun, row_dict_verbs, index_verb, row_dict_head_adj, index_head_adj, row_dict_mod_adj, index_mod_adj



#corpus = "coca" or "glowbe"
#space_type = "domain" or "action" or "qual_head" or "qual_mod"
def fill_rows(corpus, space_type):
	if space_type == 'domain': 
		return fill_row_dict_nouns(corpus)
	elif space_type == 'action':
		return fill_row_dict_verbs(corpus)
	elif space_type == 'qual_head':
		return fill_row_dict_head_adj(corpus)
	elif space_type == 'qual_mod':
		return fill_row_dict_mod_adj(corpus)
	else:
		print "invalid space_type"
		return 


#corpus = "coca" or "glowbe"
#space_type = "domain" or "action" or "qual_head" or "qual_mod"
def build_freq_mat(corpus, space_type, row_dict, index1):
	index2 = 0
	col_dict = dict()
	for row in row_dict:
		freqs = row_dict[row][1]
		# key is noun or verb
		for key in freqs: 
			if key not in col_dict:
				col_dict[key] = index2
				index2 += 1
	print '# of cols: ' + str(index2)

	space = np.zeros((index1, index2))
	for row in row_dict:
		row_pair = row_dict[row]
		row_num = row_pair[0]
		row_freqs = row_pair[1]
		for col in row_freqs:
			col_num = col_dict[col]
			freq_val = row_freqs[col]
			space[row_num][col_num] = freq_val
	np.save(path + "matrix_files" + pe + corpus + "_" + space_type + pe + corpus + "_" + space_type + "_space.npy", space)
	return space


#corpus = "coca" or "glowbe"
#space_type = "domain" or "action" or "qual_head" or "qual_mod"
def ppmi_space(corpus, space_type):
	space = np.load(path + "matrix_files" + pe + corpus + "_" + space_type + pe + corpus + "_" + space_type + "_space.npy")
	ppmi_mat = ppmi_transform(space)
	np.save(path + "matrix_files" + pe + corpus + '_' + space_type + pe + 'ppmi_' + space_type + '_' + corpus + '.npy', ppmi_mat)
	return ppmi_mat




# the final result we need for the domain space
#corpus = "coca" or "glowbe"
#space_type = 'domain' or 'action' or "qual_head" or "qual_mod"
def gen_space(corpus, space_type):
	ppmi_mat = np.load(path + "matrix_files" + pe + corpus + '_' + space_type + pe + 'ppmi_' + space_type + '_' + corpus + '.npy')
	print "loaded"
	# do SVD here 
	Uk, Dk, Vk = rank_k(ppmi_mat)
	np.save(path + "matrix_files" + pe + corpus + "_" + space_type + pe + "Uk_" + space_type + "_" + corpus + ".npy", Uk)
	np.save(path + "matrix_files" + pe + corpus + "_" + space_type + pe + "Dk_" + space_type + "_" + corpus + ".npy", Dk)
	np.save(path + "matrix_files" + pe + corpus + "_" + space_type + pe + "Vk_" + space_type + "_" + corpus + ".npy", Vk)
	return Uk, Dk, Vk

#corpus = "coca" or "glowbe"
#space_type = "domain" or "action" or "qual_head" or "qual_mod"
def do_everything_space(corpus, space_type):
	c = corpus
	print 'starting first round\n'
	row_dict, index1 = fill_rows(c, space_type)
	print 'starting second round\n'
	space = build_freq_mat(c, space_type, row_dict, index1)
	print 'starting round three\n'
	ppmi_mat = ppmi_space(c, space_type)
	print 'starting round four\n'
	return gen_space(c, space_type)

#corpus = "coca" or "glowbe"
def do_everything_all(corpus):
	c = corpus
	print 'starting first round\n'
	row_dict_nouns, index_noun, row_dict_verbs, index_verb, row_dict_head_adj, index_head_adj, row_dict_mod_adj, index_mod_adj = fill_all_rows(c)
	print 'starting second round\n'
	dspace = build_freq_mat(c, 'domain', row_dict_nouns, index_noun)
	aspace = build_freq_mat(c, 'action', row_dict_verbs, index_verb)
	qhspace = build_freq_mat(c, 'qual_head', row_dict_head_adj, index_head_adj)
	qmspace = build_freq_mat(c, 'qual_mod', row_dict_mod_adj, index_mod_adj)
	print 'starting third round\n'
	ppmi_mat_domain = ppmi_space(c, 'domain')
	ppmi_mat_action = ppmi_space(c, 'action')
	ppmi_mat_qual_head = ppmi_space(c, 'qual_head')
	ppmi_mat_qual_mod = ppmi_space(c, 'qual_mod')
	print 'starting fourth round\n'
	domain = gen_space(c, 'domain')
	action = gen_space(c, 'action')
	qual_head = gen_space(c, 'qual_head')
	qual_mod = gen_space(c, 'qual_mod')
	return domain, action, qual_head, qual_mod

