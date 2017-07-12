from DataStructures.Shapes import *
from Interpolator import Interpolator
from Adcirc.Run import Run

circle = Circle(-78.0094680, 33.8726840, 0.0035)
# circle = Infinite()

run1 = Run('/home/tristan/box/adcirc/runs/scaled20-noutgs/200/', circle)
run2 = Run('/home/tristan/box/adcirc/runs/scaled20-noutgs/3200/', circle)
run3 = Run('/home/tristan/box/adcirc/runs/scaled20-refinement/1/', circle)

interp = Interpolator()
interp.add_timeseries(run1.elevation_timeseries)

interp.flatten()
while interp.advance() is not None:
    for coordinates, values in interp.current_timestep():
        print(coordinates, values)