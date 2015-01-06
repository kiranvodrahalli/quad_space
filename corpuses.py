# Independent Work
# Kiran Vodrahalli
# COCA reading library
# (also framework for Glowbe too later)

# NOTE! THIS MODULE SHOULD BE AVAILABLE ALONG WITH THE DATASET
# THIS WAY IT IS EASY TO PARSE THE NEW CORPUSES THAT PRINCETON GOT

# citation
# http://corpus.byu.edu/faq.asp#cite
import os 
from home_path import path 
from home_path import path_ending as pe 

# COULD USE THE lexicon.txt# FILES BETTER


COCA_main_folder = path + "COCA" + pe

# could have done this automated, whatever
# this allows easy modification for testing
folder1 = "wlp_academic_rpe"
folder2 = "wlp_fiction_awq"
folder3 = "wlp_magazine_qep"
folder4 = "wlp_newspaper_lsp"
folder5 = "wlp_spoken_kde"

coca_folders = [folder1, folder2, folder3, folder4, folder5]
coca_folders = map(lambda f: COCA_main_folder + f, coca_folders)

GloWbE_main_folder = path + "GloWbE" + pe

glowbe_folders = os.listdir(GloWbE_main_folder)
glowbe_folders.remove(".DS_Store")
glowbe_folders =  map(lambda f: GloWbE_main_folder + f, glowbe_folders)

# really only need max(r1, r2, r3, ..., rk) sized mem_array
# then keep a list of pointers or wtv

