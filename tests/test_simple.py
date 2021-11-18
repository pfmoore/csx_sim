from csx_sim import GameState
from itertools import permutations, combinations_with_replacement

def test_new():
    "The initial state of the game should score 0"
    g = GameState()
    assert g.current_score() == 0

def test_first_roll():
    "All possible first rolls should score -400"
    g = GameState()
    all_rolls = {
        (p[0], p[1]+p[2], p[3]+p[4])
        for dice in combinations_with_replacement(range(1,7), 5)
        for p in permutations(dice)
    }
    for x in all_rolls:
        assert g.score(x) == -400 if x[1] != x[2] else -200
