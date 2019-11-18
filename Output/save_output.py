import pandas as pd

writer = pd.ExcelWriter("Output/output.xlsx", engine='xlsxwriter')


def save_output(models, fixed, dynamics, station_obj):
    dataframes_dict = {}
    for i in range(len(models)):
        key = "solvable_instance_" + str(len(fixed[i].stations)) + '_' + str(len(fixed[i].vehicles))
        if key not in dataframes_dict.keys():
            df = pd.DataFrame(columns=['Init #stations', 'No. of stations', 'No. of vehicles',
                                                         'Vehicle capacity', 'Station capacity', 'Time Horizon',
                                                         'Demand scenario', 'Solution time', 'Gap', 'weight violation',
                                                         'weight deviation', 'weight reward', 'reward weight dev',
                                                         'reward weight time'])
            for v in range(len(fixed[i].vehicles)):
                df['Start vehicle' + str(v)] = ""
            dataframes_dict[key] = df

        new_row = {'Init #stations': fixed[i].initial_size, 'No. of stations': len(fixed[i].stations)-2,
                   'No. of vehicles': len(fixed[i].vehicles), 'Vehicle capacity': fixed[i].vehicle_cap[0],
                   'Station capacity': fixed[i].station_cap[1], 'Time Horizon': fixed[i].time_horizon,
                   'Demand scenario': fixed[i].demand_scenario, 'Solution time': models[i][1],
                   'Gap': models[i][0].mipgap, 'weight violation': fixed[i].w_violation,
                   'weight deviation': fixed[i].w_dev_obj, 'weight reward': fixed[i].w_reward,
                   'reward weight dev': fixed[i].w_dev_reward, 'reward weight time': fixed[i].w_driving_time}

        for v in range(len(fixed[i].vehicles)):
            new_row['Start vehicle' + str(v)] = station_obj[i][dynamics[i].start_stations[v]].address

        for var in models[i][0].getVars():
            new_row[var.varName] = var.x
        dataframes_dict[key] = dataframes_dict[key].append(new_row, ignore_index=True)

    for sheet_name, df in dataframes_dict.items():
        df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
