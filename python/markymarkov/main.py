import os
import glob

from markov import MarkovBrain
from download import scrape_stories

brain = MarkovBrain()

def learn_something(url, cache_dir):
    #scrape_stories(url, cache_dir)

    for fname in glob.glob(cache_dir + '/*'):
        with open(fname) as f:
            brain.learn(f.read(), fname)

#learn_something('http://www.fanfiction.net/game/Sonic-the-Hedgehog/14/0/0/1/0/0/0/0/0/1/0/', 'cache/sonic')
learn_something('http://www.fanfiction.net/book/Lord-of-the-Rings/14/0/0/1/0/0/0/0/0/1/0/', 'cache/animorphs')
