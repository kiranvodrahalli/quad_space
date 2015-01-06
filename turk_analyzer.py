# Independent Work
# Kiran Vodrahalli
# better turker parser
# use for actually testing VSM models

from home_path import path 
from home_path import path_ending as pe 

# finally everything has 3 different ratings with these files
f1 = path + "mech_turk_results" + pe + "mech_turk_data1_round1.csv"
f2 = path + "mech_turk_results" + pe + "mech_turk_data1_round2.csv"
f3 = path + "mech_turk_results" + pe + "mech_turk_data1_round3.csv"
f4 = path + "mech_turk_results" + pe + "mech_turk_data1_repeat1.csv"
f5 = path + "mech_turk_results" + pe + "mech_turk_data1_repeat2.csv"
f6 = path + "mech_turk_results" + pe + "mech_turk_data1_repeat3.csv"
f7 = path + "mech_turk_results" + pe + "kiran_counts.csv"
f8 = path + "mech_turk_results" + pe + "mech_turk_data1_repeat4.csv"

#STRATEGY
# first we go through all files, and base our dictionary on turkers. 
# then we remove the bad turkers, and are only left with good ones. 
# for each noun compound, we find the three good trials that there are
# and build a new dict with noun compound pair keys and triples for answer.

# for each trial, add the data for each turker to the dict
# (on each noun compound, what their response is)
def trial_dict(f_, turker_dict):
	with open(f_, 'r') as f:
		for line in f:
			line = line.strip().split(",")
			nc1 = line[1].strip('\"').strip(" ")
			nc2 = line[2].strip('\"').strip(" ")
			nc = nc1 + "|" + nc2
			worker_id = line[3].strip('\"')
			result = line[4]
			if result == "\"Not similar\"":
				r = -1
			elif result == "\"Similar\"":
				r = 1
			elif result == "\"Very Similar\"":
				r = 2
			elif result == '-1':
				r = -1
			elif result == '1':
				r = 1
			elif result == '2':
				r = 2
			elif result == '0':
				r = 0
			else:
				print line
				r = 0
			key1 = worker_id
			if key1 not in turker_dict:
				turker_dict[key1] = dict()
			key2 = nc
			if key2 not in turker_dict[key1]:
				turker_dict[key1][key2] = set()
			turker_dict[key1][key2].add(r)
	return turker_dict

# used for deleting all bad HIT trials
def validate(d):
	bad_turkers = set()
	for turker in d.keys():
		for ncp in d[turker]:
			# turker put more than one thing for a noun compound pair
			if len(d[turker][ncp]) > 1:
				bad_turkers.add(turker)
	return bad_turkers

def clean_dict(d):
	for key in validate(d):
		del d[key]
	return d

def turker_dict():
	td = trial_dict(f1, dict())
	td = trial_dict(f2, td)
	td = trial_dict(f3, td)
	td = trial_dict(f4, td)
	td = trial_dict(f5, td)
	td = trial_dict(f6, td)
	td = trial_dict(f7, td)
	td = trial_dict(f8, td)
	td = clean_dict(td)
	return td

def ncp_dict(turker_dict):
	ncp_dict = dict()
	for turker in turker_dict:
		for ncp in turker_dict[turker]:
			if ncp not in ncp_dict:
				ncp_dict[ncp] = []
			r = next(iter(turker_dict[turker][ncp]))
			ncp_dict[ncp].append(r)
			'''
			if len(ncp_dict[ncp]) > 3:
				print "Alert: " + ncp + " has more than 3 values."
				print ncp_dict[ncp]
			'''
	if 'noun_compound1|noun_compound2' in ncp_dict:
		del ncp_dict['noun_compound1|noun_compound2']
	return ncp_dict

# NUMBER OF COUNTS FOR A NOUN COMPOUND PAIR in the dict
def more3counts(ncp_dict):
	more3 = []
	num = 0
	for ncp in ncp_dict:
		if len(ncp_dict[ncp]) > 3:
			more3.append(ncp)
			print ncp + ": " + str(len(ncp_dict[ncp]))
			num += 1
	return num, more3 

def less3counts(ncp_dict):
	less3 = []
	num = 0
	for ncp in ncp_dict:
		if len(ncp_dict[ncp]) < 3:
			less3.append(ncp)
			print ncp + ": " + str(len(ncp_dict[ncp]))
			num += 1
	return num, less3

def _2counts(ncp_dict):
	two = []
	num = 0
	for ncp in ncp_dict:
		if len(ncp_dict[ncp]) == 2:
			two.append(ncp)
			print ncp + ": " + str(len(ncp_dict[ncp]))
			num += 1
	return num, two

