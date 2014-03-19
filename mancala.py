# mancala simulation
class InvalidMove(Exception):pass
class GameOver(Exception): pass
class Board(object):
    def __init__(self):
        self.reset()
         
    def get_pocket(self,spot):
        return self._pocket[spot]
    def _change_player(self):
        if self._current_player == 0:
            self._current_player = 1
        else:
            self._current_player = 0
    def print_status(self):
        print(self)
        print('Current player: {:d}'.format(self._current_player))
        print('Total moves: {:d}'.format(self._total_moves))
    def opposite(self,spot):
        d = {6:11,
             11:6,
             5:12,
             12:5,
             4:13,
             13:4,
             3:14,
             14:3,
             2:15,
             15:2,
             1:16,
             16:1}
        return self.get_pocket(d[spot])
    def play_multiple(self,spots):
        for i in spots:
            self.play(i)
        if self._verbose:
            self.print_status()
    def undo(self):
        moves = list(self._moves)
        moves.pop()
        self.reset()
        self.play_multiple(moves)
    def reset(self):
        self._pocket = {i:Pocket() for i in [1,2,3,4,5,6,11,12,13,14,15,16]}
        self._pocket[0] = Mancala()
        self._pocket[10] = Mancala()
        self._verbose = True
        self._current_player = 0
        self._total_moves = 0
        self._moves = []
        self._gameover = False
        self._saved = False

    def play(self,spot):
        """[ 10 | 11 12 13 14 15 16 |    ]
           [    | 06 05 04 03 02 01 | 00 ]
        """
        if self._gameover:
            raise GameOver()
        if not (( spot < 7 and spot > 0 ) or ( spot > 10 and spot < 17 )):
            raise InvalidMove()
        if not (spot - (spot % 10))/10 == self._current_player:
            raise InvalidMove()
        pocket = self.get_pocket(spot)
        if pocket.num_rocks <= 0:
            raise InvalidMove()
        self._moves.append(spot)
        for i in self.iter_moves(spot,pocket.num_rocks):
            self.get_pocket(i).append(pocket.pop())
        if not (i == 10 or i == 0):
            if (self.get_pocket(i).num_rocks == 1 and
                    ((self._current_player == 0 and i < 10) or
                     (self._current_player == 1 and i > 10))):
                self.get_pocket(self._current_player * 10).extend(self.opposite(i).empty())
                self.get_pocket(self._current_player * 10).extend(self.get_pocket(i).empty())
            self._change_player()
        if (sum([self.get_pocket(i).num_rocks for i in range(11,17)]) == 0 or 
                sum([self.get_pocket(i).num_rocks for i in range(1,7)]) == 0 ):
            self._gameover = True
            for i in range(11,17):
                self.get_pocket(10).extend(self.get_pocket(i).empty())
            for i in range(7):
                self.get_pocket(0).extend(self.get_pocket(i).empty())
            self.save()


        self._total_moves += 1
        if self._verbose:
            self.print_status()
    def encode(self):
        ret = ''.join(map('{:02d}'.format,self._moves))
        ret = ret + ';' + ''.join(['{:02d}'.format(self.get_pocket(i).num_rocks) for i in [0,10]])
        return ret
    def save(self):
        if self._saved:
            return
        if not self._gameover:
            raise Exception()
        try:
            filename = __file__
        except NameError:
            import sys
            filename = sys.argv[0]
        try:
            with open(filename,'r') as f:
                if not f.readline().strip() == "# mancala simulation":
                    raise Exception()
        except IOError:
            pass
        except Exception:
            pass
        else:
            with open(filename,'ab') as f:
                f.write(("results.add('" + self.encode() + "')\n").replace('\r',''))
            self._saved = True




            

    
    @classmethod
    def iter_moves(cls,spot,number):
        original_spot = spot
        for i in range(number):
            spot -= 1
            if original_spot >= 10:
                if spot == 0:
                    spot = 16
                elif spot == 9:
                    spot = 06
            elif original_spot < 10:
                if spot == 10:
                    spot = 06
                elif spot < 0:
                    spot = 16
            yield spot

    def __repr__(self):
        fmt = ' '.join(['{:>2s}']*6)
        row_one = ('[ ' + '{:>2s} | '.format(self._pocket[10])
                   + fmt.format(*[self._pocket[i] for i in range(11,17)]) + ' |    ]')
        row_two = ('[    | ' + fmt.format(*[self._pocket[i] for i in range(6,0,-1)])
                   + ' | {:>2s}'.format(self._pocket[0]) + ' ]')
        return '\n'.join([row_one,row_two])
    

class Pocket(object):
    def __init__(self):
        self._rocks = []
        self.refill()
        self.append = self._rocks.append
        self.pop = self._rocks.pop
        self.extend = self._rocks.extend
    @property
    def num_rocks(self):
        return len(self._rocks)
    def is_empty(self):
        return self.num_rocks == 0
    def __repr__(self):
        return str(self.num_rocks)
    def refill(self):
        self._rocks = [Rock()] * 4
    def __iadd__(self,rock):
        self._rocks.append(rock)
    def empty(self):
        return [self._rocks.pop() for i in range(self.num_rocks)]



class Rock(object):
    pass

class Mancala(Pocket):
    def __init__(self):
        Pocket.__init__(self)
        self.empty()


class Player(object):
    pass

b = Board()

b.print_status()

results = set()
results.add('02151205021101111202150513061205110614051112031301041113010201031606;2424')
results.add('0401151106130414061106120611;4107')
results.add('0401151605140411031401160415051301051604111204160511;2424')
results.add('031101151116140213010412051601160216031602141301160612160102110215010211120513040214011603150102;2523')
results.add('03110112021504110116031112111302031112041406120105140103020412031601;1830')
results.add('05110416051204111405120611051506120514011502140314011602;1929')
results.add('06160504150616011403140411041302120511041606130115021403120102;2424')
results.add('031101140213041201160312020104130314061301021403;2424')
results.add('04011103140104111204130411061402121113031401;1929')
results.add('051106120515061601150214041305140116061405110412041115111205140413021201031112020313041601;1929')
results.add('021415130113061403150201130416021503140113051604150211051201140213031506140511;2622')
results.add('0616050415061601140415051606;2226')
results.add('061205110113061205110615120212031201131502;1632')
results.add('06110112021306120311011602120511021506160305131106;3810')
results.add('0211061201161106130614041206150412031601160515021306160311020103120614061205160313010414010215;2226')
