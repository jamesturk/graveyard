import math
from collections import defaultdict
from rich.console import Console
from rich.table import Table

FULL_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class Wordform:
    def __init__(self, width):
        self.words = set()
        self.width = width
        self.matrix = [[set(FULL_ALPHABET) for _ in range(width)] for _ in range(width)]
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.num_transitions = 0

    def learn(self, *words):
        self.words.update(words)
        for word in words:
            for i, ch in enumerate(word):
                if last_ch := word[i - 1] if i > 0 else None:
                    self.transitions[last_ch][ch] += 1
                    self.num_transitions += 1

    def show(self):
        t = Table(show_header=False)
        for i in range(self.width):
            row = [str(len(self.matrix[i][j])) for j in range(self.width)]
            t.add_row(*row)
        return t

    def step(self):
        lowest_entropy = math.inf
        lowest_entropy_cells = []

        # find lowest entropy cells
        for i in range(self.width):
            for j in range(self.width):
                # already collapsed
                if len(self.matrix[i][j]) == 1:
                    continue
                entropy = len(self.matrix[i][j])
                if entropy < lowest_entropy:
                    lowest_entropy = entropy
                    lowest_entropy_cells = [(i, j)]
                elif entropy == lowest_entropy:
                    lowest_entropy_cells.append((i, j))

        # pick one
        i, j = random.choice(self.lowest_entropy_cells)

        # collapse
        self.matrix[i][j] = set(random.choice(list(self.matrix[i][j])))

        # propagate
        if i > 0:
            if j > 0:
                self.matrix[i - 1][j]

    def propagate_direction(self, i, j, transitions):
        if i < 0 or i >= self.width or j < 0 or j >= self.width:
            return
        


def main():
    wf = Wordform(5)
    wf.learn("ape", "apple", "abe", "ace", "age", "aid", "argo", "ark")
    print(wf.transitions)
    console = Console()
    console.print(wf.show())


if __name__ == "__main__":
    main()
