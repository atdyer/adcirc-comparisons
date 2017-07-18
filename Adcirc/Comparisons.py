from Adcirc.Run import Run
from Interpolator import Interpolator
import itertools

def compare_elevation_timeseries(output_file, *args):

    width = '15'
    header = ['x', 'y', 'ele_rmse', 'ele_avg_err', 'ele_max_err']


    fmt = ' '.join(['{:> '+width+'f} ' for _ in header]) + '\n'
    fmt_header = ' '.join(['{:>'+width+'} ' for _ in header]) + '\n'


    runs = [Run(path) for path in args]

    if None in [run.elevation_timeseries for run in runs]:
        print('One or more of the runs does not have a fort.63 file')
        exit()

    interp = Interpolator()

    for run in runs:
        interp.add_timeseries(run.elevation_timeseries)

    interp.flatten()
    nodes = dict()

    for coordinates in interp.nodes():

        nodes[coordinates] = [0.0]*len(runs)

    with open(output_file, 'w') as f:

        f.write(fmt_header.format(*header))

        num_data_points = 0

        while interp.advance():

            for coordinates, values in interp.current_timestep():

                num_data_points += 1
                print('Evaluating dataset', num_data_points)

                min_val = min(values)
                max_val = max(values)
                err = tuple(high-low for high in max_val for low in min_val)

                nodes[coordinates][1] += err[0]
                nodes[coordinates][2] = max(nodes[coordinates][2], err[0])

        for coordinates, values in nodes.items():

            values[1] /= num_data_points
            f.write(fmt.format(*itertools.chain(coordinates, values)))
