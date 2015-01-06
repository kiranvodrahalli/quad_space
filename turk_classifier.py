# Independent Work
# Kiran Vodrahalli
# turk classification results

from turk_analyzer import build_classifier
from turk_analyzer import classes


classifier = build_classifier()

nc_pairs = classifier.keys()


# How many are there of each class? 

'''

print 'How many noun compound pairs for each class?\n'
print '-----------------------------------------------'
not_similar = classes(classifier, -1) # answer = 4380
print '-----------------------------------------------'
unknown = classes(classifier, 0)   # answer = 90
print '-----------------------------------------------'
similar = classes(classifier, 1)   # answer = 376
print '-----------------------------------------------'
v_similar = classes(classifier, 2) # answer = 56
print '-----------------------------------------------'
'''

def conv_result_to_str(result):
	ans = ""
	if result == -1:
		ans = "Not similar"
	elif result == 0:
		ans = "Unknown"
	elif result == 1:
		ans = "Similar"
	elif result == 2:
		ans = "Very Similar"
	else:
		print "You did something weird:"
		print key
		print result
		return 
	return ans

# Empirical results
# takes in two noun compounds of the form (mod, head) tuples. 
# returns the classification (-1, 0, 1, 2)
def classify(nc1, nc2):
	nc1_str = nc1[0] + ' ' + nc1[1]
	nc2_str = nc2[0] + ' ' + nc2[1]
	key = nc1_str + "|" + nc2_str
	result = classifier[key]
	#ans = conv_result_to_str(result)
	#print ans
	return result


