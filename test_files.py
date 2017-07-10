from Adcirc.Files import *

f63 = Fort63('/home/tristan/box/adcirc/runs/scaled20-refinement/original/fort.63')

for ts in f63.timesteps():

    print(ts.iteration, ts.model_time, ts.range())