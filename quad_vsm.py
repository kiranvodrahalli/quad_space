# Independent Work 2014
# Kiran Vodrahalli
# Quad-Space VSM model
 
from noun_compound_set import ncs
from noun_compound_set import gen_word_list
 
import numpy as np 

from util import cosine_dist
from util import geometric_mean as geo
from util import weighted_sigmoid_arithmetic_mean as wsam

from home_path import path 
from home_path import path_ending as pe 

 
 
# we need to make quadruples for each noun compound -- this is its representation
# then we need to define similarity function between noun compounds here
 
# not sure what should go in vsm_tester
 
# p is a factor we can try to optimize
# to change the way the similarity function behaves
# "sharpness"
# corpus = 'coca' or 'glowbe'
# space_type = "domain" or "action" or "qual_head" or "qual_mod"
def build_space_dict(corpus, space_type, p):
    location_str = path + 'matrix_files' + pe + corpus + '_' + space_type + pe 
    Uk = np.load(location_str + 'Uk_' + space_type + '_' + corpus + '.npy')
    Dk = np.load(location_str + 'Dk_' + space_type + '_' + corpus + '.npy')
    # note that raising a diagonal matrix
    # to the pth power is just raising each 
    # element on the diagonal to the p^th power
    Dk_p = np.power(Dk, p)
    space = np.dot(Uk, Dk_p)
 
    words = gen_word_list()
    index = 0
    if space_type == 'domain':
        # each word is a row (represent mod, head by themselves)
        # each noun compound is also a row (represent mod, head together)
        domain_dict = dict()
        for w in words: 
            if w not in domain_dict:
                domain_dict[w] = space[index]
                index += 1
        for nc in ncs:
            nc_str = nc[0] + "|" + nc[1]
            if nc_str not in domain_dict:
                domain_dict[nc_str] = space[index]
                index += 1
        return domain_dict
    elif space_type == 'action':
        # each noun compound is a row
        action_dict = dict()
        for nc in ncs:
            nc_str = nc[0] + "|" + nc[1]
            if nc_str not in action_dict:
                action_dict[nc_str] = space[index]
                index += 1
        return action_dict
    elif space_type == 'qual_head':
        # each word is a row (treat it as though it's a head)
        qual_head_dict = dict()
        for w in words: 
            if w not in qual_head_dict:
                qual_head_dict[w] = space[index]
                index += 1
        return qual_head_dict
    elif space_type == 'qual_mod':
        # each word is a row (treat it as though it's a mod)
        qual_mod_dict = dict()
        for w in words: 
            if w not in qual_mod_dict:
                qual_mod_dict[w] = space[index]
                index += 1
        return qual_mod_dict
    else:
        print 'space_type is not valid\n'
        return
 
# we will pick out a p and use that. or alternatively: we tune the parameter through cross-val
# another option: we don't tune it on the test data -- because the test data isn't varied enough. 
# but that's not true -- we can do cross-val to get ROC curves. 
 
# one reason turney's paper might do better. because they're doing parameter tuning.
# if we tune just a single parameter on the test data, that may be ok...

# no-- future work, tuning the parameter p

# p = 1 -- normal 
coca_dspace = build_space_dict('coca', 'domain', 1)
coca_aspace = build_space_dict('coca', 'action', 1)
coca_qhspace =  build_space_dict('coca', 'qual_head', 1)
coca_qmspace = build_space_dict('coca', 'qual_mod', 1)

glowbe_dspace = build_space_dict('glowbe', 'domain', 1)
glowbe_aspace = build_space_dict('glowbe', 'action', 1)
glowbe_qhspace =  build_space_dict('glowbe', 'qual_head', 1)
glowbe_qmspace = build_space_dict('glowbe', 'qual_mod', 1)

#takes in a noun compound,
#returns quad_space
#corpus = 'coca' or 'glowbe'
def parse_nc(nc, corpus):
    if corpus == 'coca':
        dspace = coca_dspace
        aspace = coca_aspace
        qhspace = coca_qhspace
        qmspace = coca_qmspace
    elif corpus == 'glowbe':
        dspace = glowbe_dspace
        aspace = glowbe_aspace
        qhspace = glowbe_qhspace
        qmspace = glowbe_qmspace
    else:
        print "Not a valid corpus.\n"
        return
    mod = nc[0] # modifier
    head = nc[1] # head
    nc_str = nc[0] + '|' + nc[1] #both

    # domain space (for full noun compound)
    dom_full_v = dspace[nc_str]
    # domain space (for the head)
    dom_head_v = dspace[head]
    # action space
    action_v = aspace[nc_str]
    # qualifier head space
    qualh_v = qhspace[head]
    # qualifier modifier space
    qualm_v = qmspace[mod]

    return (dom_full_v, dom_head_v, action_v, qualh_v, qualm_v)


coca_nc_dict = {nc: parse_nc(nc, 'coca') for nc in ncs}
glowbe_nc_dict = {nc: parse_nc(nc, 'glowbe') for nc in ncs}


# ---------------SIMILARITY FUNCTIONS---------------------------

