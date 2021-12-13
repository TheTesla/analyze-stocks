#!/usr/bin/env python3


import pickle

class Sim:
    def __init__(self):
        self.cash = 0
        self.stocks = {}
        self.ts = {}
        self.times = []
        self.subKey = 4
        self.t = 0

    def loadTS(self, ts):
        self.ts = ts
        self.times = list(ts.keys())
        self.times.sort()
        self.setTime()

    def incTime(self):
        self.setTime(self.t + 1)

    def setTime(self, t=0):
        self.t = t
        self.now = self.times[self.t]
        self.vals = self.ts[self.now]

    def buy(self, sym, amount):
        if sym not in self.stocks:
            self.stocks[sym] = 0
        self.stocks[sym] += amount
        self.cash -= self.getPrice(sym) * amount

    def sell(self, sym, amount):
        self.buy(sym, -amount)

    def getTotal(self):
        total = self.cash
        for sym, amount in self.stocks.items():
            total += self.getPrice(sym) * amount
        return total

    def getPosition(self, sym):
        amount = self.stocks[sym]
        value = self.getPrice(sym) * amount
        return (amount, value)

    def getPrice(self, sym):
        return float(self.vals[sym][self.subKey])

    def pp(self):
        print('{}:'.format(self.now))
        print('  TOTAL = {}'.format(self.getTotal()))
        print('  cash  = {}'.format(self.cash))
        for sym, amount in self.stocks.items():
            print('  {} = {} ({})'.format(sym, amount,
                self.getPrice(sym) * amount))


mySim = Sim()

with open("stockdata2.pickle", "rb") as f:
    ts = pickle.load(f)

mySim.loadTS(ts)

mySim.pp()

mySim.cash = 1000
mySim.buy('X', mySim.cash/mySim.getPrice('X'))
mySim.buy('Y', 0)
a = mySim.getPosition('X')[1]
b = mySim.getPosition('Y')[1]
m = (a + b)/2
mySim.buy('X', (m-a)/mySim.getPrice('X'))
mySim.buy('Y', (m-b)/mySim.getPrice('Y'))

mySim.pp()

for i in range(1000):
    a = mySim.getPosition('X')[1]
    b = mySim.getPosition('Y')[1]
    m = (a + b)/2
    if a/m > 1.2 or b/m > 1.2:
        mySim.buy('X', (m-a)/mySim.getPrice('X'))
        mySim.buy('Y', (m-b)/mySim.getPrice('Y'))
    mySim.pp()
    mySim.incTime()

mySim.pp()
