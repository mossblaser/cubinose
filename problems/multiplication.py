#!/usr/bin/env python

"""
Simple multiplication problems.
"""

import random
import operator

import problems

def gen_mult_problem(num_digits):
	"""
	Takes a list of numbers of digits for the numbers in the problem. Returns a
	pair (question,answer) where question is a LaTeX formatted multiplication
	problem with each number containing the given number of digits and answer is a
	LaTeX formatted integer answer.
	
	Never generates the numbers "1", "10", "100", etc. to make things harder.
	"""
	numbers = [random.randint((10**(digits-1))+1, (10**digits) - 1) for digits in num_digits]
	
	return ( "$%s$"%(r" \times ".join(map(str, numbers)))
	       , "$%d$"%(reduce(operator.mul, numbers))
	       )


@problems.register
def multidigit_multiplication(num_digits):
	"""
	Generate a number of multiplication problems.
	
	num_digits is a list containing the number of digits to be contained in each
	term of a multiplication problem. For example, [1,2,3] generates three-term
	problems with the first term containing one digit, the second two digits and
	the third containing three digits.
	"""
	while True:
		yield gen_mult_problem(num_digits)

