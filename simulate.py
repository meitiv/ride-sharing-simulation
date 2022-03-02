#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--selfish',action = 'store_true')
parser.add_argument('grid_size',type = int)
parser.add_argument('num_vehicles',type = int)
parser.add_argument('veh_capacity',type = int,help = 'number of seats')
parser.add_argument('ride_rate',type = float)
parser.add_argument('num_rides',type = int,
                    help = 'number of rides to generate')
args = parser.parse_args()

import system

s = system.System(
    gridSize = args.grid_size,
    numVehicles = args.num_vehicles,
    selfish = args.selfish,
    capacity = args.veh_capacity,
    rideRate = args.ride_rate,
    numRides = args.num_rides
)
s.run()
s.outputRideStats('rides')
