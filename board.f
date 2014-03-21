      SUBROUTINE INITIALIZE_BOARD(board)
      integer,intent(out) :: board(15)
      board(1:6) = 4
      board(8:13) = 4
      board(7) = 0
      board(14) = 0
      board(15) = 0
      RETURN
      END
      
      integer function isvalidmove(board,spot)
      integer board(15)
      integer player
      integer spot
      integer rocks
      
      player = board(15)
      rocks = board(spot)

      if (player .eq. 0) then
          if (((spot.lt.1).or.(spot.gt.6)).or.(rocks.le.0)) then
              isvalidmove = 0
          else
              isvalidmove = 1
          endif
      else
          if (((spot.lt.8).or.(spot.gt.13)).or.(rocks.le.0)) then
              isvalidmove = 0
          else
              isvalidmove = 1
          endif
      endif
      return
      end
      
c     board array:
c     
c     player: 15
c     [ 14 |  8  9 10 11 12 13 |    ]
c     [    |  6  5  4  3  2  1 |  7 ]
      SUBROUTINE MOVE(board,spot,valid)
      integer,intent(inout) :: board(15)
      integer,intent(in) :: spot
      integer,intent(out) :: valid
      integer player
      integer rocks
      integer counter
      integer next
      
      player = board(15)
      next = spot
      valid = 0

      valid = isvalidmove(board,spot)
      if (valid.ne.0) then
          rocks = board(spot)
          do counter = 1,rocks,1
              next = NEXTSPOT(next,player) + 0
              board(next) = board(next) + 1
          enddo
          board(spot) = 0
          if (next.ne.7 .and. next.ne.14) then
              if (player.eq.0) then
                  player = 1
              else
                  player = 0
              endif
          endif
      endif
      board(15) = player
      RETURN

      END
      integer function isgameover(board)
      integer board(15)
      integer total
      total = board(1) + 
     *        board(2) +
     *        board(3) +
     *        board(4) +
     *        board(5) +
     *        board(6) +
     *        board(7) +
     *        board(9) +
     *        board(10) +
     *        board(11) +
     *        board(12) +
     *        board(13)
      if (total.ne.0) then
          isgameover = 0
      else
          isgameover = 1
      endif
      return
      end

      integer function NEXTSPOT(spot,player)
      integer spot
      integer player
      NEXTSPOT = 0
      if (spot.eq.8 .and. player.ne.0) then
          NEXTSPOT = 14
      elseif (spot.eq.8 .and. player.eq.0) then
          NEXTSPOT = 6
      elseif (spot.eq.1 .and. player.ne.0) then
          NEXTSPOT = 13
      elseif (spot.eq.1 .and. player.eq.0) then
          NEXTSPOT = 7
      elseif (spot.ge.2 .and. spot.le.6) then
          NEXTSPOT = spot - 1
      elseif (spot.ge.9 .and. spot.le.13) then
          NEXTSPOT = spot - 1
      elseif (spot.eq.7) then
          NEXTSPOT = 13
      elseif (spot.eq.14) then
          NEXTSPOT = 6
      endif
      return
      end

      SUBROUTINE PRINTBOARD(board)
      integer,intent(in) ::  board(15)
  100 FORMAT ('Player: ',i1)
  101 FORMAT ('[ ',i2,' | ',i3,i3,i3,i3,i3,i3,' |    ]')
  102 FORMAT ('[    | ',i3,i3,i3,i3,i3,i3,' | ',i2,' ]')
      write(*,100) board(15)
      write(*,101) board(14),
     1             board(8),
     1             board(9),
     1             board(10),
     1             board(11),
     1             board(12),
     1             board(13)
      write(*,102) board(6),
     1             board(5),
     1             board(4),
     1             board(3),
     1             board(2),
     1             board(1),
     1             board(7)
      END
