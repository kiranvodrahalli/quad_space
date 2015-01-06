# Independent Work 2014
# Kiran Vodrahalli
# Test the VSMs against Turk results.



from fyshe_vsm import sum_model as fsm, dilation_model as fdm
from quad_vsm import coca_vanilla_model as cvm, coca_component_model as ccm, coca_weighted_model as cwm, glowbe_vanilla_model as gvm, glowbe_component_model as gcm, glowbe_weighted_model as gwm

from turk_classifier import classify as turk_classify
from turk_classifier import nc_pairs
from turk_classifier import conv_result_to_str

vsm_models = [fsm, fdm, cvm, ccm, cwm, gvm, gcm, gwm]

vsm_model_names = {fsm:'Fyshe Sum Model', fdm:'Fyshe Dilation Model', cvm:'COCA Vanilla Model', ccm:'COCA Component Model', cwm:'COCA Weighted Model', 
				   gvm:'GloWbE Vanilla Model', gcm:'GloWbE Component Model', gwm:'GloWbE Weighted Model'}

from copy import deepcopy

# convert the form of nc pair from nc1 | nc2
# into a tuple of tuples
def conv_ncp(ncp):
	ncp = ncp.strip().split('|')
	nc1 = ncp[0]
	nc2 = ncp[1]
	nc1 = nc1.split(' ')
	nc1 = (nc1[0], nc1[1])
	nc2 = nc2.split(' ')
	nc2 = (nc2[0], nc2[1])
	return (nc1, nc2)

# list of only the ones that turkers marked as similar. 
def build_similar_only_list(nc_pair_list):
	l = []
	for ncp in nc_pair_list:
		nc1, nc2 = conv_ncp(ncp)
		turk_result = turk_classify(nc1, nc2)
		if turk_result == 1:
			l.append(ncp)
		elif turk_result == 2:
			l.append(ncp)
	return l

turk_similar = build_similar_only_list(nc_pairs)

# AFTER WE RECEIVE A SIMILARITY SCORE FOR TWO NOUN COMPOUNDS, WE MUST DECIDE IF IT IS
# SIMILAR OR NOT SIMILAR. 
# -----symmetric similarity score scale-------
# similarity score > 0.99: very similar (2)
# similarity score > 0.6: similar (1)
# 0.4 <= similarity score <= 0.6: don't know (0)
# similarity score < 0.4: not similar (-1)
#---------------------------------------------
def vsm_classify(nc1, nc2, vsm):
	sim_score = vsm(nc1, nc2)
	if sim_score > 0.9999:
		return 2
	elif sim_score > 0.6:
		return 1
	elif sim_score >= 0.4:
		return 0
	else:
		return -1


# compare vsm result to turk result 
# if vsm guesses 0, then skip it
# if turk_result was also 0, then skip it regardless what vsm says
def check_pair(ncp, vsm, score):
	nc1, nc2 = conv_ncp(ncp)
	turk_result = turk_classify(nc1, nc2)
	test_result = vsm_classify(nc1, nc2, vsm)
	if turk_result == 0:
		# skip
		score[2] += 1
		# we want to know what model guessed
		'''
		print "---------------------------------------------------"
		print 'On noun compound pair (' + str(nc1) + ", " + str(nc2) + ")," + '\n'
		print "Mechanical Turk did not know.\n"
		print  vsm_model_names[vsm] + " guessed: " + str(test_result) + '\n'
		print "---------------------------------------------------"
		'''
	else:
		if test_result == 0:
			# skip
			score[2] += 1
		else:
			if test_result == turk_result:
				# correct
				score[0] += 1
			else:
				# incorrect
				score[1] += 1
				# if incorrect, we want to know discrepancy
				'''
				print "---------------------------------------------------"
				print 'On noun compound pair (' + str(nc1) + ", " + str(nc2) + ")," + '\n'
				print "Mechanical Turk answer was " + str(turk_result) + ".\n"
				print  vsm_model_names[vsm] + " guessed: " + str(test_result) + '\n'
				print "---------------------------------------------------"
				'''