# for unigram, bigram, and verb
def all_traverse_corpus(folder_list, r, r_verb, r_headadj, r_modadj, function, skip_punctuation):
	size = 2*r + 1
	size2 = 2*r + 2
	size_v = 2*r_verb + 1
	size_ha = 2*r_headadj + 1
	size_ma = 2*r_modadj + 1
	for folder in folder_list:
		print "-------------------------------------------------------"
		for f_ in os.listdir(folder):
			fstr = folder + pe + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = []
				mem2 = []
				mem_v = []
				mem_ha = []
				mem_ma = []
				count = 0
				count2 = 0
				count_v = 0
				count_ha = 0
				count_ma = 0
				started = False
				ptr = r
				ptr_v = r_verb
				ptr_ha = r_headadj
				ptr_ma = r_modadj
				linenum = 0
				for line in f:
					linenum += 1
					line = line.split("\t")
					w, l, p = line[0], line[1], line[2]
					if skip_punctuation and (p[0] == 'y'):
						continue
					new_section = ((w[0:2] == '##') and (len(w) > 2))
					tup = (w, l, p)
					if new_section and not started:
						started = True
					elif new_section and started:
						# -------------------UNIGRAM NOUN-------------------------#
						iter_lb = 0
						iter_ub = 0
						actual_size = count
						if count < size:
							# haven't applied function on any of them yet
							iter_lb = 0
							iter_ub = count - 1 + 1
							actual_size = count 
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb = ptr 
							iter_ub = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size = 2*r + 1
						for i in range(iter_lb, iter_ub):
							lb = i - r
							if lb < 0:
								lb = 0
							ub = i + 1 + r 
							if ub > actual_size:
								ub = actual_size
							function('noun', 1, i, lb, ub, mem)
						count = 0
						mem = []
						# --------------------BIGRAM NOUN--------------------------#
						iter_lb2 = 0
						iter_ub2 = 0
						actual_size2 = count2
						if count2 < size2:
							# haven't applied function on any of them yet
							iter_lb2 = 0
							iter_ub2 = count2 - 2 + 1
							actual_size2 = count2
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb2 = ptr 
							iter_ub2 = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size2 = 2*r + 2
						for i2 in range(iter_lb2, iter_ub2):
							lb2 = i2 - r
							if lb2 < 0:
								lb2 = 0
							ub2 = i2 + 2 + r 
							if ub2 > actual_size2:
								ub2 = actual_size2
							function('noun', 2, i2, lb2, ub2, mem2)
						count2 = 0
						mem2 = []
						# ----------------VERB--------------------------#
						iter_lb_v = 0
						iter_ub_v = 0
						actual_size_v = count_v
						if count_v < size_v:
							# haven't applied function on any of them yet
							iter_lb_v = 0
							iter_ub_v = count_v - 1 + 1
							actual_size_v = count_v
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb_v = ptr_v
							iter_ub_v = 2*r_verb + 1 # center of n-gram can't go farther than 2*r_verb
							actual_size_v = 2*r_verb + 1
						for i_v in range(iter_lb_v, iter_ub_v):
							lb_v = i_v - r_verb
							if lb_v < 0:
								lb_v = 0
							ub_v = i_v + 1 + r_verb
							if ub_v > actual_size_v:
								ub_v = actual_size_v
							function('verb', 1, i_v, lb_v, ub_v, mem_v)
						count_v = 0
						mem_v = []		
						# ----------------HEAD ADJ--------------------------#
						iter_lb_ha = 0
						iter_ub_ha = 0
						actual_size_ha = count_ha
						if count_ha < size_ha:
							# haven't applied function on any of them yet
							iter_lb_ha = 0
							iter_ub_ha = count_ha - 1 + 1
							actual_size_ha = count_ha
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb_ha = ptr_ha
							iter_ub_ha = 2*r_headadj + 1 # center of n-gram can't go farther than 2*r_headadj
							actual_size_ha = 2*r_headadj + 1
						for i_ha in range(iter_lb_ha, iter_ub_ha):
							lb_ha = i_ha - r_headadj
							if lb_ha < 0:
								lb_ha = 0
							ub_ha = i_ha + 1 + r_headadj
							if ub_ha > actual_size_ha:
								ub_ha = actual_size_ha
							function('head_adj', 1, i_ha, lb_ha, ub_ha, mem_ha)
						count_ha = 0
						mem_ha = []	
						# ----------------MOD ADJ--------------------------#
						iter_lb_ma = 0
						iter_ub_ma = 0
						actual_size_ma = count_ma
						if count_ma < size_ma:
							# haven't applied function on any of them yet
							iter_lb_ma = 0
							iter_ub_ma = count_ma - 1 + 1
							actual_size_ma = count_ma
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb_ma = ptr_ma
							iter_ub_ma = 2*r_modadj + 1 # center of n-gram can't go farther than 2*r_modadj
							actual_size_ma = 2*r_modadj + 1
						for i_ma in range(iter_lb_ma, iter_ub_ma):
							lb_ma = i_ma - r_modadj
							if lb_ma < 0:
								lb_ma = 0
							ub_ma = i_ma + 1 + r_modadj
							if ub_ma > actual_size_ma:
								ub_ma = actual_size_ma
							function('mod_adj', 1, i_ma, lb_ma, ub_ma, mem_ma)
						count_ma = 0
						mem_ma = []					
					else: # not new_section
						# ----------------UNIGRAM NOUN--------------------------#
						if count < size:
							mem.append(tup)
							count += 1
							if count == size:
								# everything before the middle
								for i in range(0, ptr):
									function('noun', 1, i, 0, i + 1 + r, mem)
								count += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('noun', 1, ptr, 0, size, mem)
							del mem[0]
							mem.append(tup)

						# ----------------BIGRAM NOUN--------------------------#
						if count2 < size2:
							mem2.append(tup)
							count2 += 1
							if count2 == size2:
								# everything before the middle
								for i2 in range(0, ptr):
									function('noun', 2, i2, 0, i2 + 2 + r, mem2)
								count2 += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('noun', 2, ptr, 0, size2, mem2)
							del mem2[0]
							mem2.append(tup)
						# -----------------VERB --------------------#
						if count_v < size_v:
							mem_v.append(tup)
							count_v += 1
							if count_v == size_v:
								# everything before the middle
								for i_v in range(0, ptr_v):
									function('verb', 1, i_v, 0, i_v + 1 + r_verb, mem_v)
								count_v += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('verb', 1, ptr_v, 0, size_v, mem_v)
							del mem_v[0]
							mem_v.append(tup)
						# -----------------HEAD ADJ --------------------#
						if count_ha < size_ha:
							mem_ha.append(tup)
							count_ha += 1
							if count_ha == size_ha:
								# everything before the middle
								for i_ha in range(0, ptr_ha):
									function('head_adj', 1, i_ha, 0, i_ha + 1 + r_headadj, mem_ha)
								count_ha += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('head_adj', 1, ptr_ha, 0, size_ha, mem_ha)
							del mem_ha[0]
							mem_ha.append(tup)
						# -----------------MOD ADJ --------------------#
						if count_ma < size_ma:
							mem_ma.append(tup)
							count_ma += 1
							if count_ma == size_ma:
								# everything before the middle
								for i_ma in range(0, ptr_ma):
									function('mod_adj', 1, i_ma, 0, i_ma + 1 + r_modadj, mem_ma)
								count_ma += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('mod_adj', 1, ptr_ma, 0, size_ma, mem_ma)
							del mem_ma[0]
							mem_ma.append(tup)

				# now we've reached the end, and memory is still full (unless ended, and then only a few after)
				# -------------------UNIGRAM NOUN--------------------------------#
				mem_actual_size = len(mem)
				if mem_actual_size > 2*r + 1:
					mem_actual_size = 2*r + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r
				for i in range(ptr + 1, mem_actual_size):
					function('noun', 1, i, i - r, size, mem)
				# -------------------BIGRAM NOUN--------------------------------#
				mem_actual_size2 = len(mem2)
				if mem_actual_size2 > 2*r + 1:
					mem_actual_size2 = 2*r + 1
				# center of n-gram can't go farther than 2*r
				for i2 in range(ptr + 1, mem_actual_size2):
					function('noun', 2, i2, i2 - r, size2, mem2)
				# -------------------VERB ----------------------------#
				mem_actual_size_v = len(mem_v)
				if mem_actual_size_v > 2*r_verb + 1:
					mem_actual_size_v = 2*r_verb + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r_verb
				for i_v in range(ptr_v + 1, mem_actual_size_v):
					function('verb', 1, i_v, i_v - r_verb, size_v, mem_v)
				# -------------------HEAD ADJ ----------------------------#
				mem_actual_size_ha = len(mem_ha)
				if mem_actual_size_ha > 2*r_headadj + 1:
					mem_actual_size_ha = 2*r_headadj + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r_headadj
				for i_ha in range(ptr_ha + 1, mem_actual_size_ha):
					function('head_adj', 1, i_ha, i_ha - r_headadj, size_ha, mem_ha)
				# -------------------MOD ADJ ----------------------------#
				mem_actual_size_ma = len(mem_ma)
				if mem_actual_size_ma > 2*r_modadj + 1:
					mem_actual_size_ma = 2*r_modadj + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r_headadj
				for i_ma in range(ptr_ma + 1, mem_actual_size_ma):
					function('mod_adj', 1, i_ma, i_ma - r_modadj, size_ma, mem_ma)
	return

