import pandas as pd


def save_output(models, fixed, dynamics):
    solvable_instance = pd.DataFrame(columns=['Init #stations', 'No. of stations', 'No. of vehicles', 'Demand scenario',
                                              'Solution time', 'Gap'])
    for i in range(len(models)):
        new_row = {'Init #stations': fixed[i].initial_size, 'No. of stations': len(fixed[i].stations)-2,
                   'No. of vehicles': len(fixed[i].vehicles), 'Demand scenario': fixed[i].demand_scenario,
                   'Solution time': models[i][1], 'Gap': models[i][0].mipgap}
        solvable_instance = solvable_instance.append(new_row, ignore_index=True)

    solvable_instance.to_excel("Output/output.xlsx", sheet_name="Size of solvable instance")
