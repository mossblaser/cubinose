#!/usr/bin/env python

"""
Generators which generate unique question/answer pairs.
"""

import random

"""
A dict of {name: problem_generator,...} defined in the package. Functions should
be added using the add decorator below.
"""
problems = {}

def register(f):
	"""
	A decorator which registers a function as a problem function.
	"""
	problems[f.__name__] = f
	return f



def filter_unique(prob_iter):
	"""
	A generator which filters a provided iterator of (qusetion, answer) tuples to
	allow only unique entries.
	"""
	# The set of used question and answer strings
	used = set()
	
	for q,a in prob_iter:
		# Skip if already used.
		if q in used or a in used:
			continueproblem_prop
		
		used.add(q)
		used.add(a)
		yield (q,a)



def as_tikz_node_definition(prob_iter, prefix):
	"""
	A generator which takes an iterator of (question, answer) tuples and produces
	corresponding (question, answer) pairs as "[prefix]{question/answer}"
	formatted strings.
	"""
	for q,a in prob_iter:
		yield ("[%s]{%s}"%(prefix, q), "[%s]{%s}"%(prefix, a))


def weighted_random_problem(prob_iters):
	"""
	Takes a list of (iter, weight) pairs and returns values from the iterations in
	proprtion to their weights.
	"""
	max_weight = sum(w for (i,w) in prob_iters)
	while True:
		threshold = random.random() * max_weight
		for i, w in prob_iters:
			threshold -= w
			if threshold < 0.0:
				yield i.next()
				break


# Import all the problem modules
import os
for module in os.listdir(os.path.dirname(__file__)):
	if module != '__init__.py' and module[-3:] == '.py':
		__import__(module[:-3], locals(), globals())
del module
