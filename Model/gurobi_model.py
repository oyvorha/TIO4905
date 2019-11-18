from gurobipy import *
from Input.fixed_file_variables import FixedFileVariables
from Input.dynamic_file_variables import DynamicFileVariables
import time


def run_model(instance, last_mode=False):

    if last_mode:
        f = FixedFileVariables()
        d = DynamicFileVariables()
    else:
        f = instance.fixed
        d = instance.dynamic

    try:
        m = Model("Bicycle")
        start_time = time.time()

        # ------ SETS -----------------------------------------------------------------------------
        Stations = f.stations
        Swap_Stations = Stations[1:-1]
        Vehicles = f.vehicles

        # ------ FIXED PARAMETERS -----------------------------------------------------------------
        time_horizon = f.time_horizon
        vehicle_cap = f.vehicle_cap
        station_cap = f.station_cap
        driving_times = f.driving_times
        parking_time = f.parking_time
        handling_time = f.handling_time

        M_1 = f.M_1
        M_2 = f.M_2
        M_3 = f.M_3
        M_4 = f.M_4
        M_5 = f.M_5
        M_6 = f.M_6
        M_7A = f.M_7A
        M_7B = f.M_7B
        M_8A = f.M_8A
        M_8B = f.M_8B
        M_9 = f.M_9
        M_10 = f.M_10
        M_11 = f.M_11
        M_12 = f.M_12
        M_13 = f.M_13
        M_14 = f.M_14

        w_dev_reward = f.w_dev_reward
        w_driving_times = f.w_driving_time
        w_dev_obj = f.w_dev_obj
        w_reward = f.w_reward
        w_violation = f.w_violation

        # ------- DYNAMIC PARAMETERS --------------------------------------------------------------
        start_stations = d.start_stations
        init_vehicle_load = d.init_vehicle_load
        init_station_load = d.init_station_load
        init_flat_station_load = d.init_flat_station_load
        ideal_state = d.ideal_state
        driving_to_start = d.driving_to_start
        demand = d.demand
        incoming_rate = d.incoming_rate
        incoming_flat_rate = d.incoming_flat_rate

        # ------ VARIABLES -------------------------------------------------------------------------
        x = m.addVars({(i, j, v) for i in Stations[:-1]
                         for j in Stations for v in Vehicles}, vtype=GRB.BINARY, lb=0, name="x")
        t = m.addVars({i for i in Stations[1:]}, vtype=GRB.CONTINUOUS, lb=0, name="t")
        q = m.addVars({(i, v) for i in Swap_Stations for v in Vehicles}, vtype=GRB.INTEGER, lb=0, name="q")
        l_B = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="l_B")
        l_F = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="l_F")
        l_V = m.addVars({(i, v) for i in Stations for v in Vehicles}, vtype=GRB.INTEGER, lb=0, name="l_V")
        s_B = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="s_B")
        s_F = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="s_F")
        s_V = m.addVars({v for v in Vehicles}, vtype=GRB.CONTINUOUS, lb=0, name="s_V")
        v_S = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="v_S")
        d = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="d")
        delta = m.addVars({i for i in Swap_Stations}, vtype=GRB.BINARY, name="delta")
        gamma = m.addVars({i for i in Swap_Stations}, vtype=GRB.BINARY, name="gamma")
        v_Sf = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, name="v_Sf")
        v_SF = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, name="v_SF")
        omega = m.addVars({i for i in Stations}, vtype=GRB.BINARY, name="omega")
        r_D = m.addVars({i for i in Swap_Stations}, vtype=GRB.CONTINUOUS, lb=0, name="r_D")
        t_f = m.addVars({v for v in Vehicles}, vtype=GRB.CONTINUOUS, lb=0, name="t_f")
        t_D = m.addVars({v for v in Vehicles}, vtype=GRB.CONTINUOUS, lb=0, name="t_D")

        # ------- FEASIBILITY CONSTRAINTS ----------------------------------------------------------
        # Routing constraints
        m.addConstrs(x.sum(start_stations[v], '*', v) == 1 for v in Vehicles)
        m.addConstrs(x.sum('*', Stations[-1], v) == 1 for v in Vehicles)
        for j in Stations[:-1]:
            for v in Vehicles:
                if j != start_stations[v]:
                    m.addConstr(x.sum('*', j, v) - x.sum(j, '*', v) == 0)
        m.addConstrs(x.sum('*', j, '*') <= 1 for j in Swap_Stations)
        m.addConstrs(x.sum('*', Stations[0], v) <= 1 for v in Vehicles)
        m.addConstrs(x.sum('*', '*', v) <= (len(Stations)-1) for v in Vehicles)
        for i in Stations[:-1]:
            for j in Stations:
                if i == j:
                    m.addConstrs(x[(i, j, v)] <= 0 for v in Vehicles)
        m.addConstrs(x[(Stations[0], Stations[-1], v)] <= 0 for v in Vehicles)

        # Time Constraints
        m.addConstrs(t[i] + parking_time + handling_time * q.sum(i, '*') + driving_times[i][j]
                     - t[j] - M_1[i][j] * (1 - x.sum(i, j, '*')) <= 0 for i in Swap_Stations for j in Stations[1:])
        m.addConstrs(t[i] + parking_time + handling_time * q.sum(i, v) + driving_times[i][Stations[0]]
                     - t_D[v] - M_1[i][Stations[0]] * (1 - x.sum(i, Stations[0], v)) <= 0 for i in Swap_Stations
                     for v in Vehicles)
        m.addConstrs(t_D[v] + parking_time + driving_times[Stations[0]][j]
                     - t[j] - M_1[0][j] * (1 - x.sum(Stations[0], j, v)) <= 0 for j in Stations[1:] for v in Vehicles)
        for v in Vehicles:
            if start_stations[v] != Stations[0]:
                m.addConstr(t[start_stations[v]] >= driving_to_start[v])
            else:
                m.addConstr(t_D[v] >= driving_to_start[v])
        m.addConstrs(t[i] - time_horizon - M_2[i] * x.sum(i, Stations[-1], '*') <= 0 for i in Swap_Stations)
        m.addConstrs(t_D[v] - time_horizon - M_2[0] * x.sum(Stations[0], Stations[-1], v) <= 0 for v in Vehicles)
        m.addConstrs(t[i] - M_3[i] * x.sum(i, '*', '*') <= 0 for i in Swap_Stations)
        m.addConstrs(t_D[v] - M_3[0] * x.sum(Stations[0], '*', v) <= 0 for v in Vehicles)

        # Vehicle Loading Constraints
        m.addConstrs(q[(i, v)] <= l_V[(i, v)] for i in Swap_Stations for v in Vehicles)
        m.addConstrs(l_V[(start_stations[v], v)] == init_vehicle_load[v] for v in Vehicles)
        m.addConstrs(
            l_V[(j, v)] - vehicle_cap[v] - M_4 * (1 - x[(Stations[0], j, v)]) <= 0 for j in Stations for v in Vehicles)
        m.addConstrs(
            l_V[(j, v)] - vehicle_cap[v] + M_4 * (1 - x[(Stations[0], j, v)]) >= 0 for j in Stations for v in Vehicles)
        m.addConstrs(-l_V[(j, v)] + l_V[(i, v)] - q[(i, v)] - M_5 * (
                1 - x[(i, j, v)]) <= 0 for i in Swap_Stations for j in Stations for v in Vehicles)
        m.addConstrs(-l_V[(j, v)] + l_V[(i, v)] - q[(i, v)] + M_5 * (
                1 - x[(i, j, v)]) >= 0 for i in Swap_Stations for j in Stations for v in Vehicles)

        # Station Loading Constraints
        m.addConstrs(l_F[i] == init_flat_station_load[i] + incoming_flat_rate[i] * t[i] for i in Swap_Stations)

        m.addConstrs(l_B[i] == init_station_load[i] + (
                incoming_rate[i] - demand[i]) * t[i] + v_S[i] for i in Swap_Stations)

        m.addConstrs(q.sum(i, '*') <= l_F[i] for i in Swap_Stations)
        m.addConstrs(q[(i, v)] - vehicle_cap[v] * x.sum(i, '*', v) <= 0 for i in Swap_Stations for v in Vehicles)

        # ------- VIOLATION CONSTRAINTS ------------------------------------------------------------------
        m.addConstrs(t[i] <= time_horizon + M_6[i] * delta[i] for i in Swap_Stations)
        m.addConstrs(t[i] >= time_horizon * delta[i] for i in Swap_Stations)
        m.addConstrs(delta[i] <= x.sum(i, Stations[-1], '*') for i in Swap_Stations)
        m.addConstrs(gamma[i] == x.sum(i, '*', '*') for i in Swap_Stations)

        # Situation 1
        m.addConstrs(s_B[i] <= init_station_load[i] + (incoming_rate[i] - demand[i]
                                                        ) * time_horizon + v_Sf[i] + M_7A[i] * gamma[i] for i in
                     Swap_Stations)
        m.addConstrs(s_B[i] >= init_station_load[i] + (incoming_rate[i] - demand[i]
                                                        ) * time_horizon + v_Sf[i] - M_7A[i] * gamma[i] for i in Swap_Stations)
        m.addConstrs(s_F[i] <= init_flat_station_load[i] +
                     incoming_flat_rate[i] * time_horizon + M_7B[i] * gamma[i] for i in Swap_Stations)
        m.addConstrs(s_F[i] >= init_flat_station_load[i] +
                     incoming_flat_rate[i] * time_horizon - M_7B[i] * gamma[i] for i in Swap_Stations)

        # Situation 2
        m.addConstrs(s_B[i] <= l_B[i] + q.sum(i, '*') + (incoming_rate[i]-demand[i]) * (
                    time_horizon - t[i]) + v_Sf[i] + M_8A[i] * (1 - gamma[i] + delta[i]) for i in Swap_Stations)
        m.addConstrs(s_B[i] >= l_B[i] + q.sum(i, '*') + (incoming_rate[i] - demand[i]) * (
                    time_horizon - t[i]) + v_Sf[i] - M_8A[i] * (1 - gamma[i] + delta[i]) for i in Swap_Stations)
        m.addConstrs(s_F[i] <= l_F[i] - q.sum(i, '*') + incoming_flat_rate[i] * (
                    time_horizon - t[i]) + M_8B[i] * (1 - gamma[i] + delta[i]) for i in Swap_Stations)
        m.addConstrs(s_F[i] >= l_F[i] - q.sum(i, '*') + incoming_flat_rate[i] * (
                    time_horizon - t[i]) - M_8B[i] * (1 - gamma[i] + delta[i]) for i in Swap_Stations)

        # Situation 3
        m.addConstrs(l_B[i] <= s_B[i] + (incoming_rate[i] - demand[i]) * (
                    t[i] - time_horizon) + v_SF[i] + M_9[i] * (1 - delta[i]) for i in Swap_Stations)
        m.addConstrs(l_B[i] >= s_B[i] + (incoming_rate[i] - demand[i]) * (
                t[i] - time_horizon) + v_SF[i] - M_9[i] * (1 - delta[i]) for i in Swap_Stations)
        m.addConstrs(l_F[i] <= s_F[i] + incoming_flat_rate[i] * (t[i]-time_horizon) + M_10[i] * (1 - delta[i]
                                                                                           ) for i in Swap_Stations)
        m.addConstrs(l_F[i] >= s_F[i] + incoming_flat_rate[i] * (t[i] - time_horizon) - M_10[i] * (1 - delta[i]
                                                                                             ) for i in Swap_Stations)
        m.addConstrs(l_B[i] + station_cap[i] * omega[i] <= station_cap[i] for i in Swap_Stations)
        m.addConstrs(1 - omega[i] <= l_B[i] for i in Swap_Stations)
        m.addConstrs((v_S[i] - v_SF[i]) - M_11[i] * (omega[i] - delta[i] + 1) <= 0 for i in Swap_Stations)
        m.addConstrs(v_SF[i] <= M_12[i] * delta[i] for i in Swap_Stations)
        m.addConstrs(v_SF[i] - M_13[i] * (1 - delta[i]) <= v_S[i] for i in Swap_Stations)

        # ------- DEVIATIONS -----------------------------------------------------------------------------
        m.addConstrs(d[i] >= ideal_state[i] - s_B[i] for i in Swap_Stations)
        m.addConstrs(d[i] >= s_B[i] - ideal_state[i] for i in Swap_Stations)

        # ------- OBJECTIVE CONSTRAINTS ------------------------------------------------------------------
        m.addConstrs(s_V[v] >= l_V[(i, v)] - q[(i, v)]-(
                1-x[(i, Stations[-1], v)]) * vehicle_cap[v] for i in Swap_Stations for v in Vehicles)
        m.addConstrs(s_V[v] <= l_V[(i, v)] - q[(i, v)] + (
                1 - x[(i, Stations[-1], v)]) * vehicle_cap[v] for i in Swap_Stations for v in Vehicles)
        m.addConstrs(r_D[i] <= q.sum(i, '*') + station_cap[i] * (1 - delta[i])
                     for i in Swap_Stations)
        m.addConstrs(r_D[i] <= delta[i] * station_cap[i] for i in Swap_Stations)
        m.addConstrs(t_f[v] - t[i] + time_horizon + M_14[v] * (1 - delta[i]) >= 0
                     for i in Swap_Stations for v in Vehicles)
        m.addConstrs(t_f[v] - t[i] + time_horizon - M_14[v] * (1 - delta[i]) <= 0
                     for i in Swap_Stations for v in Vehicles)

        # ------- OBJECTIVE ------------------------------------------------------------------------------
        m.setObjective(w_violation * (v_S.sum('*') - v_SF.sum('*') + v_Sf.sum('*')) + w_dev_obj * d.sum('*')
                       - w_reward * (w_dev_reward * r_D.sum('*') - w_driving_times * t_f.sum('*')), GRB.MINIMIZE)

        m.optimize()
        end_time = time.time()

        exec_time = end_time - start_time
        print("Execution time was", exec_time)

        return m, exec_time

    except GurobiError:
        print("Error")
