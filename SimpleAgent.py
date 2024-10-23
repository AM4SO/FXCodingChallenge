import FXapi
import time

class SimpleAgent:
    knowledge = {"BrexitTime": 0}
    startWorth = None 

    def getWorth():
        FXapi.getNormalisedCapitals()

    def __init__(self):
        self.startWorth = self.getWorth()

    def loop():
        FXapi.trade2(1, FXapi.SIDE_BUY)