def all_traverse_corpus_coca(r, r_verb, r_headadj, r_modadj, function, skip_punctuation):
	return all_traverse_corpus(coca_folders, r, r_verb, r_headadj, r_modadj, function, skip_punctuation)

def all_traverse_corpus_glowbe(r, r_verb, r_headadj, r_modadj, function, skip_punctuation):
	return all_traverse_corpus(glowbe_folders, r, r_verb, r_headadj, r_modadj, function, skip_punctuation)


# for unigram, bigram, and verb
def nounverb_traverse_corpus(folder_list, r, r_verb, function, skip_punctuation):
	size = 2*r + 1
	size2 = 2*r + 2
	size_v = 2*r_verb + 1
	for folder in folder_list:
		print "-------------------------------------------------------"
		for f_ in os.listdir(folder):
			fstr = folder + pe + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = []
				mem2 = []
				mem_v = []
				count = 0
				count2 = 0
				count_v = 0
				started = False
				ptr = r
				ptr_v = r_verb
				linenum = 0
				for line in f:
					linenum += 1
					line = line.split("\t")
					w, l, p = line[0], line[1], line[2]
					if skip_punctuation and (p[0] == 'y'):
						continue
					new_section = ((w[0:2] == '##') and (len(w) > 2))
					tup = (w, l, p)
					if new_section and not started:
						started = True
					elif new_section and started:
						# --------------------------------------------#
						iter_lb = 0
						iter_ub = 0
						actual_size = count
						if count < size:
							# haven't applied function on any of them yet
							iter_lb = 0
							iter_ub = count - 1 + 1
							actual_size = count 
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb = ptr 
							iter_ub = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size = 2*r + 1
						for i in range(iter_lb, iter_ub):
							lb = i - r
							if lb < 0:
								lb = 0
							ub = i + 1 + r 
							if ub > actual_size:
								ub = actual_size
							function('noun', 1, i, lb, ub, mem)
						count = 0
						mem = []
						# ----------------------------------------------#
						iter_lb2 = 0
						iter_ub2 = 0
						actual_size2 = count2
						if count2 < size2:
							# haven't applied function on any of them yet
							iter_lb2 = 0
							iter_ub2 = count2 - 2 + 1
							actual_size2 = count2
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb2 = ptr 
							iter_ub2 = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size2 = 2*r + 2
						for i2 in range(iter_lb2, iter_ub2):
							lb2 = i2 - r
							if lb2 < 0:
								lb2 = 0
							ub2 = i2 + 2 + r 
							if ub2 > actual_size2:
								ub2 = actual_size2
							function('noun', 2, i2, lb2, ub2, mem2)
						count2 = 0
						mem2 = []
						# ----------------VERB--------------------------#
						iter_lb_v = 0
						iter_ub_v = 0
						actual_size_v = count_v
						if count_v < size_v:
							# haven't applied function on any of them yet
							iter_lb_v = 0
							iter_ub_v = count_v - 1 + 1
							actual_size_v = count_v
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb_v = ptr_v
							iter_ub_v = 2*r_verb + 1 # center of n-gram can't go farther than 2*r
							actual_size_v = 2*r_verb + 1
						for i_v in range(iter_lb_v, iter_ub_v):
							lb_v = i_v - r_verb
							if lb_v < 0:
								lb_v = 0
							ub_v = i_v + 1 + r_verb
							if ub_v > actual_size_v:
								ub_v = actual_size_v
							function('verb', 1, i_v, lb_v, ub_v, mem_v)
						count_v = 0
						mem_v = []						
					else: # not new_section
						# ------------------------------------------#
						if count < size:
							mem.append(tup)
							count += 1
							if count == size:
								# everything before the middle
								for i in range(0, ptr):
									function('noun', 1, i, 0, i + 1 + r, mem)
								count += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('noun', 1, ptr, 0, size, mem)
							del mem[0]
							mem.append(tup)

						# ------------------------------------------#
						if count2 < size2:
							mem2.append(tup)
							count2 += 1
							if count2 == size2:
								# everything before the middle
								for i2 in range(0, ptr):
									function('noun', 2, i2, 0, i2 + 2 + r, mem2)
								count2 += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('noun', 2, ptr, 0, size2, mem2)
							del mem2[0]
							mem2.append(tup)
						# -----------------VERB --------------------#
						if count_v < size_v:
							mem_v.append(tup)
							count_v += 1
							if count_v == size_v:
								# everything before the middle
								for i_v in range(0, ptr_v):
									function('verb', 1, i_v, 0, i_v + 1 + r_verb, mem_v)
								count_v += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function('verb', 1, ptr_v, 0, size_v, mem_v)
							del mem_v[0]
							mem_v.append(tup)

				# now we've reached the end, and memory is still full (unless ended, and then only a few after)
				# ---------------------------------------------------#
				mem_actual_size = len(mem)
				if mem_actual_size > 2*r + 1:
					mem_actual_size = 2*r + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r
				for i in range(ptr + 1, mem_actual_size):
					function('noun', 1, i, i - r, size, mem)
				# ----------------------------------------------------#
				mem_actual_size2 = len(mem2)
				if mem_actual_size2 > 2*r + 1:
					mem_actual_size2 = 2*r + 1
				# center of n-gram can't go farther than 2*r
				for i2 in range(ptr + 1, mem_actual_size2):
					function('noun', 2, i2, i2 - r, size2, mem2)
				# -------------------VERB ----------------------------#
				mem_actual_size_v = len(mem_v)
				if mem_actual_size_v > 2*r_verb + 1:
					mem_actual_size_v = 2*r_verb + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r_verb
				for i_v in range(ptr_v + 1, mem_actual_size_v):
					function('verb', 1, i_v, i_v - r_verb, size_v, mem_v)
	return

