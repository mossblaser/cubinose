Cubinose
========

An "educational" tile-matching game generator. Produces a set of triangular
tiles whose edges contain either questions or answers to simple problems. Tiles
with matching question/answer pairs should be placed next to eachother in a
style similar to dominoes.

Usage
-----

	python . --shape SHAPE [SHAPE_ARGUMENT...] \
	         --problem PROBLEM [PROBLEM_ARGUMENT...] \
	                   [--prefix PREFIX] \
	                   [--proportion PROPORTION]

Produces (on stdout) a LaTeX file containing the puzzle. To see a list of
shapes and problems, run `python . -h`.

An example with two difficulties of multiplication question, 25% easy, 75%
harder:

	python . --shape triangle 5 \
	         --problem multidigit_multiplication '(1, 1)' \
	                   --prefix "blue" \
	                   --proportion 25 \
	         --problem multidigit_multiplication '(2, 2)' \
	                   --prefix "red" \
	                   --proportion 75

Useful Formulae
---------------

When the puzzle is shaped like a large triangle, e.g.:

	        /\
	       /  \
	      /____\
	     /\    /\
	    /  \  /  \
	   /____\/____\
	  /\    /\    /\
	 /  \  /  \  /  \
	/____\/____\/____\

The size of the puzzle, $n$, is defined to be the number of triangles on the
bottom row of the triangle. In the example above, $n = 5$.

The number of tiles will be $\frac{(n+1)^2}{4}$.

The number of question-answer pairs required is $3\frac{n^2 - 1}{8}$.

The largest triangle which can be made with at most $q$ questions is
$\Big\lfloor \sqrt{\frac{8q}{3} + 1} \Big\rfloor$.
