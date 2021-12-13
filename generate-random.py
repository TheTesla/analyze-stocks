#!/usr/bin/env python3


import random


r = [1/1.1 if random.randrange(0,2) else 1.1 for e in range(10000)]

tsv = []


v = 100


for e in r:
    v *= e
    tsv.append(v)


ts = {'{:09}'.format(i): {'X': ['{}'.format(x)] * 5 + [0,1], 'Y': ['100']*5 +[0,1]} for i, x in enumerate(tsv)}


with open("stockdata2.pickle", "wb") as f:
    pickle.dump(ts, f)