def nounverb_traverse_corpus_coca(r, r_verb, function, skip_punctuation):
	return all_traverse_corpus(coca_folders, r, r_verb, function, skip_punctuation)

def nounverb_traverse_corpus_glowbe(r, r_verb, function, skip_punctuation):
	return all_traverse_corpus(glowbe_folders, r, r_verb, function, skip_punctuation)



# specifically for unigram and bigram only
def spec_traverse_corpus(folder_list, r, function, skip_punctuation):
	size = 2*r + 1
	size2 = 2*r + 2
	for folder in folder_list:
		print "-------------------------------------------------------"
		for f_ in os.listdir(folder):
			fstr = folder + pe + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = []
				mem2 = []
				count = 0
				count2 = 0
				started = False
				ptr = r
				linenum = 0
				for line in f:
					linenum += 1
					line = line.split("\t")
					w, l, p = line[0], line[1], line[2]
					if skip_punctuation and (p[0] == 'y'):
						continue
					new_section = ((w[0:2] == '##') and (len(w) > 2))
					tup = (w, l, p)
					if new_section and not started:
						started = True
					elif new_section and started:
						iter_lb = 0
						iter_ub = 0
						if count < size:
							# haven't applied function on any of them yet
							iter_lb = 0
							iter_ub = count - 1 + 1
							actual_size = count 
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb = ptr 
							iter_ub = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size = 2*r + 1
						for i in range(iter_lb, iter_ub):
							lb = i - r
							if lb < 0:
								lb = 0
							ub = i + 1 + r 
							if ub > actual_size:
								ub = actual_size
							function(1, i, lb, ub, mem)
						count = 0
						mem = []
						# ----------------------------------------------#
						iter_lb2 = 0
						iter_ub2 = 0
						if count2 < size2:
							# haven't applied function on any of them yet
							iter_lb2 = 0
							iter_ub2 = count2 - 2 + 1
							actual_size2 = count2
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb2 = ptr 
							iter_ub2 = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size2 = 2*r + 2
						for i2 in range(iter_lb2, iter_ub2):
							lb2 = i2 - r
							if lb2 < 0:
								lb2 = 0
							ub2 = i2 + 2 + r 
							if ub2 > actual_size2:
								ub2 = actual_size2
							function(2, i2, lb2, ub2, mem2)
						count2 = 0
						mem2 = []
					else: # not new_section
						if count < size:
							mem.append(tup)
							count += 1
							if count == size:
								# everything before the middle
								for i in range(0, ptr):
									function(1, i, 0, i + 1 + r, mem)
								count += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function(1, ptr, 0, size, mem)
							del mem[0]
							mem.append(tup)

						# ------------------------------------------#
						if count2 < size2:
							mem2.append(tup)
							count2 += 1
							if count2 == size2:
								# everything before the middle
								for i2 in range(0, ptr):
									function(2, i2, 0, i2 + 2 + r, mem2)
								count2 += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function(2, ptr, 0, size2, mem2)
							del mem2[0]
							mem2.append(tup)
				# now we've reached the end, and memory is still full (unless ended, and then only a few after)
				mem_actual_size = len(mem)
				if mem_actual_size > 2*r + 1:
					mem_actual_size = 2*r + 1
				# take care of the last few
				# center of n-gram can't go farther than 2*r
				for i in range(ptr + 1, mem_actual_size):
					function(1, i, i - r, size, mem)
				# ----------------------------------------------------#
				mem_actual_size2 = len(mem2)
				if mem_actual_size2 > 2*r + 1:
					mem_actual_size2 = 2*r + 1
				# center of n-gram can't go farther than 2*r
				for i2 in range(ptr + 1, mem_actual_size2):
					function(2, i2, i2 - r, size2, mem2)
	return

