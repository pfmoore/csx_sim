from . import Game, Turn

def dumb(choices: set[Turn], game: Game):
    return next(iter(choices))

def score(choices: set[Turn], game: Game):
    return sorted(choices, key=lambda c: game.turn_score(c), reverse=True)[0]

def even_5(choices: set[Turn], game: Game):
    def sort_key(turn: Turn):
        if len(game.extras) >= 3 and turn.extra not in game.extras:
            f = -1000
        else:
            f = game.extras[turn.extra]
        s = game.turn_score(turn)
        return (f, -s)
    return sorted(choices, key=sort_key)[0]

def score_central(choices: set[Turn], game: Game):
    def weight(n):
        return abs(n-7)
    def sort_key(turn: Turn):
        score = game.turn_score(turn)
        w = sum(weight(n) for n in turn.pairs)
        return (score, -w)
    return sorted(choices, key=sort_key)[0]
