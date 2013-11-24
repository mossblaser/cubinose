#!/usr/bin/env python

import shapes, tile

@shapes.register
def triangle(width):
	r"""
	Generates a triangluar puzzle of a given width.
	
	Returns a dictionary {(x,y):Tile,...} for a set of tiles arranged like so:
	
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
	    width = 5
	"""
	assert width%2 == 1, \
		"Must be an odd width."
	
	tiles = {}
	
	# Generate a pyramid of triangular tiles
	for y in range(width):
		for x in range(width - 2*y):
			tiles[(x,y)] = tile.Tile()
	
	return tiles