def spec_traverse_corpus_coca(r, function, skip_punctuation):
	return spec_traverse_corpus(coca_folders, r, function, skip_punctuation)

def spec_traverse_corpus_glowbe(r, function, skip_punctuation):
	return spec_traverse_corpus(glowbe_folders, r, function, skip_punctuation)







# general traversal 
# (only does one type of n-gram at a time)
# function f takes in:
# n, center, left bound, right bound, memory_array
# f(center, left_bound, right_bound)
# (center, left_bound, right_bound)
# represents a valid range in the corpus
# memory_array is the implementation of our current memory
# n is n-tuple: if n = 1, treat single word as center
# if n = 2, treat bigram as center. (and so on)
# skip_punctuation is a boolean that decides whether or not 
# to skip punctuation (pos = 'y')
def traverse_corpus(folder_list, r, n, function, skip_punctuation):
	size = 2*r + n
	for folder in folder_list:
		print "-------------------------------------------------------"
		for f_ in os.listdir(folder):
			fstr = folder + pe + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = []
				count = 0
				started = False
				ptr = r
				linenum = 0
				for line in f:
					linenum += 1
					line = line.split("\t")
					w, l, p = line[0], line[1], line[2]
					if skip_punctuation and (p[0] == 'y'):
						continue
					new_section = ((w[0:2] == '##') and (len(w) > 2))
					tup = (w, l, p)
					if new_section and not started:
						started = True
					elif new_section and started:
						iter_lb = 0
						iter_ub = 0
						if count < size:
							# haven't applied function on any of them yet
							iter_lb = 0
							iter_ub = count - n + 1
							actual_size = count 
						else:
							# have already applied function for everything up to ptr
							# still need to apply to ptr (need to go else (not new section) -> else (apply f on ptr))
							# (and we haven't done that if we went to elif new_section and started)
							iter_lb = ptr 
							iter_ub = 2*r + 1 # center of n-gram can't go farther than 2*r
							actual_size = 2*r + n
						for i in range(iter_lb, iter_ub):
							lb = i - r
							if lb < 0:
								lb = 0
							ub = i + n + r 
							if ub > actual_size:
								ub = actual_size
							function(n, i, lb, ub, mem)
						count = 0
						mem = []
					else: # not new_section
						if count < size:
							mem.append(tup)
							count += 1
							if count == size:
								# everything before the middle
								for i in range(0, ptr):
									function(n, i, 0, i + n + r, mem)
								count += 1 # don't want to repeat this
						else:
							# always apply f on the middle
							function(n, ptr, 0, size, mem)
							del mem[0]
							mem.append(tup)
				# now we've reached the end, and memory is still full
				# take care of the last few
				mem_actual_size = len(mem)
				if mem_actual_size > 2*r + 1:
					mem_actual_size = 2*r + 1

				# center of n-gram can't go farther than 2*r
				for i in range(ptr + 1, mem_actual_size):
					function(n, i, i - r, size, mem)
	return

