from DataStructures.Shapes import *
from Interpolator import Interpolator
from Adcirc.Run import Run

circle = Circle(-78.0094680, 33.8726840, 0.01)
# circle = Infinite()

run1 = Run('/home/tristan/box/adcirc/runs/scaled20-noutgs/200/', circle)
run2 = Run('/home/tristan/box/adcirc/runs/scaled20-noutgs/3200/', circle)
run3 = Run('/home/tristan/box/adcirc/runs/scaled20-refinement/1/', circle)

interp = Interpolator()
interp.add_run(run1)
interp.add_run(run2)
interp.add_run(run3)

interp.flatten()
interp.align_elevation_timeseries()
interp.calculate_maximum_elevation_differences()