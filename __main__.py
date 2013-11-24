#!/usr/bin/env python

import sys
import optparse

import tile, shapes, problems

def get_help_string():
	shape_docs   = "\n\n".join("%s:\n%s"%(f.__name__, f.__doc__) for f in shapes.shapes.values())
	problem_docs = "\n\n".join("%s:\n%s"%(f.__name__, f.__doc__) for f in problems.problems.values())
	
	return "usage: --shape SHAPE [SHAPE_ARGUMENT...] \\\n" + \
	       "       --problem PROBLEM [PROBLEM_ARGUMENT...] \\\n" + \
	       "                 [--prefix PREFIX] \\\n" + \
	       "                 [--proportion PROPORTION]\n" + \
	       "\n" + \
	       "Shapes:\n" + \
	       shape_docs + \
	       "\n" + \
	       "\n" + \
	       "Problems:\n" + \
	       problem_docs + \
	       "\n"
	


if __name__=="__main__":
	shape_options = None
	problem_options = []
	
	# Divide options between the shape and problem
	STATE_SHAPE = object()
	STATE_PROBLEM = object()
	state = None
	for arg in sys.argv[1:]:
		# Change state when encountering --state/--problem
		if arg.startswith("--shape"):
			state = STATE_SHAPE
			shape_options = []
		elif arg.startswith("--problem"):
			state = STATE_PROBLEM
			problem_options.append([])
		
		# Record the option
		if state is None and arg in ("-h", "--help"):
			sys.stdout.write(get_help_string())
			sys.exit(0)
		elif state is STATE_SHAPE:
			shape_options.append(arg)
		elif state is STATE_PROBLEM:
			problem_options[-1].append(arg)
		else:
			sys.stderr.write("Unexpected argument '%s'. Usage:\n"%arg)
			sys.stderr.write(get_help_string())
			sys.exit(-1)
	
	# Parse the shape arguments
	shape_parser = optparse.OptionParser()
	shape_parser.add_option( "--shape", dest="shape"
	                       , help = "the shape of the tesselation"
	                       , choices = shapes.shapes.keys()
	                       , nargs = 1
	                       )
	shape_args = shape_parser.parse_args(shape_options)
	
	# Parse each of the problem arguments
	problem_args = []
	for args in problem_options:
		problem_parser = optparse.OptionParser()
		problem_parser.add_option( "--problem", dest="problem"
		                         , help = "a type of problem to include"
		                         , choices = problems.problems.keys()
		                         , nargs = 1
		                         )
		problem_parser.add_option( "--prefix", dest="prefix"
		                         , help = "a prefix to insert before questions and answers"
		                         , nargs = 1
		                         , default = ""
		                         )
		problem_parser.add_option( "--proportion", dest="proportion"
		                         , help = "the proportion of q/a pairs this question should account for"
		                         , nargs = 1
		                         , type = float
		                         , default = 1.0
		                         )
		problem_args.append(problem_parser.parse_args(args))
	
	# Generate the tiles
	tiles = shapes.shapes[shape_args[0].shape](*map(eval, shape_args[1]))
	
	# Create the question generators (as (iterator, weight) pairs)
	problem_iters = []
	for problem in problem_args:
		problem_iter = problems.problems[problem[0].problem](*map(eval, problem[1]))
		problem_prop = problem[0].proportion
		
		problem_iters.append(( problems.as_tikz_node_definition(problem_iter, problem[0].prefix)
		                     , problem_prop
		                     ))
	problem_iter = problems.weighted_random_problem(problem_iters)
	
	# Allocate questions to tiles
	tile.add_questions(tiles, problem_iter)
	
	# Print the output
	sys.stdout.write(tile.to_tikz(tiles))
