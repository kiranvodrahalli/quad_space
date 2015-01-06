#Kiran Vodrahalli
#Independent Work 2014
#parse Amazon Turk results
#analyze which turkers to remove, etc.

from home_path import path 
from home_path import path_ending as pe 

f_1 = path + "mech_turk_results" + pe + "mech_turk_data1_round1.csv"
f_2 = path + "mech_turk_results" + pe + "mech_turk_data1_round2.csv"
f_3 = path + "mech_turk_results" + pe + "mech_turk_data1_round3.csv"
f_4 = path + "mech_turk_results" + pe + "mech_turk_data1_repeat2.csv"

#dict from string of nc pair to tuple of answers (only if all different ID)
nc_pair_dict = dict()

#dict of turkers
turker_dict = dict()

def turker_names(f):
	names = set()
	with open(f, 'r') as f1:
		for line in f1:
			line = line.strip().split(",")
			names.add(line[3].strip('\"'))
	return names

def build_dict_for_file(f):
	ncpd = dict()
	for line in f:
		line = line.strip().split(",")
		hit_id = line[0]
		nc1 = line[1].strip('\"').strip(" ")
		nc2 = line[2].strip('\"').strip(" ")
		worker_id = line[3].strip('\"')
		if worker_id not in turker_dict:
			turker_dict[worker_id] = set()
		result = line[4]
		if result == "\"Not similar\"":
			r = -1
		elif result == "\"Similar\"":
			r = 1
		elif result == "\"Very Similar\"":
			r = 2
		else:
			r = 0
		date = line[5]
		key = nc1 + "|" + nc2
		turker_dict[worker_id].add(key)
		#just in case there are duplicates
		#should not be
		if key not in ncpd:
			ncpd[key] = []
		ncpd[key].append((worker_id, r))
	return ncpd

ncpd1 = dict()
ncpd2 = dict()
ncpd3 = dict()



with open(f_1, 'r') as f1, open(f_2, 'r') as f2, open(f_3, 'r') as f3:
	ncpd1 = build_dict_for_file(f1)
	ncpd2 = build_dict_for_file(f2)
	ncpd3 = build_dict_for_file(f3)
bad_turkers = 0
total_lines = 0
triple_turker_set = set()
double_turker_set = set()
bad_turker_dict = dict()
# turkers who respond to same question more than once w/diff answers
really_bad_turkers = set()
with open(f_3, 'r') as f:
	for line in f:
		total_lines += 1
		line = line.strip().split(",")
		key = line[1].strip('\"').strip(" ") + "|" + line[2].strip('\"').strip(" ")

		if (len(ncpd1[key]) != 1) and (len(ncpd2[key]) != 1) and (len(ncpd3[key]) != 1):
			print "check length of " + key
			print "ncpd1: " + str(len(ncpd1[key])) + ", " + "ncpd2: " + str(len(ncpd2[key])) + ", " + "ncpd3: " + str(len(ncpd3[key]))
		else:
			tuple1 = ncpd1[key][0]
			tuple2 = ncpd2[key][0]
			tuple3 = ncpd3[key][0]
			t1 = tuple1[0].strip('\"')
			t1ans = str(tuple1[1])
			t2 = tuple2[0].strip('\"')
			t2ans = str(tuple2[1])
			t3 = tuple3[0].strip('\"')
			t3ans = str(tuple3[1])
			#print (tuple1[1], tuple2[1], tuple3[1])
			turker = True 
			if t1 == t2:
				turker = False
			if t1 == t3:
				turker = False
			if t2 == t3:
				turker = False	
			if t1 == t2 and t2 == t3:
				triple_turker_set.add(t1)
				if t1 not in bad_turker_dict:
					bad_turker_dict[t1] = []
				bad_turker_dict[t1].append(key)
				if t1ans != t2ans:
					print "ALERT: same turker (" + t1 + ") reported diff answer for same key at trials 1 and 2: " + key
					really_bad_turkers.add(t1)
				if t3ans != t2ans:
					print "ALERT: same turker (" + t1 + ") reported diff answer for same key at trials 2 and 3: " + key
				if t1ans != t3ans:
					print "ALERT: same turker (" + t1 + ") reported diff answer for same key at trials 1 and 3: " + key

			if t1 == t2 and t2 != t3:
				double_turker_set.add(t1)
				if t1 not in bad_turker_dict:
					bad_turker_dict[t1] = []
				bad_turker_dict[t1].append(key)
				if t1ans != t2ans:
					print "ALERT: same turker (" + t1 + ") reported diff answer for same key: " + key
					really_bad_turkers.add(t1)
			if t1 == t3 and t2 != t3:
				double_turker_set.add(t1)
				if t1 not in bad_turker_dict:
					bad_turker_dict[t1] = []
				bad_turker_dict[t1].append(key)
				if t1ans != t3ans:
					print "ALERT: same turker (" + t1 + ") reported diff answer for same key: " + key
					really_bad_turkers.add(t1)
			if t2 == t3 and t1 != t2:
				double_turker_set.add(t2)
				if t2 not in bad_turker_dict:
					bad_turker_dict[t2] = []
				bad_turker_dict[t2].append(key)
				if t3ans != t2ans:
					print "ALERT: same turker (" + t2 + ") reported diff answer for same key: " + key
					really_bad_turkers.add(t2)

			if turker is False:
				print "check turker for " + key
				bad_turkers += 1
				print (t1 + ": " + t1ans, t2 + ": " + t2ans, t3 + ": " + t3ans)
			else:
				nc_pair_dict[key] = (tuple1[1], tuple2[1], tuple3[1])

print "total lines: " + str(total_lines)
print "number of bad turkers: " + str(bad_turkers)

for turker in double_turker_set:
	print turker + " is a double turker"
for turker in triple_turker_set:
	print turker + " is a triple turker"

to_repeat = set()
#for every turker in the double turker set
for turker in double_turker_set:
	print "Bad Turker " + turker + " did these more than once: "
	for item in bad_turker_dict[turker]:
		ltup = item.split("|")
		tup = (ltup[0], ltup[1])
		print tup
		to_repeat.add(tup)
	print "---------------"

for turker in really_bad_turkers:
	print "Turker " + turker + " is a really bad turker." 

def build_repeat_csv(to_repeat, i):
	file_str = "noun_compound1, noun_compound2\n"
	for item in to_repeat:
		file_str += item[0] + "," + item[1] + "\n"
	with open(path + 'mech_turk_inputs' + pe + "ncs_repeat" + str(i) + ".csv", 'w') as f:
		f.write(file_str)

to_repeat2 = set()
# for all bad turkers, we want to replace them completely
# we counted them once for their repeat if they did it twice
# now we replace their original as well, because they were a bad turker
for turker in really_bad_turkers:
	for item in turker_dict[turker]:
		ltup = item.split("|")
		tup = (ltup[0], ltup[1])
		to_repeat2.add(tup)

to_repeat3 = set()
# the only triple turker is a bad turker
# so replace all of this person's
# we need to do it a third time.
for turker in triple_turker_set:
	for item in turker_dict[turker]:
		ltup = item.split("|")
		tup = (ltup[0], ltup[1])
		to_repeat3.add(tup)



