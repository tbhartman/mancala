      PROGRAM MANCALA
      integer board(15)
      integer validmove
      integer nextmove
      integer player
      validmove = 0
      player = board(15)
      call INITIALIZE_BOARD(board)
      call printboard(board)
      call MOVE(board,4,validmove)
      call printboard(board)
      call MOVE(board,3,validmove)
      call printboard(board)
      player = board(15)
      write(*,*)'Where to move?'
      read(*,10) nextmove
   10 format(i5)
      if (player.ne.0) then
          nextmove = nextmove + 7
      endif
      write(*,*) nextmove
      call MOVE(board,nextmove,validmove)
      call printboard(board)
      write(*,*) isgameover(board)
      END