def _1counts(ncp_dict):
	one = []
	num = 0
	for ncp in ncp_dict:
		if len(ncp_dict[ncp]) == 1:
			one.append(ncp)
			print ncp + ": " + str(len(ncp_dict[ncp]))
			num += 1
	return num, one

def one_count_file(ncp_dict):
	l = _1counts(ncp_dict)[1]
	file_str = ""
	for ncp in l:
		ncs = ncp.split("|")
		file_str += "space," + ncs[0] + "," + ncs[1] + ", kiran, \n"
	with open('1counts.csv', 'w') as f:
		f.write(file_str)

def turk_two_counts(ncp_dict):
	l = _2counts(ncp_dict)[1]
	file_str = "noun_compound1,noun_compound2\n"
	for ncp in l:
		ncs = ncp.split("|")
		file_str += ncs[0] + "," + ncs[1] + "\n"
	with open('2counts.csv', 'w') as f:
		f.write(file_str)

def equal3counts(ncp_dict):
	equal3 = []
	num = 0
	for ncp in ncp_dict:
		if len(ncp_dict[ncp]) == 3:
			equal3.append(ncp)
			#print ncp + ": " + str(len(ncp_dict[ncp]))
			num += 1
	return num, equal3

#checking to make sure each category means all different turkers
# this is just a check, after we've verified everything and built
# the td dict well, then it's all good. 
#usage:  ta.which_turkers(ta.less3counts(ncp)[1], d)
# ncp = ncp_dict, d = turker_dict
# ta = turk_analyzer
def which_turkers(ncp_set, turker_dict):
	ndict = ncp_dict(turker_dict)
	for ncp in ncp_set:
		#print "Noun Compound Pair: " + ncp + "\n"f
		num_turkers = 0
		for turker in turker_dict:
			if ncp in turker_dict[turker]:
				#print turker
				num_turkers += 1
		if num_turkers != len(ndict[ncp]):
			print "TROUBLE for " + ncp + "\n"
		#print "============================="



# Given a noun compound, we want to know how to classify it
# based on the 3- 5 responses from the different turkers

def classification_dict(ncp_dict):
	class_dict = dict()
	for ncp in ncp_dict:
		true_val = -2
		# similar, not similar, very similar, unknown
		# 1, -1, 2, 0 are the actual values
		vals = ncp_dict[ncp] # tuple of different turker responses
		val_dict = dict()
		total = 0
		# counting the frequencies of each type of response
		val_dict[-1] = 0
		val_dict[0] = 0
		val_dict[1] = 0
		val_dict[2] = 0
		for v in vals:
			if v not in val_dict:
				print "BIG PROBLEM\n"
				return
			val_dict[v] += 1
			total += 1
		total = total + 0.0 # for division

		def find_max():
			max_count = 0 # max frequency of val
			max_v = -2 # can be -1, 0, 1, or 2
			for v in val_dict:
				curr_count = val_dict[v]
				if curr_count > max_count:
					max_count = curr_count
					max_v = v
			return max_count, max_v

		max_freq, v_max = find_max()

		# if more than half agree (majority rule), say yes.
		if max_freq/ total > 0.5:
			true_val = v_max
		else:
			# otherwise, value 2 = value 1 (very similar is still similar)
			val_dict[1] += val_dict[2]
			del val_dict[2] # get rid of value 2

			new_max_freq, new_v_max = find_max()
			if new_max_freq / total > 0.5:
				true_val = new_v_max
			else:
				# if freq/total == 0.5, then we still say unknown
				# (could equal if # of turkers is 4 or 6)
				true_val = 0 

		# we want to make sure true_val changed!
		if true_val == -2:
			print "WRONG\n"
		if ncp not in class_dict:
			class_dict[ncp] = true_val

	return class_dict

# build the classifier of noun compound similarity
# based on the mech turk results
def build_classifier():
	return classification_dict(ncp_dict(turker_dict()))


#c = -1, 0, 1, 2
def classes(classification_dict, c):
	descript_str = ''
	if c == -1:
		descript_str = 'Not Similar.\n'
	elif c == 0:
		descript_str = 'Unknown.\n'
	elif c == 1:
		descript_str = 'Similar.\n'
	elif c == 2:
		descript_str = "Very Similar.\n"
	else:
		print str(c) + " is not valid.\n"
		return
	num = 0
	for ncp in classification_dict:
		if classification_dict[ncp] == c:
			print ncp + " is " + descript_str
			num += 1
	print 'There are ' + str(num) + ' instances of class ' + str(c) + '\n'
	return num




