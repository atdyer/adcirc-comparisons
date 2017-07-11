from Adcirc.Files import *

f63 = Fort63('/home/tristan/box/adcirc/runs/scaled20-refinement/original/fort.63')

for ts in f63.timesteps():

    if ts.iteration == 3600:

        for node, value in ts.nodes():

            print(node, value)

        exit()