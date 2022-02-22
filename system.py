from network import RoadNetwork
from ride import Ride
from vehicle import Vehicle
from numpy.random import exponential

from sortedcontainers import SortedDict

class System:
    def __init__(self,gridSize = 10,numVehicles = 10,selfish = True,
                 capacity = 3,rideRate = 1,numRides = 50):

        self.selfish = selfish
        
        # make a suffix for outputting stats
        self.suffix = f'gs{gridSize}_nv{numVehicles}_cp{capacity}_rr{rideRate}'
        
        # init road network
        self.network = RoadNetwork()
        self.network.initGrid(gridSize,gridSize)

        # node arrival event queue
        self.nodeArrivalEvents = SortedDict()

        # list of available vehicles
        self.vehicles = [Vehicle(idx,capacity = capacity)
                         for idx in range(numVehicles)]

        # place the vehicles
        for v in self.vehicles:
            v.placeAtRandom(self.network)

        # generate random ride requests
        self.eventQueue = SortedDict()
        time = 0.
        self.rides = {}
        for rideID in range(1,numRides + 1):
            time += exponential(1./rideRate)
            ride = Ride(rideID,time)
            ride.random(self.network)
            self.eventQueue[ride.requestTime] = ride
            self.rides[ride.rideID] = ride

    def run(self):
        # process ride requests in order of request time and set the
        # vehicles in motion
        while self.eventQueue:
            time,value = self.eventQueue.popitem(0)
            if type(value) == Ride:
                ride = value
                print('Processing new ride request:',
                      ride.rideID,'at time:',time)
                # compute the total delays for each vehicle
                performance = sorted(
                    [(idx,*vehicle.delayDeltaAddedRide(
                        ride,self.network,self.selfish))
                     for idx,vehicle in enumerate(self.vehicles)],
                    key = lambda t: t[1]
                )
                vehID,delay,waypoints = performance[0]
                print('Best vehicle is',vehID,delay,waypoints)

                # add the ride to the vehicle
                vehicle = self.vehicles[vehID]
                vehicle.addRide(ride,waypoints)
                
                # vehicle was idle, add the node arrival event
                if vehicle.isIdle():
                    vehicle.calcNextNodeTime(time,self.network)
                    self.eventQueue[vehicle.nextTime] = vehicle

            elif type(value) == Vehicle:
                # the vehicle arrived at a node
                vehicle = value
                print('Vehicle',vehicle.ID,'arrived at node:',
                      vehicle.nextNode,'at time:',time)
                # this function will update waypoints, and return the
                # delay 2-tuples keyed by rideID if a ride(s) were
                # dropped off on this node
                performance = vehicle.processNodeArrival(time,self.network)
                if performance:
                    print('Performance:',performance)

                # add node arrival event if the vehicle is not idling
                if not vehicle.isIdle():
                    self.eventQueue[vehicle.nextTime] = vehicle

    def outputRideStates(self,outfile):
        with open(f'{outfile}_{self.suffix}','w') as f:
            for ride in self.rides.values():
                print(ride.rideID,ride.shortestTime,
                      ride.requestTime,ride.pickupTime,
                      ride.dropoffTime,file = f)
