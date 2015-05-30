from .utils import weighted_choice
from collections import Counter

def test_weighted_choice():
    choices = {'A': 0.8, 'B': 0.1, 'C': 0.09, 'D': 0.01}
    ctr = Counter()

    for _ in range(10000):
        ctr[weighted_choice(choices)] += 1

    assert 7800 < ctr['A'] < 8200   # ~200
    assert 900 < ctr['B'] < 1100    # ~100
    assert 800 < ctr['C'] < 1000    # ~100
    assert 50 < ctr['D'] < 150      # ~50
