import numpy as np

class Ride:
    def __init__(self,ID,requestTime):
        self.rideID = ID
        self.requestTime = requestTime
        self.pickupTime = np.nan
        self.dropoffTime = np.nan

    def random(self,network):
        self.origin = network.randomNode()
        while True:
            self.destination = network.randomNode()
            if self.destination != self.origin: break
        
        self.shortestTime = network.pathDuration[self.origin][self.destination]

    def pickupDelay(self):
        return self.pickupTime - self.requestTime

    def travelDelay(self):
        return self.dropoffTime - self.pickupTime - self.shortestTime

    def totalDelay(self):
        return self.pickupDelay() + self.travelDelay()
