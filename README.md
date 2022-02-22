# Ride Sharing Simulation

This repository contains Python code to simulate random ride
generation and dispatch to shared vehicles on a square grid.

### Installation
In a Linux (or WSL) environemnt install python3, python3-pip and the
requirements by running
```bash
$ sudo apt install python3 python3-pip
$ sudo -H pip3 install -r requirements
```

### Simulation

The transportation system is an N by N square grid in which traversal
of each edge is a random number drawn from a Gaussian distribution
with unit mean and the standard deviation of 0.01.  The standard
deviation can be changed via a parameter to the `__init__()` function
of the `RoadwayNetwork` object.  Rides are generated at random with a
rate `ride_rate` rides per unit time.  The origins and destinations of
the rides are picked at random on the grid with the constraint that
the origin must differ from the destination.  Vehicles move across the
network according to the traversal times of the edges (links) picking
up and dropping off rides.  We assume that pickups, dropoffs, and
intersections do not take any time.  Each vehicle can have at most
`veh_capacity` concurrent rides.  New ride requests are matched to the
vehicle in such a way as to minimize the delay of the new ride.  The
`--selfish` flag determines whether the delays of existing rides can
be increased in the process of selecting the optimal pickup/dropoff
sequence.  When this flag is added to the command line, the delays of
existing (picked up or scheduled) rides cannot be increased by the new
ride.

The simulation is run via
```bash
$ ./simulate.py [--selfish] N num_vehicles veh_capacity ride_rate num_rides
```
where
1. `--selfish` changes how new rides are matched to vehicles
2. `N` is the size of the square grid (number of links on a side)
3. `num_vehicles` is the number of vehicles in the transportation system
4. `veh_capacity` is the maximum number of concurrent pickup rides
5. `ride_rate` is the average number of ride requests per unit time
6. `num_rides` number of rides to generate and process before stopping
   the simulation
   
The simulation script outputs lots of diagnostic data which can be
safely ignored and redirected to `/dev/null`.  Upon completion the
script will create a file whose name is composed of 5 parts separated
by underscores, for example:
`rides_gs10_nv20_cp3_rr2.0`
Parts 2 through 5 of the filename encode the parameters of the
simulation: `gs` is grid size, `nv` is the number of vehicles, `cp` is
the vehicle capacity, and `rr` is the ride rate.
The file contains 5 space separated columns,
- Ride number
- Shortest route duration for that ride
- Ride request time
- Ride pickup time
- Ride dropoff time

After running a number of simulations with different parameters, one
can use a helper script `process_results.py` which is run without
command line parameters.  It computes the average and standard
deviation of the ride delays for every simulation run and outputs a
comma delimited `results.csv` with columns
- gs
- nv
- cp
- rr
- meanPickupDelay
- meanTravelDelay
- stdPickupDelay
- stdTravelDelay
