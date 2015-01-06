# Independent Work 2014
# Kiran Vodrahalli
# Noun Compound frequency information

from copy import deepcopy

from home_path import path 
from home_path import path_ending as pe 

from corpuses import glowbe_folders
import os


# ------------------------ ON COCA -----------------------

coca_ncs = path + "COCA_info" + pe + "coca_n_n.txt" 

# paper cup: head = cup, modifier = paper

# noun compounds organized by head word
# map from head to a set of mods
head_dict = dict()

# noun compounds organized by modifier word
# map from mod to a set of heads
mod_dict = dict()


coca_num_ncs = 0
coca_ncs_count = 0
with open(coca_ncs, 'r') as f:
	for line in f:
		coca_num_ncs += 1
		line = line.strip().split("\t")
		freq = int(line[1])
		coca_ncs_count += freq
		nn_head = line[3]
		nn_mod = line[2]
		if nn_mod not in mod_dict:
			mod_dict[nn_mod] = set()
		mod_dict[nn_mod].add((nn_head, freq))
		if nn_head not in head_dict:
			head_dict[nn_head] = set()
		head_dict[nn_head].add((nn_mod, freq))

coca_num_heads = len(head_dict)
coca_num_mods = len(mod_dict)
# count the starting points: 
# (# noun compounds (not distinct) )/ (words - 1)
# 440 million words
coca_approx_fraction = (coca_ncs_count + 0.0) / (440000000.0 - 1)

def head_freq(head):
	mods = head_dict[head]
	return sum(f for (m, f) in mods)
def mod_freq(mod):
	heads = mod_dict[mod]
	return sum(f for (h, f) in heads)

head_freqs = deepcopy(head_dict)
head_freqs = map(lambda h: (head_freq(h), h), head_freqs)
hfs = sorted(head_freqs, reverse=True)

mod_freqs = deepcopy(mod_dict)
mod_freqs = map(lambda m: (mod_freq(m), m), mod_freqs)
mfs = sorted(mod_freqs, reverse=True)

def topk_heads(k):
	return hfs[0:k]

def topk_mods(k):
	return mfs[0:k]

def num_ncs_topk_heads(k):
	count = 0
	for f_nc in topk_heads(k):
		print f_nc[1] + ": " + str(len(head_dict[f_nc[1]]))
		count += len(head_dict[f_nc[1]])
	return count

def num_ncs_topk_mods(k):
	count = 0
	for f_nc in topk_mods(k):
		print f_nc[1] + ": " + str(len(mod_dict[f_nc[1]]))
		count += len(mod_dict[f_nc[1]])
	return count


def print_COCA_info():
	info_str = ''
	info_str += "#===================================COCA INFO==================================================#\n"
	info_str += "Some statistics on COCA corpus: " + '\n'
	info_str += "Number of distinct noun compounds: " + str(coca_num_ncs) + '\n'
	info_str += "Number of distinct heads: " + str(coca_num_heads) + '\n'
	info_str += "Number of distinct modifiers: " + str(coca_num_mods) + '\n'
	info_str += "Total Number of times a noun compound shows up: " + str(coca_ncs_count) + '\n'
	info_str += "Approximate fraction of places in corpus that begin with a noun compound: " + str(coca_approx_fraction) + '\n'
	info_str += "50 Most Common Head words and their frequencies: " + '\n'
	for freq, head in topk_heads(50):
		info_str += "   " + head + ": " + str(freq) + '\n'
	info_str += "50 Most Common Modifier words and their frequencies: " + '\n'
	for freq, mod in topk_mods(50):
		info_str += "   " + mod  + ": " + str(freq) + '\n'
	info_str += "#==============================================================================================#\n"
	print info_str
	return info_str
# ------------------------ ON GloWbE -----------------------

def glowbe_nc_freq():
	# total frequencies of noun compounds
	nc_freq_dict = dict()
	# frequencies of head words
	g_head_dict = dict()
	# frequencies of mod words
	g_mod_dict = dict()
	# traverse GloWbE
	for folder in glowbe_folders:
		print "-------------------------------------------------------"
		for f_ in os.listdir(folder):
			fstr = folder + pe + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = [] #mod, head
				for line in f:
					line = line.split('\t')
					w, l, p = line[0], line[1], line[2]
					if len(mem) < 2:
						mem.append((l,p))
					else:
						del mem[0]
						mem.append((l,p))
					if len(mem) == 2:
						mod, pos1 = mem[0]
						head, pos2 = mem[1]
						# if both mod and head are nouns
						if pos1[0] == 'n' and pos2[0] == 'n':
							nc = (mod, head)
							if nc not in nc_freq_dict:
								nc_freq_dict[nc] = 0
							nc_freq_dict[nc] += 1
							if mod not in g_mod_dict:
								g_mod_dict[mod] = 0
							g_mod_dict[mod] += 1
							if head not in g_head_dict:
								g_head_dict[head] = 0
							g_head_dict[head] += 1
	# clean up the false noun compounds
	to_del = []
	for tup in nc_freq_dict:
		a = tup[0]
		b = tup[1]
		if a == '':
			to_del.append(tup)
		elif b == '':
			to_del.append(tup)
	for tup in to_del:
		del nc_freq_dict[tup]
	# clean up false head and mod (empy space)
	del g_head_dict['']
	del g_mod_dict['']
	return nc_freq_dict, g_head_dict, g_mod_dict