# noun compound representations will be treated at first as a quintuple
# of the vectors from each of the four spaces (domain,  action, qual_head, qual_mod)
# then we get 5 vectors: domain: full noun compound, domain: head, action: full noun compound, 
# qual_head: head, qual_mod: mod
# then these 5-tuple will be used in some way to calculate the similarity
# between two noun compounds, often using cosine distances and then composing 
# a set of cosine distance functions on different spaces. 

# each similarity function takes in two representations of noun compound (5-tuple of vectors)

# FUTURE WORK: test other similarity functions, and composition functions other than
# geometric mean and 

# FUTURE WORK: use neural nets to learn similarity composition functions for noun compounds


# returns a 5-tuple of distances between each of the components
# of two noun compound representations (nc_rep1, nc_rep2)
# then, this tuple of distances can be composed in different ways
# by a similarity function
# NOTE THAT SINCE WE ARE COMPARING TWO NOUN COMPOUNDS, THE FOLLOWING IS TRUE:
# each noun compound has an underlying structure. we want to compare each 
# facet of that structure in a one-to-one manner, and then compose appropriately. 
# moreover, there are 4 vector spaces. comparisons must take place between 
# vectors inside the same vector space. so we might as well compare 1-1. 
# (i.e. component wise, and then use a similarity function to represent the
#  structure of the noun compound)
# since distances are cosine, each distance is between -1 and 1
def dist_tuple(nc_rep1, nc_rep2):

    # domain nouns related to the noun compound
    # space is a broad measure of similarity
    domain_full1 = nc_rep1[0]
    domain_full2 = nc_rep2[0]
    dist0 = cosine_dist(domain_full1, domain_full2)

    # domain nouns related to the head
    # space is analagous to the head
    domain_head1 = nc_rep1[1]
    domain_head2 = nc_rep2[1]
    dist1 = cosine_dist(domain_head1, domain_head2)

    # verbs related to the noun compound
    # space is measuring the action of the modifier on the head
    action1 = nc_rep1[2]
    action2 = nc_rep2[2]
    dist2 = cosine_dist(action1, action2)

    # adjectives that act on the head
    # space is analagous to modifier
    qualifier_head1 = nc_rep1[3]
    qualifier_head2 = nc_rep2[3]
    dist3 = cosine_dist(qualifier_head1, qualifier_head2)

    # adjectives the modifier might be like
    # space is analagous to modifier
    qualifier_mod1 = nc_rep1[4]
    qualifier_mod2 = nc_rep2[4]
    dist4 = cosine_dist(qualifier_mod1, qualifier_mod2)

    return (dist0, dist1, dist2, dist3, dist4)


 
# we want these to satisfy eq (26) - (29) in Turney2012
# see pages (554-555); (560-561) in Turney2012
# for mode of explanation

# similarity composition function should take in a list and return 
# a value in the range [0, 1]. 

# ---------------------CANDIDATE COMPOSITION FUNCTIONS---------------------

# ---------------------GEOMETRIC MEAN WITH CUTOFF--------------------
# geo()
# note that cutoff geometric mean is aggressive in proclaiming not similar:
# if one component is 0, the whole thing gets zeroed. so we will be more likely 
# to mistakenly claim not similar 
# also note that geo: [-1, 1] --> [0, 1]
# the reason why we don't claim that theta = pi (-1 scores) are similar is because
# semantic vector spaces work more based on clustering -- not algebra. 
# things "nearby" a vector are similar to it, where "nearby" is a cluster of a certain size.
# therefore, we just have to throw out the exact values -- if the similarity is too far apart, 
# (i.e., it is negative, after all), then let's just say it is 0. that is easiest, and it makes sense.
# (we're allowing all positive cosine distances for the clustering range -- it doesnt make much sense
#  to have the allowed cluster size span the whole space! it wouldn't be much of a cluster then.)


# -------------------- SHIFTED SIGMOID ON ARITHMETIC MEAN --------------------
# wsam()
# first we set all negative valued similarities equal to 0, by the clustering argument above.
# we use arithmetic mean to avoid automatically sending stuff to 0.
# and then let the sigmoid achieve a smoother distribution
# can actually generalize to weighted average.  
# Then we take the arithmetic mean, and apply a sigmoid function (lower bound 0, upper bound 1) to it with two tunable parameters
# 1) controlling the derivative (0 -> infinity): (uniform -> really steep)
# 2) controlling the point of shift (i.e. at what point do we suddenly start really sending stuff to 1 -- could be at .5, or maybe HIGHER like .7)
#   note: this allows us to justify a similarity score scale along these lines: 
#    # -----symmetric similarity score scale-------
#       similarity score > 0.95: very similar (2)
#       similarity score > 0.6: similar (1)
#       0.4 <= similarity score <= 0.6: don't know (0)
#       similarity score < 0.4: not similar (-1)

