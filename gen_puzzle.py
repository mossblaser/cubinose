#!/usr/bin/env python

import random
import operator

#                    ______
#      /\            \    /
# --> /  \    or  --> \  /
#    /____\            \/
LEFT_EDGE  = "LEFT_EDGE"

#                 ______
#   /\            \    /
#  /  \ <--   or   \  / <--
# /____\            \/
RIGHT_EDGE = "RIGHT_EDGE"

#    |
#   \|/
# ______
# \    /
#  \  /
#   \/
TOP_EDGE     = "TOP_EDGE"

#   /\
#  /  \
# /____\
#   /|\
#    |
BOTTOM_EDGE     = "BOTTOM_EDGE"


def opposite(edge):
	"""
	Given an edge, returns the corresponding opposite edge
	"""
	if   edge == TOP_EDGE:    return BOTTOM_EDGE
	elif edge == BOTTOM_EDGE: return TOP_EDGE
	elif edge == LEFT_EDGE:   return RIGHT_EDGE
	elif edge == RIGHT_EDGE:  return LEFT_EDGE
	else:
		assert(False)


class Tile(object):
	"""
	Represents a single tile in a puzzle.
	"""
	
	def __init__(self):
		self.edges = {}
	
	
	def add_edge(self, side, label, colour):
		"""
		Set the label (and colour) of an edge of the tile. It is the responsibility
		of the caller to sensibly choose which edges are labelled. That is, the tile
		doesn't know its orientation and so doesn't know if it is sensible to have a
		top or bottom side.
		"""
		assert(side not in self.edges)
		assert(len(self.edges) < 3)
		assert(not (side in (TOP_EDGE,BOTTOM_EDGE) and opposite(side) in self.edges))
		self.edges[side] = (label,colour)


def generate_puzzle(size, q_a_pairs):
	r"""
	Generates a triangluar puzzle of a given size using questions from the list
	q_a_pairs.
	
	Returns a dictionary {(x,y):Tile,...} for a set of tiles arranged like so with
	tile edges being assigned a random subset of the q_a_pairs questions.
	
	        /\
	       /02\
	      /____\
	     /\    /\
	    /01\11/21\
	   /____\/____\
	  /\    /\    /\
	 /00\10/20\30/40\
	/____\/____\/____\
	
	`-------v--------'
	    size = 5
	"""
	assert size%2 == 1, \
		"Must be an odd size."
	
	assert len(q_a_pairs) >= 3*((size**2 - 1)/8), \
		">= %d questions required."%(3*((size**2 - 1)/8))
	
	tiles = {}
	
	# Shuffle the questions
	random.shuffle(q_a_pairs)
	q_a_iter = iter(q_a_pairs)
	
	# Generate a pyramid of triangular tiles
	for y in range(size):
		for x in range(size - 2*y):
			tiles[(x,y)] = Tile()
	
	# Place q/a pairs on touching edges
	for (x,y) in tiles.iterkeys():
		for side, pos in [ (RIGHT_EDGE, (x+1, y))
		                 , (TOP_EDGE, (x-1, y+1))
		                 ]:
			if pos in tiles and not (side == TOP_EDGE and x%2 == 0):
				# Randomly choose which edge gets the question and which gets the answer
				q,a,c = list(q_a_iter.next())
				q_a = [q,a]
				random.shuffle(q_a)
				tiles[(x,y)].add_edge(side, q_a[0], c)
				tiles[pos].add_edge(opposite(side), q_a[1], c)
	
	return tiles


