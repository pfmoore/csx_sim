from random import randint
from itertools import permutations
from statistics import mean, median, stdev
from dataclasses import dataclass, field
from collections import Counter
import copy

SCORES = {2: 100, 3: 70, 4: 60, 5: 50, 6: 40, 7: 30, 8: 40, 9: 50, 10: 60, 11: 70, 12: 100}

@dataclass(frozen=True)
class Turn:
    extra: int
    pairs: tuple[int, int]

@dataclass
class Game:
    turns: list[Turn] = field(default_factory=list)
    extras: Counter = field(default_factory=Counter)

    def add(self, turn: Turn):
        if turn.extra in self.extras or len(self.extras) < 3:
            self.extras[turn.extra] += 1
        self.turns.append(turn)

    def is_valid(self, turn: Turn):
        return (turn.extra in self.extras or len(self.extras) < 3)

    def is_finished(self):
        return any(n >= 8 for n in self.extras.values())

    def score(self):
        counts = Counter(n for t in self.turns for n in t.pairs)
        score = 0
        for n, count in counts.items():
            if count < 5:
                score -= 200
            elif count > 5:
                score += (count - 5) * SCORES[n]
        return score

    def turn_score(self, turn: Turn):
        g = Game(copy.copy(self.turns), copy.copy(self.extras))
        g.add(turn)
        return g.score() - self.score()

    def valid_choices(self, roll: set[Turn]):
        # If you have a free fifth die slot,
        # all choices are valid.
        if len(self.extras) < 3:
            return set(roll)
        # You must choose one of your selected fifth dice
        choices = {turn for turn in roll if self.is_valid(turn)}
        # If none of your fifth dice appeared, you get a
        # free die
        if not choices:
            return set(roll)
        return choices


def roll_5d6():
    dice = [randint(1,6) for _ in range(5)]
    return {Turn(extra=p[0], pairs=(p[1]+p[2], p[3]+p[4])) for p in permutations(dice)}

def simulate(game: Game, strategy):
    while not game.is_finished():
        choices = game.valid_choices(roll_5d6())
        choice = strategy(choices, game)
        game.add(choice)
    return game

def report(statname, stat):
    print(statname)
    print(f"    Mean: {mean(stat)}")
    print(f"    Median: {median(stat)}")
    print(f"    Min: {min(*stat)}")
    print(f"    Max: {max(*stat)}")
    print(f"    Std Deviation: {stdev(stat)}")

def main():
    from . import strategies
    strats = {
        "dumb": strategies.dumb,
        "score": strategies.score,
        "even_5": strategies.even_5,
        "central": strategies.score_central,
    }
    for name, strat in strats.items():
        turns = []
        scores = []
        for i in range(1000):
            g = Game()
            simulate(g, strat)
            turns.append(len(g.turns))
            scores.append(g.score())

        print(f"Strategy: {name}")
        print()
        report("Turns", turns)
        report("Score", scores)
        print("-"*30)