# this composition function is not as strict in that if something is <= than 0, 
# we don't immediately zero out the whole thing. it could just be that that similarity
# measure (of, what, 5?) is not significant and the rest are really significant.
# it also sends similarity values much closer to mean
# it may be more likely to send to extremes -- but we can fix this with the tunable parameters
# the sigmoid also has the effect of getting rid of ambiguity around middle scores where you can't
# tell which side it's on. this way, we uniformly send ambiguous scores to one side or the other.

# IN THIS PAPER, we pick the parameters for the sigmoid to get what seems like a nice curve. 

# IN THIS PAPER, we may not necessary actually tune these parameters. 
# could be future work (in a neural net model, for instance)
# AN IMPORTANT PARADIGM MIGHT BE DEFINE parameters on similarity functions
# and TUNE THOSE instead of tuning other stuff. (i mean, tune other stuff also, but this could be good.)
# Turney comments that he wants to keep similarity function simple and parameter free, but 
# parameters might be good here. 


# just apply the geo similarity composition function to all of them
def geo_vanilla_sim(nc_rep1, nc_rep2):
    d1, d2, d3, d4, d5 = dist_tuple(nc_rep1, nc_rep2)
    return geo([d1, d2, d3, d4, d5])

# first do compositions to isolate the individual 
# components of the noun compound representation
# (the mod, the head, the action, the mod_head)
# then using these as building blocks, write a function)
# geo is similarity composition function
def geo_component_sim(nc_rep1, nc_rep2):
    # note that all of these values are between -1 and 1
    d1, d2, d3, d4, d5 = dist_tuple(nc_rep1, nc_rep2)

    # most important is the similarity of 
    # the action of the modifier on the head
    # it is characterized by the action space, since 
    # the action space is built from verbs related to
    # both the modifier and the head words, and can constitute
    # an action of the modifier on the head. 
    # "air temperature": you MEASURE the temperature of the air.
    # and also characterized by the qualifier head space. 
    # the qualifier head space space is built from adjectives
    # that act on the head part of the noun compound. 
    # thus we combine these to derive a distance measurement of the action.
    function_sim = geo([d3, d4])

    # however, the qualifier head space also helps describe the modifier
    # combine the two qualifier spaces to get a measurement of 
    # modifier similarity
    modifier = geo([d4, d5])

    head = d2

    # then we can build our domain similarity from the modifier and the head
    mod_head = geo([modifier, head])

    # but we also already have domain space for mod_head
    domain_sim = geo([mod_head, d1])

    # now we have the functional similarity and the domain similarity
    # and they are both in the range [0, 1]. 
    # let's take a weighted average as the result. 
    # we want to reflect the fact that the most important 
    # aspect of similarity is a similar relation between head and modifier, 
    # and that a secondary aspect is the similarity of the domains. 

    function_weight = 0.8
    domain_weight = 0.2
    return function_weight*function_sim + domain_weight*domain_sim



# we can also define specific weights for each of the distances and use a scheme simliar to
# shifted sigmoid on weighted arithmetic mean 

def weighted_sim(nc_rep1, nc_rep2):
    # note that all of these values are between -1 and 1
    d1, d2, d3, d4, d5 = dist_tuple(nc_rep1, nc_rep2)
    dist_array = [d1, d2, d3, d4, d5]

    dom_all_weight = .05
    dom_head_weight = .20
    action_weight = .35
    qualh_weight = .25
    qualm_weight = .15

    weight_array = [dom_all_weight, dom_head_weight, action_weight, qualh_weight, qualm_weight]

    return wsam(dist_array, weight_array, 0.00007, 20, 4)


def coca_rep(nc1, nc2, func):
    rep1 = coca_nc_dict[nc1]
    rep2 = coca_nc_dict[nc2]
    return func(rep1, rep2)

def glowbe_rep(nc1, nc2, func):
    rep1 = glowbe_nc_dict[nc1]
    rep2 = glowbe_nc_dict[nc2]
    return func(rep1, rep2)

# These functions take in 2 noun compounds, represented as (mod, head)
def coca_gv_sim(nc1, nc2):
    return coca_rep(nc1, nc2, geo_vanilla_sim)
def coca_comp_sim(nc1, nc2):
    return coca_rep(nc1, nc2, geo_component_sim)
def coca_weight_sim(nc1, nc2):
    return coca_rep(nc1, nc2, weighted_sim)

def glowbe_gv_sim(nc1, nc2):
    return glowbe_rep(nc1, nc2, geo_vanilla_sim)
def glowbe_comp_sim(nc1, nc2):
    return glowbe_rep(nc1, nc2, geo_component_sim)
def glowbe_weight_sim(nc1, nc2):
    return glowbe_rep(nc1, nc2, weighted_sim)


# models are just a similarity function!
# takes in two noun compounds represented as (mod, head) tuples. 
# returns a measure of similarity

# could simply introduce parameters for at least the weighted_sim... 
# then could train on that

coca_vanilla_model = coca_gv_sim
coca_component_model = coca_comp_sim
coca_weighted_model = coca_weight_sim

glowbe_vanilla_model = glowbe_gv_sim
glowbe_component_model = glowbe_comp_sim
glowbe_weighted_model = glowbe_weight_sim








