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
        #print("Running")
        while self._running:
            time.sleep(1)
            #print(self.coin)

    def status(self):
        return "status is good"