def traverse_corpus_coca(r, n, function, skip_punctuation):
	return traverse_corpus(coca_folders, r, n, function, skip_punctuation)

def traverse_corpus_glowbe(r, n, function, skip_punctuation):
	return traverse_corpus(glowbe_folders, r, n, function, skip_punctuation)


# first can get a method just to count all relevant frequencies in the document
# of lemmas and of specific words
# don't specifically need to do this, since we will be using our 100 noun compounds
# and the however many words make them up. 
# so we need to find context windows for individual words and for the full noun compounds

# we should construct our own word context matrix as well from COCA
# recall that Fyshe did their own thing, and we could use that as a domain space also. 
# but we still should just construct our own. 

# DOMAIN SPACE
# for each word in the word list (not full noun compound), we can build a domain space vector
# from our own COCA stuff. 
# to do this, we need, for each word in the word list, to: 
# 1) find the words in given radius r for each appearance of the word, and do counts
# 2) ignore silly words like the/an/a etc.  (we don't have to actually)


#structure 


# this file contains helper methods to build relational VSM
# since we are building for noun compounds, each row of our matrix
# is a noun compound relation vector

# this means we take in two nouns for every method in search. 

# things we want to search:

# words nearby (particularly, verbs) within radius of any one of the words
# words nearby (particularly, verbs) in spaces surrounding nearest instances of both words
# more? context, or something? 
# some kind of wsd may be necessary... 
# we want to keep lemmas

