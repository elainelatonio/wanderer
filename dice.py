import random

class Dice:
    @staticmethod
    def roll():
        d6 = random.randint(1, 6)
        return d6
