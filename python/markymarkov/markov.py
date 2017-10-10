from __future__ import division
import re
import random
from collections import defaultdict, namedtuple

Item = namedtuple('Item', ['word', 'source'])


class MarkovBrain(object):

    def __init__(self):
        self.table = defaultdict(list)

    def learn(self, text, source=None):
        prevprev = None
        prev = None
        text = re.sub(r'[\?\.\!\(\)\,]', ' ', text)
        for word in text.split():
            self.table[(prevprev, prev)].append(Item(word, source))
            prevprev = prev
            prev = word

    def generate(self, num_sentences=10):
        sources = set()

        prevprev, prev = random.choice(self.table.keys())

        sentence_lengths = [1,3,4,5,5,6,6,7,7,8,8,9,9,
                            10,10,10,11,11,11,11,12,12,12,12,13,13,13,
                            14,14,14,15,15,15,16,16,16,17,17,17,18,18,
                            19,19,20,20,21,22,23,24]
        sentence = []
        cur_sen_length = random.choice(sentence_lengths)
        sentences = []

        while len(sentences) < num_sentences:
            choices = self.table[(prevprev, prev)]
            # end a sentence if we hit a dead end or our time is up
            if not choices or len(sentence) > cur_sen_length:
                sentence = ' '.join(sentence) + random.choice('.....!?')
                if sentence.count('"') % 2 == 1:
                    sentence += '"'
                # clean up sentence a bit
                sentence = sentence.strip(',').capitalize()
                sentences.append(sentence)
                sentence = []
                cur_sen_length = random.choice(sentence_lengths)
                ppp, choices = random.choice(self.table.items())
                prevprev, prev = ppp

            # pull a new item out of the choices
            item = random.choice(choices)
            word = item.word
            if random.random() < 0.1:
                word += ','
            sentence.append(word)
            sources.add(item.source)
            prevprev = prev
            prev = item.word

        return '\n'.join(sentences), sources


def test():
    b = MarkovBrain()
    b.learn('this is a good story', 'one')
    b.learn('a good story is always long', 'two')
    b.learn('this is not a good time', 'three')
    b.learn('for a good time call martha', 'four')
    b.learn('a cake is not always tasty', 'five')
    return b