# after we are able to retreive these sets of strings from the corpus files, we then want to do
# more with them/ analyze them more to come up with the columns and the frequencies. 

# we only want vectors for the 100 specified noun compounds that we are testing
# though of course we use the whole corpus to build the word vectors for them. 

# word here should be a lemma
# we definitely want the lemmatized form of the word
# so that we caputre plural occurences and so on
# r is # of words to left and right. so if r = 3, then there are 2r + 1 = 7 words.
# note that we count lemmas

'''
def radius_of(word, r):
	freq = dict()
	total_counts = 0
	for folder in folders:
		for f_ in os.listdir(folder):
			fstr = folder + "/" + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = []
				count = 0
				started = False
				ptr = r
				# for every lemma in the range of the word (in memory), update frequency count for each lemma
				def freq_fill(index, lower_bound, upper_bound):
					fcount = 0
					# word or lemma
					if mem[index][0] == word or mem[index][1] == word:
						for j in range(lower_bound, upper_bound):
							if j != index:
								lemma = mem[j][1]
								if lemma not in freq:
									freq[lemma] = 0
								freq[lemma] += 1
								fcount += 1
					return fcount
				for line in f:
					line = line.split("\t")
					w, l, p = line[0], line[1], line[2]
					new_section = (w[0:2] == '##')
					tup = (w, l, p)
					if new_section and not started:
						started = True
					elif new_section and started:
						iter_lb = 0
						iter_ub = 0
						if count < 2*r + 1:
							# haven't done the counts for any of them yet
							iter_lb = 0
							iter_ub = count
						else:
							# have already done counts for everything up to and including ptr
							iter_lb = ptr + 1
							iter_ub = 2*r + 1
						for i in range(iter_lb, iter_ub):
							lb = i - r
							if lb < iter_lb:
								lb = iter_lb
							ub = i + r + 1
							if ub > iter_ub:
								ub = iter_ub
							total_counts += freq_fill(i, lb, ub)
						count = 0
						mem = []
					else: # not new_section
						if count < 2*r + 1:
							mem.append(tup)
							count += 1
						else:
							if count == 2*r + 1:
								# everything before the middle
								for i in range(0, ptr):
									total_counts += freq_fill(i, 0, i + r + 1)
								count += 1 # don't want to repeat this
							# always fill from the middle
							total_counts += freq_fill(ptr, 0, 2*r + 1)
							del mem[0]
							mem.append(tup)
				# now we've reached the end, and memory is still full
				# if len(mem) > 0, then we didn't end on a new section
				# and len(mem) = 7 (if r = 3), for instance
				# take care of the last few
				if len(mem) > 0:
					for i in range(ptr + 1, 2*r + 1):
						total_counts += freq_fill(i, i - r, 2*r + 1)

	return freq, total_counts

# note: mistake from before should ensure counts are 1/4 the size of before (roughly)
# could have extra counted once, twice, or three times depending on location of word
# in the memory array (1 2 3 Word 4 5 6) -> 2 extra-counted once, 3 extra-counted twice, 4, 5, 6 extra-counted thrice 
# if whatever word is at 4 always appears to the right of Word, then should be 1/4 count of mistake-program

# can now adapt to take into account parts of speech
# y: punctuation, etc -- can remove, or not remove
# verbs of all kinds: can store part of speech info in frequency table
# or could just add a filtering option so that we only take add verbs or wtv to the frequency table
# or rather we have a more general filtering option: 
# we can say, "allow verbs, disallow punctuation, etc"
# and only take those in. 

# also we don't have to just do frequency counts of words appearing in each window
# we can get the windows as we want and use them to generate contextual patterns
# (if we do simple contextual pattern, i.e. noun right next to word, this is easy: r = 1 frequency dictionary solves it)
# for more complicated ones, we need the part of speech info -- our memory block is a fixed-length list of triples (w, l, p)


# also need to be able to automate this calculation for a bunch of words, not just one word at a time
def lradius_of(word_list, r):
	freq_wdict = dict()
	for w in word_list:
		if w not in freq_wdict:
			freq_wdict[w] = [dict(), 0]
	for folder in folders:
		for f_ in os.listdir(folder):
			fstr = folder + "/" + f_
			print "In folder: " + fstr
			with open(fstr, 'r') as f:
				mem = []
				count = 0
				started = False
				ptr = r
				# for every lemma in the range of the word (in memory), update frequency count for each lemma
				def freq_fill(index, lower_bound, upper_bound):
					# word or lemma
					word_key = ''
					if mem[index][1] in word_list:
						word_key = mem[index][1]
					elif mem[index][0] in word_list:
						word_key = mem[index][0]
					else:
						return
					freq_count = freq_wdict[word_key]
					freq = freq_count[0]
					for j in range(lower_bound, upper_bound):
						if j != index:
							lemma = mem[j][1]
							if lemma not in freq:
								freq[lemma] = 0
							freq[lemma] += 1
							freq_count[1] += 1
					
				for line in f:
					line = line.split("\t")
					w, l, p = line[0], line[1], line[2]
					new_section = (w[0:2] == '##')
					tup = (w, l, p)
					if new_section and not started:
						started = True
					elif new_section and started:
						iter_lb = 0
						iter_ub = 0
						if count < 2*r + 1:
							# haven't done the counts for any of them yet
							iter_lb = 0
							iter_ub = count
						else:
							# have already done counts for everything up to and including ptr
							iter_lb = ptr + 1
							iter_ub = 2*r + 1
						for i in range(iter_lb, iter_ub):
							lb = i - r
							if lb < iter_lb:
								lb = iter_lb
							ub = i + r + 1
							if ub > iter_ub:
								ub = iter_ub
							freq_fill(i, lb, ub)
						count = 0
						mem = []
					else: # not new_section
						if count < 2*r + 1:
							mem.append(tup)
							count += 1
						else:
							if count == 2*r + 1:
								# everything before the middle
								for i in range(0, ptr):
									freq_fill(i, 0, i + r + 1)
								count += 1 # don't want to repeat this
							# always fill from the middle
							freq_fill(ptr, 0, 2*r + 1)
							del mem[0]
							mem.append(tup)
				# now we've reached the end, and memory is still full
				# take care of the last few
				if len(mem) > 0:
					for i in range(ptr + 1, 2*r + 1):
						freq_fill(i, i - r, 2*r + 1)
	for w in freq_wdict:
		curr_dict, curr_count = freq_wdict[w]
		for key in curr_dict:
			curr_dict[key] = curr_dict[key] / (curr_count + 0.0)
	# don't need counts anymore
	for w in freq_wdict:
		d, cc = freq_wdict[w]
		freq_wdict[w] = d
	return freq_wdict

# maybe for each word (row), have a bunch of dicts (one for nouns, one for verbs, etc...)



#word_frequencies = lradius_of(gen_word_list(), 4)

# wf is generated from lradius
def gen_columns(wf):
	cols = dict()
	for word in wf:
		freq_dict, c = wf[word]
		for col_word in freq_dict:
			if col_word not in cols:
				cols[col_word] = 0
			cols[col_word] += freq_dict[col_word]
	col_list = []
	for col in cols:
		col_list.append((cols[col], col))
	return sorted(col_list, reverse=True)

#potential_cols = gen_columns(word_frequencies)

def topk_cols(col_list, k):
	return col_list[0:k]


# we also need to do the thing turney paper does: as contexts, get the first noun to the left
# and the first noun to the right.. (way to build domain space as described in the paper)

				# for every lemma in the range of the word (in memory), update frequency count for each lemma
				def freq_fill(index, lower_bound, upper_bound):
					# word or lemma
					word_key = ''
					if mem[index][1] in word_list:
						word_key = mem[index][1]
					elif mem[index][0] in word_list:
						word_key = mem[index][0]
					else:
						return
					freq_count = freq_wdict[word_key]
					freq = freq_count[0]
					for j in range(lower_bound, upper_bound):
						if j != index:
							lemma = mem[j][1]
							if lemma not in freq:
								freq[lemma] = 0
							freq[lemma] += 1
							freq_count[1] += 1
'''












