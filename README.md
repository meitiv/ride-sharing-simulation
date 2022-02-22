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
$ ./simulate.py
```