# build vsm_scores from a list of noun compound pairs (nc_pair_list), (in the format nc1|nc2)
def build_scores(nc_pair_list, vsm_list):
	vsm_scores = dict()
	for vsm in vsm_list:
		if vsm not in vsm_scores:
			# each vsm function maps to a triple: [#correct, #incorrect, #skipped]
			vsm_scores[vsm] = [0, 0, 0]
	# fill vsm_scores up
	for ncp in nc_pair_list:
		for vsm in vsm_list:
			check_pair(ncp, vsm, vsm_scores[vsm])
	# check that each tuple sums up to the total number
	# of noun compound pairs there were, to make sure
	# each vsm went through all the tests.
	total = len(nc_pair_list)
	for vsm in vsm_list:
		score = vsm_scores[vsm]
		score_sum = score[0] + score[1] + score[2]
		if score_sum != total:
			print 'Error: score_sum != total'
			print 'score_sum = ' + str(score_sum)
			print 'total = ' + str(total)
			return 
	return vsm_scores


def organize_results(vsm_scores):
	scores = deepcopy(vsm_scores)
	# we compute the % correct on a run on a given noun compound pair list
	# performance is a triple [#correct, #incorrect, #skipped]
	def percent_right(performance):
		total = sum(v for v in performance)
		return 100.0*(performance[0] / (total + 0.0))
	scores = map(lambda vsm: (percent_right(scores[vsm]), vsm_model_names[vsm]), scores)
	scores = sorted(scores, reverse=True)
	return scores

# tell how each model did
def print_performance(vsm_scores):
	for vsm in vsm_model_names:
		score = vsm_scores[vsm]
		print "----------------------------------"
		print vsm_model_names[vsm] + ':'
		print '# Correct: ' + str(score[0])
		print '# Incorrect: ' + str(score[1])
		print '# Skipped: ' + str(score[2])
	print "######################################"
	print "Summary (sorted by % correct): "
	print "----------------------------------"
	ordered = organize_results(vsm_scores)
	for score, vsm_name in ordered:
		print vsm_name + ': ' + str(score) + '%' + '\n'

# AGAIN NOTE THAT IN THE MECH TURK DATA SET MOST OF IT IS 'Not Similar'
# this training set is kind of imbalanced THOUGH it may just be the case
# that most noun compound pairs are not similar. 

def run_test():
	nc_pair_list1 = nc_pairs
	nc_pair_list2 = turk_similar
	# first rank by % correct on the whole data set
	print "Ranked by % correct on all noun compound pairs:\n"
	vsm_scores1 = build_scores(nc_pair_list1, vsm_models)
	print_performance(vsm_scores1)
	# then rank by # correct on the noun compound pairs Mech Turk labeled similar
	print "Ranked by % correct on noun compound pairs that Mechanical Turk labeled 'Similar':\n"
	vsm_scores2 = build_scores(nc_pair_list2, vsm_models)
	print_performance(vsm_scores2)


# given a vsm model
# return a dict with keys in the form (turk_ans, vsm_guess)
# (where turk_ans and vsm_guess are one of  -1, 0, 1, 2)
# dict maps those keys to a list of the noun compound pairs
# which had a classification of this form for this vsm. 
def wrong_guesses(vsm, nc_pair_list):
	bad_guess = dict()
	for ncp in nc_pair_list:
		nc1, nc2 = conv_ncp(ncp)
		guess = vsm_classify(nc1, nc2, vsm)
		turk_ans = turk_classify(nc1, nc2)
		if guess != turk_ans:
			if (turk_ans, guess) not in bad_guess:
				bad_guess[(turk_ans, guess)] = []
			bad_guess[(turk_ans, guess)].append(ncp)
	return bad_guess

# dict from vsm to a dict from (turk_ans, vsm_guess) to list of noun compounds of that classification form
def vsm_wrong_guesses(nc_pair_list):
	bad_guesses_dict = dict()
	for vsm in vsm_model_names:
		if vsm not in bad_guesses_dict:
			bad_guesses_dict[vsm] = wrong_guesses(vsm, nc_pair_list)
	return bad_guesses_dict


def print_all_incorrect_guesses():
	bad_guess_dict = vsm_wrong_guesses(nc_pairs)	

	for vsm in vsm_model_names:
		# guess_pattern is (turk_ans, vsm_ans)
		for guess_pattern in bad_guess_dict[vsm]:
			print '-----------------------------------------------------\n'
			print  vsm_model_names[vsm] + ' guessed ' + conv_result_to_str(guess_pattern[1]) + ' when Mechanical Turk answered ' + conv_result_to_str(guess_pattern[0]) + ' for the following noun compound pairs: ' + '\n'
			print bad_guess_dict[vsm][guess_pattern]
			print '-----------------------------------------------------\n'








