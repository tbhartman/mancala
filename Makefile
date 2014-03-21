
all : mancala


mancala : mancala.f board.f
	gfortran -fimplicit-none -g $^ -o $@
