def dumb(roll, game_state):
    return next(iter(game_state.valid_choices(roll)))

def score(roll, game_state):
    choices = [
        c for c in game_state.valid_choices(roll)
    ]
    choices.sort(key=lambda c: game_state.score(c), reverse=True)
    return choices[0]

def even_5(roll, game_state):
    choices = [
        c for c in game_state.valid_choices(roll)
    ]
    def sort_key(c):
        if c[0] is None:
            f = -1000
        else:
            f = game_state.fifths.get(c[0], 0)
        s = game_state.score(c)
        return (f, s)
    choices.sort(key=sort_key)
    return choices[0]