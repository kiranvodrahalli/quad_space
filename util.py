# Independent Work 2014
# Kiran Vodrahalli
# utility functions
# ppmi, rank_k approximation

import numpy as np 

from numpy.linalg import svd
from numpy import shape
from numpy.linalg import norm
from numpy import dot

#from scipy.linalg import svd
from math import log
from math import e



## GOOD SIGMOID PARAMETERS TO USE
# empirically what we want.
# p1 = .00007
# p2 = 20
# p3 = 4

# computes arithmetic mean
# after zeroing negative elements
# according to weights in w (same length as l)
# then takes the sigmoid function of the 
# arithmetic mean
# sigmoid has parameters controlling sharpness of slope
# and location of concavity change:
# p1 controls shift
# p2 controls slope
# p3 affects both
def weighted_sigmoid_arithmetic_mean(l, w, p1, p2, p3):
	def zify(v):
		if v < 0:
			return 0
		else:
			return v
	l = map(zify, l)
	lv = np.array(l)
	wv = np.array(w)
	mean = np.dot(lv, wv)
	def sigmoid(x, a, b, c):
		return (a + 0.0)/ (a + c*pow(e, -1.0*b*x))
	return sigmoid(mean, p1, p2, p3)

# uniform weights
def sigmoid_arithmetic_mean(l, p1, p2, p3):
	n = len(l)
	w = []
	for i in range(n):
		w.append(1)
	return weighted_sigmoid_arithmetic_mean(l, w, p1, p2, p3)

# computes the modified geometric mean
# of a list of values
# if any of the values is <= 0, the result
# is 0. (See Dual-space paper by Turney, Section 3.7)
# (geometric mean doesn't work for negatives)
# note that this will be applied to lists with numbers
# in the range [-1, 1]. 
# in cosine_dist, -1 means opposite -- and therefore, 
# not 'similar'. it's not really true that
# vectors that are geometrically opposite are opposites
# along the same axis, so we set it to zero. 
def geometric_mean(l):
	n = len(l)
	pwr = 1.0 / (n + 0.0)
	gt_zero = reduce(lambda acc, v: ((v > 0) and acc), l, True)
	if gt_zero:
		return pow(reduce(lambda acc, v: acc*v, l, 1), pwr)
	else:
		return 0.0


# cosine distance function between two vectors
# we normalize length to measure in cosine 
# return a value between -1 and 1
# closer to 1 means similar
# closer to 0 means dissimilar
# closer to -1 means opposite similar
def cosine_dist(v1, v2):
	if len(shape(v1)) == 1:
		v1 = np.matrix(v1)
	if len(shape(v2)) == 1:
		v2 = np.matrix(v2)
	return dot((v1/(0.0 + norm(v1))), (v2.T/(0.0 + norm(v2))))[0, 0]


def ppmi_transform(fmatrix):
	row, col = shape(fmatrix)
	new_mat = np.zeros((row, col))

	total_sum = 0
	for i in range(0, row):
		for j in range(0, col):
			total_sum += fmatrix[i][j]
	total_sum = total_sum + 0.0

	row_sums = []
	for i in range(0, row):
		isum = 0
		for j in range(0, col):
			isum += fmatrix[i][j]
		row_sums.append(isum)


	col_sums = []
	for j in range(0, col):
		jsum = 0
		for i in range(0, row):
			jsum += fmatrix[i][j]
		col_sums.append(jsum)


	for i in range(0, row):
		for j in range(0, col):
			if fmatrix[i][j] == 0:
				# - infinity < 0
				new_mat[i][j] = 0.0
			else:
				pij = (fmatrix[i][j] + 0.0) / total_sum
				pi = (row_sums[i] + 0.0)/ total_sum
				pj = (col_sums[j] + 0.0) / total_sum
				pmi_ij = log((pij* 1.0) / (pi * pj * 1.0))
				if pmi_ij < 0:
					pmi_ij = 0
				new_mat[i][j] = pmi_ij
	return new_mat


# http://www.p2p-conference.org/p2p14/wp-content/uploads/2014/09/206.P2P2014_033.pdf
# See Table 1 -- square sum up to k / total square sum > 0.9 
# this is a common choice for choosing the number of singular values
def rank_k(M):
	U, s, Vt = svd(M, full_matrices = False)
	V = Vt.T
	D = np.diag(s)
	tot = sum(v*v for v in s) + 0.0
	curr = 0.0
	k = 0
	while (curr/tot) < 0.9:
		curr += (s[k]*s[k])
		k += 1
	Dk = D[:k, :k]
	print '# singular values: ' + str(k)
	Uk = U[:, :k]
	Vk = V[:, :k]
	# WE ACTUALLY ONLY MULTIPLY U AND D, not V.T
	# U is rows, D is singular values, V is cols
	# (in order to compare rows)
	#return np.dot(U, D)#np.dot(U, np.dot(D, V.T))
	# we actually want to save these two separately
	# so that we can compare rows (Uk)
	# and later perhaps introduct an exponent for D (i.e. D^p)
	return Uk, Dk, Vk