def puzzle_to_tikz(tiles):
	"""
	Convert a dict {(x,y):Tile,...} into a string containing a valid LaTeX/TikZ
	document with the tiling in.
	"""
	
	out = r"""
			\documentclass[12pt]{standalone}
			
			\usepackage{ifthen}
			\usepackage[cm]{sfmath}
			
			\usepackage{tikz}
			\usetikzlibrary{shapes.geometric}
			\usetikzlibrary{positioning}
			
			% Produce a trianglar tile with labels on each side
			% #1 position
			% #2 name
			% #3 points up? (1/0)
			% #4 Top/Bottom node string (e.g. "[red] {Question}")
			% #5 Left node string (e.g. "[red] {Question}")
			% #6 Right node string (e.g. "[red] {Question}")
			\newcommand{\tri}[6]{
				\coordinate (#2 start) at ([x=(0:0.5),y=(90:0.8660254)]#1);
				
				\ifthenelse{\equal{#3}{up}}{
					\draw (#2 start) -- +(0:1) -- +(60:1) -- cycle;
					\coordinate (#2 center) at ([shift={(30:0.57735027)}]#2 start);
					\coordinate (#2 left) at ([shift={(60:0.5)}]#2 start);
					\coordinate (#2 right) at ([shift={(0:1)}]#2 start);
					\coordinate (#2 right) at ([shift={(90+30:0.5)}]#2 right);
					\coordinate (#2 bottom) at ([shift={(0:0.5)}]#2 start);
					
					\node [rotate=180,below=of #2 bottom] #4;
					\node [rotate= 60,below=of #2 left] #5;
					\node [rotate=-60,below=of #2 right] #6;
				}{
					\coordinate (#2 start) at ([shift={(0.5,0)}]#2 start);
					\draw (#2 start) -- +(60:1) -- +(90+30:1) -- cycle;
					\coordinate (#2 center) at ([shift={(90:0.57735027)}]#2 start);
					\coordinate (#2 left) at ([shift={(90+30:0.5)}]#2 start);
					\coordinate (#2 right) at ([shift={(60:0.5)}]#2 start);
					\coordinate (#2 top) at ([shift={(60:1)}]#2 start);
					\coordinate (#2 top) at ([shift={(180:0.5)}]#2 top);
					\node [rotate=  0,below=of #2 top] #4;
					\node [rotate=180+60,below=of #2 right] #6;
					\node [rotate=180-60,below=of #2 left] #5;
				}
			}
			
			\begin{document}
				\begin{tikzpicture}[scale=4, node distance=0, minimum width=0, minimum height=0]
	"""
	
	# Produce the tiles
	for pos, tile in tiles.iteritems():
		# Determine orientation of tile
		top_or_btm = TOP_EDGE if pos[0]%2==1 else BOTTOM_EDGE
		
		# Determine the label/colour for each tile
		tb_l, tb_c = tile.edges.get(top_or_btm, ["",""])
		l_l, l_c = tile.edges.get(LEFT_EDGE, ["",""])
		r_l, r_c = tile.edges.get(RIGHT_EDGE, ["",""])
		
		# Produce the relevent \tri command
		out += "\\tri{%d,%d}{tile %d %d}{%s}{[%s]{%s}}{[%s]{%s}}{[%s]{%s}};\n"%(
			pos[1] + pos[0], pos[1],
			pos[0], pos[1],
			"up" if pos[0]%2 == 0 else "down",
			tb_c, tb_l,
			l_c, l_l,
			r_c, r_l,
		)
	
	out += r"""
			\end{tikzpicture}
		\end{document}
	"""
	
	return out


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


def gen_problems(problem_spec, max_num = None):
	"""
	Generate a series of multiplication problems.
	
	Takes a list [(num, num_digits, colour),...], where num_digits is a list of
	the format accepted by gen_mult_problem, num is the number of these such
	problems desired and colour is the colour to apply to this problem .
	
	Produces a corresponding list of (question,answer,colour) tuples.
	"""
	questions = []
	answers = []
	colours = []
	for num_problems, num_digits, colour in problem_spec:
		for _ in range(num_problems):
			q,a = None, None
			while q is None or q in questions or a in answers:
				q,a = gen_mult_problem(num_digits)
			questions.append(q)
			answers.append(a)
			colours.append(colour)
	
	return zip(questions,answers,colours)


if __name__=="__main__":
	size = 7
	num_questions = 3*((size**2-1)/8)
	pairs = gen_problems([ (num_questions/3,    (3,3), "red")
	                     , (num_questions/3,    (2,3), "blue")
	                     , ((num_questions+1)/3,(1,3), "green")
	                     ])
	puzzle = generate_puzzle(size, pairs)
	open("out.tex","w").write(puzzle_to_tikz(puzzle))
	
