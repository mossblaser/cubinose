#!/usr/bin/env python

import random

"""
Datastructures and constants for a set of tiles.
"""

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
	
	
	def add_edge(self, side, label):
		"""
		Set the label of an edge of the tile.
		
		Note: It is the responsibility of the caller to sensibly choose which edges
		are labelled. That is, the tile doesn't know its orientation and so doesn't
		know if it is sensible to have a top or bottom side.
		"""
		assert(side not in self.edges)
		assert(len(self.edges) < 3)
		assert(not (side in (TOP_EDGE,BOTTOM_EDGE) and opposite(side) in self.edges))
		self.edges[side] = label


def iter_touching_edges(tiles):
	"""
	Iterate over pairs of touching edges returning a list of ((tile,side),
	(tile,side)) tuples.
	"""
	for (x,y) in tiles.iterkeys():
		for side, pos in [ (RIGHT_EDGE, (x+1, y))
		                 , (TOP_EDGE, (x-1, y+1))
		                 ]:
			if pos in tiles and not (side == TOP_EDGE and x%2 == 0):
				yield ( (tiles[(x,y)], side)
				      , (tiles[pos], opposite(side))
				      )


def add_questions(tiles, problem_generator):
	"""
	Takes a dictionary {(x,y): tile, ...} and an iterator problem_generator and
	populates the edge of the tiles with random question and answer paris.
	"""
	# Generate a list of random problems
	num_problems = len(list(iter_touching_edges(tiles)))
	problems = [problem_generator.next() for _ in range(num_problems)]
	random.shuffle(problems)
	
	# Put the problems on edges of the tiles
	for touching_edge, (q,a) in zip(iter_touching_edges(tiles), problems):
		# Put the question/answer part on random edges
		touching_edge = list(touching_edge)
		random.shuffle(touching_edge)
		
		touching_edge[0][0].add_edge(touching_edge[0][1], q)
		touching_edge[1][0].add_edge(touching_edge[1][1], a)


def to_tikz(tiles):
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
		
		# Determine the label for each tile
		tb_l = tile.edges.get(top_or_btm, "{}")
		l_l  = tile.edges.get(LEFT_EDGE, "{}")
		r_l  = tile.edges.get(RIGHT_EDGE, "{}")
		
		# Produce the relevent \tri command
		out += "\\tri{%d,%d}{tile %d %d}{%s}{%s}{%s}{%s};\n"%(
			pos[1] + pos[0], pos[1],
			pos[0], pos[1],
			"up" if pos[0]%2 == 0 else "down",
			tb_l,
			l_l,
			r_l,
		)
	
	out += r"""
			\end{tikzpicture}
		\end{document}
	"""
	
	return out
