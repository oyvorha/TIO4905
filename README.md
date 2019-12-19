# AOO026
Optimization model with Gurobi

This model implements the static and deterministic subproblem of the
*Dynamic Stochastic Bicycle Battery Swap Routing Problem*. The test instance data is collected from Oslo City Bike.

The model is run from **run_model.py** where the following input-parameters should be set:
**n_instances** = the number of stations to include \
**scenario** = set to either 'A', 'B', 'C', 'D' or 'E', representing the demand at a specified interval of time of day \
**n_vehicles** = the number of service vehicles operated \
**time_horizon** = the planning horizon for the subproblem \
**vehicle_cap** = the capacity of batteries of the vehicles \
**station_cap** = the number of locks on the stations \
**ideal_state** = the ideal number of battery bikes at each station \

An overview of the stations in the BSS with related data should be placed at the user root. This file should be an
.xlsx file with the following columns:
Station ID,	Station name, Station Address, latitude, longitude, init_B_bikes, init_F_bikes, Scenario, Demand,
Ideal State, B-bike-rate, F-bike-rate

The model output is visualized with *matplotlib* and saved in "Output/output.xlsx"
