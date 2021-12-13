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

with open("stockdata.pickle", "rb") as f:
    ts = pickle.load(f)

#mySim.loadTS(qryData(['LSCC', 'XLNX'], 'TIME_SERIES_DAILY_ADJUSTED', 'full'))
mySim.loadTS(ts)

mySim.pp()

mySim.cash = 1000
mySim.buy('XLNX', mySim.cash/mySim.getPrice('XLNX'))
mySim.buy('MSFT', 0)
mySim.buy('NVDA', 0)
mySim.buy('AMD', 0)
mySim.buy('LSCC', 0)
a = mySim.getPosition('MSFT')[1]
b = mySim.getPosition('XLNX')[1]
c = mySim.getPosition('NVDA')[1]
d = mySim.getPosition('AMD')[1]
e = mySim.getPosition('LSCC')[1]
m = (a + b + c + d + e)/5
mySim.buy('MSFT', (m-a)/mySim.getPrice('MSFT'))
mySim.buy('XLNX', (m-b)/mySim.getPrice('XLNX'))
mySim.buy('NVDA', (m-c)/mySim.getPrice('NVDA'))
mySim.buy('AMD', (m-d)/mySim.getPrice('AMD'))
mySim.buy('LSCC', (m-e)/mySim.getPrice('LSCC'))

mySim.pp()

for i in range(5500):
    a = mySim.getPosition('MSFT')[1]
    b = mySim.getPosition('XLNX')[1]
    c = mySim.getPosition('NVDA')[1]
    d = mySim.getPosition('AMD')[1]
    e = mySim.getPosition('LSCC')[1]
    m = (a + b + c + d + e)/5
    if a/m > 20 or b/m > 20 or c/m > 20 or d/m > 20 or e/m > 20:
        mySim.buy('MSFT', (m-a)/mySim.getPrice('MSFT'))
        mySim.buy('XLNX', (m-b)/mySim.getPrice('XLNX'))
        mySim.buy('NVDA', (m-c)/mySim.getPrice('NVDA'))
        mySim.buy('AMD', (m-d)/mySim.getPrice('AMD'))
        mySim.buy('LSCC', (m-e)/mySim.getPrice('LSCC'))
    mySim.pp()
    mySim.incTime()

mySim.pp()
