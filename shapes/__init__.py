#!/usr/bin/env python

"""
Functions which produce arrangements of tiles in fun forms.
"""


"""
A dictionary of {names:shapes_func,...} defined in the package. Functions should
be added using the add decorator below.
"""
shapes = {}

def register(f):
	"""
	A decorator which registers a function as a shape function.
	"""
	shapes[f.__name__] = f
	return f




# Import all the shape modules
import os
for module in os.listdir(os.path.dirname(__file__)):
	if module != '__init__.py' and module[-3:] == '.py':
		__import__(module[:-3], locals(), globals())
del module
