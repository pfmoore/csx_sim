from . import strategies
from random import randint
from itertools import permutations
from statistics import mean, median, stdev

# Choice: (fifth, n1, n2)
# Roll: {Choices}
# GameState: current position on board
#   points (a "point" is one of the numbers 2-12, need a better name)
#   fifths (a "fifth" is an extra die, need a better name)
# gs.score(choice)
# gs.current_score()
# gs.valid(choice)
# gs.finished()

def roll_5d6():
    dice = [randint(1,6) for _ in range(5)]
    return {(p[0], p[1]+p[2], p[3]+p[4]) for p in permutations(dice)}

class GameState:
    def __init__(self):
        self.points = [0] * 11
        self.scores = [100,70,60,50,40,30,40,50,60,70,100]
        self.fifths = {}
        self.choices = []
    def current_score(self):
        total = 0
        for point in range(2, 13):
            n = self.points[point-2]
            if n == 0:
                continue
            if n < 5:
                total -= 200
            elif n > 5:
                total += (n-5)*self.scores[point-2]
        return total
    def valid_choices(self, roll):
        # If you have a free fifth die slot,
        # all choices are valid.
        if len(self.fifths) < 3:
            return roll
        # You must choose one of your selected fifth dice
        choices = {
            c for c in roll
            if c[0] in self.fifths
        }
        # If none of your fifth dice appeared, you get a
        # free die
        if not choices:
            choices = {(None, n1, n2) for (_, n1, n2) in roll}
        return choices
    def add(self, choice):
        self.choices.append(choice)
        fifth, n1, n2 = choice
        if fifth is None:
            # None is a free die
            pass
        elif fifth in self.fifths:
            self.fifths[fifth] += 1
        else:
            self.fifths[fifth] = 1
        self.points[n1-2] += 1
        self.points[n2-2] += 1
    def finished(self):
        return (len(self.fifths) == 3 and any(v == 8 for v in self.fifths.values()))
    def score(self, choice):
        _, n1, n2 = choice
        score = 0
        for point in (n1, n2):
            n = self.points[point-2]
            if n == 0:
                score -= 200
            elif n == 4:
                score += 200
            elif n > 4:
                score += self.scores[point-2]
        return score

def simulate(game_state, strategy):
    while not game_state.finished():
        roll = roll_5d6()
        choice = strategy(roll, game_state)
        game_state.add(choice)
    return game_state

def main():
    strats = {
        "dumb": strategies.dumb,
        "score": strategies.score,
        "even_5": strategies.even_5,
    }
    for name, strat in strats.items():
        turns = []
        scores = []
        for i in range(1000):
            g = GameState()
            simulate(g, strat)
            turns.append(len(g.choices))
            scores.append(g.current_score())
        print(name)
        print(f"Turns: avg={mean(turns)}, median={median(turns)}, std_dev={stdev(turns)}")
        print(f"Turns: avg={mean(scores)}, median={median(scores)}, std_dev={stdev(scores)}")
