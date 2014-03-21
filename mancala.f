      PROGRAM MANCALA
      integer board(15)
      integer validmove
      integer nextmove
      integer player
      validmove = 0
      player = board(15)
      call INITIALIZE_BOARD(board)
      call printboard(board)
  100 continue
      player = board(15)
      write(*,*)'Where to move?'
      read(*,10) nextmove
   10 format(i5)
      if (player.ne.0) then
          nextmove = nextmove + 7
      endif
      call MOVE(board,nextmove,validmove)
      if (validmove.eq.0) then
          write(*,*) 'Invalid move!'
          goto 100
      endif
      call printboard(board)
      if (isgameover(board).ne.0) then
          write(*,*) 'Game over!'
          goto 200
      endif
      goto 100
  200 continue
      END

