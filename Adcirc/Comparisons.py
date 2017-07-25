from Adcirc.Run import Run
from Interpolator import Interpolator
from abc import ABCMeta, abstractmethod
import itertools

class Comparator:

    def __init__(self):

        self._interpolator = Interpolator()
        self._comparisons = []
        self._baseline_index = None

    def add_comparison(self, comparison):

        self._comparisons.append(comparison)

        if self._baseline_index is not None and isinstance(comparison, BaselineComparison):

            comparison.set_baseline(self._baseline_index)

    def add_timeseries(self, timeseries, is_baseline=False):

        index = self._interpolator.add_timeseries(timeseries)

        if is_baseline:

            self._baseline_index = index

    def work(self):

        # Initialize the interpolator
        self._interpolator.flatten()

        print('Starting timestepping')

        # Start timestepping
        while self._interpolator.advance():

            for comparison in self._comparisons:

                comparison.advance()

            for coordinates, values in self._interpolator.current_timestep():

                for comparison in self._comparisons:

                    comparison.nodal_values(coordinates, values)

        print('Finished timestepping')

        for comparison in self._comparisons:

            comparison.done()


class Comparison(metaclass=ABCMeta):

    @abstractmethod
    def advance(self):
        """This method must prepart the Comparison to recieve the next set timestep data"""

    @abstractmethod
    def nodal_values(self, coordinates, values):
        """Called for each node in a single timestep"""

    @abstractmethod
    def done(self):
        """Called when finished timestepping"""

    @abstractmethod
    def save(self, file):
        """This method must provide a way to write the data to file"""

class BaselineComparison(Comparison):

    @abstractmethod
    def set_baseline(self, index):
        """Sets the index in the values array to use as the baseline"""

class AverageMaximumDifference(Comparison):

    def __init__(self):
        """At every node, calculates the largest difference in values and averages this value across all timesteps"""

        self._count = 0
        self._accumulator = dict()

    def advance(self):
        pass

    def nodal_values(self, coordinates, values):

        rotated = tuple(zip(*values))
        min_vals = tuple(min(t) for t in rotated)
        max_vals = tuple(max(t) for t in rotated)
        diffs = tuple(high-low for high, low in zip(max_vals, min_vals))

        if coordinates not in self._accumulator:

            if -99999.0 in min_vals:

                self._accumulator[coordinates] = [0, tuple(-99999.0 for _ in diffs)]

            else:

                self._accumulator[coordinates] = [1, diffs]

        else:

            if not -99999.0 in min_vals:

                if self._accumulator[coordinates][0] == 0:

                    self._accumulator[coordinates] = [1, diffs]

                else:

                    accum = self._accumulator[coordinates][1]
                    self._accumulator[coordinates][0] += 1
                    self._accumulator[coordinates][1] = tuple(map(lambda a, b: a + b, accum, diffs))

    def nodes(self):

        for coordinates, (count, values) in self._accumulator.items():

            if count == 0:

                yield coordinates, values

            else:

                yield coordinates, tuple(map(lambda x: x/count, values))

    def done(self):

        for coordinates, (count, values) in self._accumulator.items():

            if count == 0:

                print('\t\N{WHITE BULLET} No average maximum difference available for', coordinates, ' because all values were -99999')

    def save(self, file):

        with open(file, 'w') as f:

                f.write('x\ty\taverage maximum difference\n')

                for coordinates, values in self.nodes():

                    f.write('\t'.join(str(coord) for coord in coordinates) + '\t' + '\t'.join(str(val) for val in values) + '\n')



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
