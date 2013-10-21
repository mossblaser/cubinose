Cubinose
========

An "educational" tile-matching game generator. Produces a set of triangular
tiles whose edges contain either questions or answers to simple problems. Tiles
with matching question/answer pairs should be placed next to eachother in a
style similar to dominoes.

Usage:
------

Note: Currently proof of concept only! Generates puzzles with simple
integer multiplication problems.

* Run `python gen_puzzle.py` specifying the size of the puzzle at the end of
  `gen_puzzle.py`.
* The program produces `out.tex` containing a TikZ representation of the puzzle
* Compile the generated LaTeX source with `pdflatex out.tex`
* Output is in `out.pdf`

An example output looks something like this:

![Cubinose Example Output](http://jhnet.co.uk/misc/cubinose.png)

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
