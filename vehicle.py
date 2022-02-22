from numpy.random import choice
import numpy as np

def sign(x):
    return 1 if x > 0 else -1

class Vehicle:
    def __init__(self,ID,capacity = 3):
        self.ID = ID
        
        # number of seats; updated at pickup and dropoff
        self.numSeats = capacity

        # keys are rideIDs
        self.rides = {}

        # waypoints is a list of rideIDs in order of pickup and
        # dropoff, if a rideID is negative, it's a dropoff
        # if waypoints is empty the vehicle is at rest
        self.waypoints = []

        # next node to be reached on the route to the proximal
        # waypoint or the node at which the vehicle is idling
        self.nextNode = None
        self.nextTime = None

    def placeAtRandom(self,network):
        # location will be used if the vehicle is idle and has no
        # current route 
        self.nextNode = network.randomNode()

    def isIdle(self):
        return self.nextTime is None

    def nextWaypointNode(self,waypoint):
        # given a waypoint which is a positive or negarive rideID
        # return the nodeID of ride's origin or destination
        if waypoint < 0:
            return self.rides[-waypoint].destination
        else:
            return self.rides[waypoint].origin

    def addRide(self,ride,waypoints):
        # save the ride and update waypoints
        self.rides[ride.rideID] = ride
        self.waypoints = waypoints

    def calcTotalDelay(self,waypoints,network):
        # the time and node at which the calculation starts
        if self.isIdle():
            # return empty dict if the passed waypoints list is empty
            if not waypoints: return {}
            
            # the first waypoint is guaranteed to be a pickup if
            # vehicle is idle
            time = self.rides[abs(waypoints[0])].requestTime
        else:
            time = self.nextTime
        node = self.nextNode

        # sanity check
        if set(abs(w) for w in waypoints) != set(self.rides):
            print('The self.rides and passed waypoints do not match')

        for rideID in waypoints:
            ride = self.rides[abs(rideID)]

            # update the pick up dropoff time
            if rideID > 0: # pickup
                # time from current location to pickup loc
                time += network.pathDuration[node][ride.origin]
                node = ride.origin
                # set the pickup time
                ride.pickupTime = time

            else: # dropoff
                time += network.pathDuration[node][ride.destination]
                node = ride.destination
                ride.dropoffTime = time

        # return the total delay
        # return sum(r.totalDelay() for r in self.rides.values())

        # return inividual ride delays
        return dict((ID,r.totalDelay()) for ID,r in self.rides.items())
        
    def delayDeltaAddedRide(self,extraRide,network,selfish):
        # try adding the extraRide pickup and dropoff among the
        # existing waypoints and compute the sum of delay for
        # every ride of this vehicle including extraRide

        # recompute the current delay
        currentDelay = self.calcTotalDelay(self.waypoints,network)
        
        # the time at this moment is the extraRide request time
        self.rides[extraRide.rideID] = extraRide
        
        numIntervals = len(self.waypoints) + 1
        bestDelay = None
        bestWaypoints = []
        for firstInterval in range(numIntervals):
            for secondInterval in range(firstInterval,numIntervals):
                trialWaypoints = self.waypoints.copy()
                trialWaypoints.insert(firstInterval,extraRide.rideID)
                trialWaypoints.insert(secondInterval + 1,-extraRide.rideID)

                # check that the this sequence of pickups and dropoffs
                # does not violate total capacity constraint
                if self.overloaded(trialWaypoints): continue
                
                delay = self.calcTotalDelay(trialWaypoints,network)

                # reject this waypoint order if any existing ride's
                # delay increased if selfish flag is set:
                if selfish:
                    for rideID,oldDelay in currentDelay.items():
                        if delay[rideID] > oldDelay:
                            continue

                # if the delay is shorter than bestDelay (or bestDelay
                # is None) save it
                totDelay = sum(delay.values())
                if bestDelay is None or totDelay < bestDelay:
                    bestDelay = totDelay
                    bestWaypoints = trialWaypoints

        # sanity check, bestDelay cannot still be None
        if bestDelay is None:
            print('Could not add ride')
            return np.nan,[]

        # pop the extra ride
        self.rides.pop(extraRide.rideID)
        
        # return the increase in the total delay if extraRide is added
        # and the waypoint order which minimizes this delay
        return bestDelay - sum(currentDelay.values()),bestWaypoints

    def overloaded(self,waypoints):
        numSeats = self.numSeats
        for waypoint in waypoints:
            numSeats -= sign(waypoint)
            if numSeats < 0: return True

        return False

    def processNodeArrival(self,currentTime,network):
        # arrived at self.nextNode
        currentNode = self.nextNode
        
        # keys are rideIDs, values are 2-tuples of pickup delay and
        # travel delay
        performance = {}

        # process pickups and dropoffs at this node if any
        while True:
            if not self.waypoints: break
            waypoint = self.waypoints[0]
            ride = self.rides[abs(waypoint)]

            # if it's a pickup, record the pickup time
            if waypoint > 0 and ride.origin == currentNode:
                ride.pickupTime = currentTime
                self.numSeats -= 1
            elif waypoint < 0 and ride.destination == currentNode:
                ride.dropoffTime = currentTime
                self.numSeats += 1
                # remove this ride from self.rides
                self.rides.pop(ride.rideID)
                # save the pickup and travel delays
                performance[ride.rideID] = (
                    ride.pickupDelay(),ride.travelDelay()
                )
            else:
                break

            # remove this waypoint
            self.waypoints.pop(0)

        # set the next node and time        
        self.calcNextNodeTime(currentTime,network)

        return performance

    def calcNextNodeTime(self,currentTime,network):
        # compute the next route to the next waypoint if it exists
        currentNode = self.nextNode
        if self.waypoints:
            # the next node the vehicle is headed for
            destination = self.nextWaypointNode(self.waypoints[0])
            self.nextNode = network.nextNodeOnPathFromTo(
                currentNode,destination
            )
            if self.nextNode is None:
                self.nextNode = currentNode
                self.nextTime = currentTime
            else:
                self.nextTime = currentTime + network.graph\
                    [currentNode][self.nextNode]['traversal']
        else:
            # idle
            self.nextTime = None

