#Task/Location Allocation

This was designed as a hobby project inspired by a problem we faced at JPAL.

This script takes in a csv and outputs a list of locations we can give to one agent.
The locations are chosen such that some of these locations are within a given threshold distance from eachother, while others are farther away from that distance.

The script also prints out a distance matrix so the user can easily look at the distribution of tasks and distances finally allocated.

All parameters are asked as inputs from the user and the code itself doesn't have these parameters pre defined. The code is just a collection of function definitions.