def load_into_file(glowbe_nc_freq_dict, glowbe_head_dict, glowbe_mod_dict):
	glowbe_nc_freq_str = ''
	for nc in glowbe_nc_freq_dict:
		nc_str = nc[0] + ' ' + nc[1]
		glowbe_nc_freq_str += nc_str + ': ' + str(glowbe_nc_freq_dict[nc]) + '\n'
	with open(path + 'GloWbE_info' + pe + "glowbe_nc_freq.txt", 'w') as f:
		f.write(glowbe_nc_freq_str)	

	glowbe_head_str = ''
	for head in glowbe_head_dict:
		glowbe_head_str += head + ": " + str(glowbe_head_dict[head]) + '\n'
	with open(path + 'GloWbE_info' + pe + 'glowbe_nc_heads.txt', 'w') as f:
		f.write(glowbe_head_str)	

	glowbe_mod_str = ''
	for mod in glowbe_mod_dict:
		glowbe_mod_str += mod + ': ' + str(glowbe_mod_dict[mod]) + '\n'
	with open(path + 'GloWbE_info' + pe + 'glowbe_nc_mods.txt', 'w') as f:
		f.write(glowbe_mod_str)

def build_files():
	glowbe_nc_freq_dict, glowbe_head_dict, glowbe_mod_dict = glowbe_nc_freq()
	load_into_file(glowbe_nc_freq_dict, glowbe_head_dict, glowbe_mod_dict)


glowbe_ncs = path + 'GloWbE_info' + pe + "glowbe_nc_freq.txt"
glowbe_heads = path + 'GloWbE_info' + pe + 'glowbe_nc_heads.txt'
glowbe_mods = path + 'GloWbE_info' + pe + 'glowbe_nc_mods.txt'

gnc_freq = dict()
with open(glowbe_ncs, 'r') as f:
	for line in f:
		nc, str_val = line.split(':')
		count = int(str_val)
		if nc not in gnc_freq:
			gnc_freq[nc] = count

ghead_dict = dict()
with open(glowbe_heads, 'r') as f:
	for line in f:
		head, str_val = line.split(':')
		count = int(str_val)
		if head not in ghead_dict:
			ghead_dict[head] = count

gmod_dict = dict()
with open(glowbe_mods, 'r') as f:
	for line in f:
		mod, str_val = line.split(':')
		count = int(str_val)
		if mod not in gmod_dict:
			gmod_dict[mod] = count


glowbe_num_ncs = len(gnc_freq)
glowbe_ncs_count = 0
for nc in gnc_freq:
	glowbe_ncs_count += gnc_freq[nc]

glowbe_num_heads = len(ghead_dict)
glowbe_num_mods = len(gmod_dict)
glowbe_approx_frac = (glowbe_ncs_count + 0.0)/ (1.9 * 1000000000)

ghead_freqs = deepcopy(ghead_dict)
ghead_freqs = map(lambda h: (ghead_freqs[h], h), ghead_freqs)
ghfs = sorted(ghead_freqs, reverse=True)

gmod_freqs = deepcopy(gmod_dict)
gmod_freqs = map(lambda m: (gmod_freqs[m], m), gmod_freqs)
gmfs = sorted(gmod_freqs, reverse=True)

def g_topk_heads(k):
	return ghfs[:k]

def g_topk_mods(k):
	return gmfs[:k]

def print_GloWbE_info():
	info_str = ''
	info_str += "#===================================GloWbE INFO==================================================#\n"
	info_str += "Some statistics on GloWbE corpus: \n"
	info_str += "Number of distinct noun compounds: " + str(glowbe_num_ncs) + '\n'
	info_str += "Number of distinct heads: " + str(glowbe_num_heads) + '\n'
	info_str += "Number of distinct modifiers: " + str(glowbe_num_mods) + '\n'
	info_str += "Total Number of times a noun compound shows up: " + str(glowbe_ncs_count) + '\n'
	info_str += "Approximate fraction of places in corpus that begin with a noun compound: " + str(glowbe_approx_frac) + '\n'
	info_str += "50 Most Common Head words and their frequencies: " + '\n'
	for freq, head in g_topk_heads(50):
		info_str += "   " + head + ": " + str(freq) + '\n'
	info_str += "50 Most Common Modifier words and their frequencies: " + '\n'
	for freq, mod in g_topk_mods(50):
		info_str += "   " + mod  + ": " + str(freq) + '\n'
	info_str += "#==============================================================================================#\n"
	print info_str
	return info_str



def print_infos_to_files():
	coca_file = path + 'COCA_info' + pe + 'COCA_stats.txt'
	glowbe_file = path + 'GloWbE_info' + pe + 'GloWbE_stats.txt'
	c_info = print_COCA_info()
	g_info = print_GloWbE_info()
	with open(coca_file, 'w') as f:
		f.write(c_info)
	with open(glowbe_file, 'w') as f:
		f.write(g_info)
	print '---------DONE---------'

