import time

#This is what your basic strategy will look like
class Strategy:
    def __init__(self, strategyNum, coin):
        self._running = True
        self.strategyNumber = strategyNum
        self.coin = coin

    def terminate(self):
        self._running = False
    
    def run(self):
        print("Running")
        while self._running:
            time.sleep(1)
            print(self.coin)

    def status(self):
        return "status is good"




#Algorithm Handler Example
#Make Sure to start in a TRY incase there strategy is bad
#All algos are stored in a list
#algorithms = []
#algorithms.append(Strategy(1, "ETH"))
#algorithms.append(Strategy(2, "BTC"))
#algorithms.append(Strategy(3, "BTC"))

#for algo in algorithms:
#    print("Starting Thread: " + str(algo.strategyNumber))
#    print(algo.status())
#    t = Thread(target= algo.run)
#    t.start()

#time.sleep(10)

#for x in algorithms:
#    x.terminate()