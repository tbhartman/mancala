
all : mancala


mancala : mancala.f board.f
	gfortran -g $^ -o $@
