from run_model import Subproblem

horizons = 1
id_list = ['377', '380']
demand = [0.5, 0.3]
init_bikes = [5, 3]
init_rates = [0.4, 0.8]
outgoing_rates = [1, 2]
init_vehicles = [15]
start_stations = [1]
time_to_start = [0]

total_obj = 0

for i in range(horizons):
    sub = Subproblem(None, demand, init_bikes, init_vehicles, start_stations, time_to_start)
    model = sub.run_model()
    total_obj += model.objVal
    for var in model.getVars():
        pass
