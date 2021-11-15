from csx_sim import Game, Turn
from itertools import permutations, combinations_with_replacement

def test_new():
    "The initial state of the game should score 0"
    g = Game()
    assert g.score() == 0

def test_first_roll():
    "All possible first rolls should score -200 or -400"
    g = Game()
    all_rolls = {
        Turn(p[0], (p[1]+p[2], p[3]+p[4]))
        for dice in combinations_with_replacement(range(1,7), 5)
        for p in permutations(dice)
    }
    for x in all_rolls:
        assert g.turn_score(x) == (-200 if x.pairs[0] == x.pairs[1] else -400)
