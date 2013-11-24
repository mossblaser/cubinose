#!/usr/bin/env python

"""
Fraction interpretation problems.
"""

import random

import problems

def gen_fraction( whole_min, whole_max
                , denomenator_min, denomenator_max
                ):
	"""
	Generate a fraction in the form (whole, numerator, denomenator).
	"""
	
	denomenator = random.randint(denomenator_min, denomenator_max)
	return ( random.randint(whole_min, whole_max)
	       , random.randint(1, denomenator)
	       , denomenator
	       )


def format_fraction(fraction, format_name):
	r"""
	Format a fraction in one of the following styles:
	
	mixed: a mixed-number fraction, e.g. $1\frac{2}{3}$
	impropper: an impropper fraction, e.g. $\frac{3}{2}$
	pie: as a series of pie-charts
	"""
	if format_name == "mixed":
		if fraction[0] == 0:
			return r"$\frac{%d}{%d}$"%(fraction[1], fraction[2])
		else:
			return r"$%d\frac{%d}{%d}$"%(fraction[0], fraction[1], fraction[2])
	elif format_name == "impropper":
		return r"$\frac{%d}{%d}$"%(fraction[1] + (fraction[2]*fraction[0]), fraction[2])
	elif format_name == "pie":
		out = r"\begin{tikzpicture}[scale=0.3,thick]"
		# Command which draws a wedge
		#  #1: Offset
		#  #2: Number of slices
		#  #3: Slice number
		#  #4: Style
		out += r"  \newcommand{\wdge}[4]{"
		out += r"    \begin{scope}[shift={#1}]"
		out += r"      \pgfmathsetmacro{\wangle}{360.0 / #2}"
		out += r"      \pgfmathsetmacro{\wstart}{\wangle * #3}"
		out += r"      \pgfmathsetmacro{\wend}{\wangle * (#3+1)}"
		out += r"      \draw [fill opacity=0.5, #4]"
		out += r"            (0,0)"
		out += r"         -- (\wstart:0.5)"
		out += r"        arc (\wstart:\wend:0.5)"
		out += r"         -- cycle;"
		out += r"    \end{scope}"
		out += r"  }"
		for whole in range(fraction[0]):
			for wedge in range(fraction[2]):
				out += r"  \wdge{(%f*1.2,0)}{%d}{%d}{fill}"%(
					whole, fraction[2], wedge
				)
		for wedge in range(fraction[2]):
			out += r"  \wdge{(%f*1.2,0)}{%d}{%d}{%s}"%(
				fraction[0], fraction[2], wedge,
				"fill" if wedge < fraction[1] else ""
			)
		out += r"\end{tikzpicture}"
		return out
	else:
		raise Exception("Unrecognised fraction format '%s'"%format_name)


@problems.register
def fraction_conversion( whole_min, whole_max
                       , denomenator_min, denomenator_max
                       , format_q
                       , format_a
                       ):
	r"""
	Generate question and answer pairs of fractions displayed in two formats.
	Fraction possibilities given as whole_min, whole_max, denomenator_min and
	denomenator_max.
	
	Formats are:
	
	mixed: a mixed-number fraction, e.g. $1\frac{2}{3}$
	impropper: an impropper fraction, e.g. $\frac{3}{2}$
	pie: as a series of pie-charts
	"""
	
	while True:
		fraction = gen_fraction(whole_min, whole_max
		                       , denomenator_min, denomenator_max
		                       )
		yield ( format_fraction(fraction, format_q)
		      , format_fraction(fraction, format_a)
		      )

