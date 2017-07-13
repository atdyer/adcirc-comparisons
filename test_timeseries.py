from Adcirc.Run import Run
from DataStructures.Timeseries import Timeseries

run = Run('./Data/single-1')

timeseries = Timeseries(1, './Data/single-1/fort.63', run.mesh)
timeseries.advance()
# print(timeseries.nodal_value(1, 1))
# print(timeseries.nodal_value(2, 1))
# print(timeseries.nodal_value(3, 1))
#
# print(timeseries.nodal_value(1, 1.5))
# print(timeseries.nodal_value(2, 1.5))
# print(timeseries.nodal_value(3, 1.5))
#
# print(timeseries.nodal_value(1, 2))
# print(timeseries.nodal_value(2, 2))
# print(timeseries.nodal_value(3, 2))

print(timeseries.elemental_value(1, 1/3, 1/3, 1))
print(timeseries.elemental_value(1, 1/3, 1/3, 1.5))
print(timeseries.elemental_value(1, 1/3, 1/3, 2))