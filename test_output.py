from Adcirc.Run import Run
from Adcirc.Comparisons import Comparator, AverageMaximumDifference
from DataStructures.Shapes import Circle

test_output = './Data/comparisons.txt'
# run1 = Run('./Data/black')
# run2 = Run('./Data/blue')
# run3 = Run('./Data/red')

circle = Circle(-78.0094680, 33.8726840, 0.0035)
run1 = Run('/home/tristan/box/adcirc/runs/refinement/4/', circle)
run2 = Run('/home/tristan/box/adcirc/runs/refinement/original/', circle)

ele_comparator = Comparator()
ele_comparator.add_timeseries(run1.elevation_timeseries, True)
ele_comparator.add_timeseries(run2.elevation_timeseries)
# ele_comparator.add_timeseries(run3.elevation_timeseries)

ele_avg_max = AverageMaximumDifference()

ele_comparator.add_comparison(ele_avg_max)
ele_comparator.work()

for coordinates, avgs in ele_avg_max.nodes():
    print(coordinates, avgs)
exit()

vel_comparator = Comparator()
vel_comparator.add_timeseries(run1.velocity_timeseries, True)
vel_comparator.add_timeseries(run2.velocity_timeseries)
# vel_comparator.add_timeseries(run3.velocity_timeseries)

vel_avg_max = AverageMaximumDifference()

vel_comparator.add_comparison(vel_avg_max)
vel_comparator.work()

for coordinates, avgs in vel_avg_max.nodes():
    print(coordinates, avgs)