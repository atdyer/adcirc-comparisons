from Adcirc.Comparisons import compare_elevation_timeseries

test_output = './Data/comparisons.txt'
# run1 = './Data/single-1'
# run2 = './Data/single-1-offset'
# run3 = './Data/single-2'

run1 = '/home/tristan/box/adcirc/runs/refinement/original'
run2 = '/home/tristan/box/adcirc/runs/refinement/16'


compare_elevation_timeseries(test_output, run1, run2)
