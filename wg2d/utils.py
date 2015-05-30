import random


def weighted_choice(options):
    r = random.random()
    total = 0
    for choice, weight in options.items():
        if total + weight >= r:
            return choice
        total += weight
