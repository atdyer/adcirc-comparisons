import math

def build_mesh(rows, cols, x_offset=0.0, y_offset=0.0, direction=0):

    node_rows = rows+1
    node_cols = cols+1

    nodes = dict()
    n = 1
    for i in range(node_rows):
        for j in range(node_cols):
            x = x_offset + float(j)
            y = y_offset + float(i)
            z = 0.0
            nodes[n] = (x, y, z)
            n += 1

    elements = dict()
    offset = cols+1
    e = 1

    for i in range(rows):
        for j in range(cols):
            bl = i*offset + 1 + j
            br = i*offset + 2 + j
            tl = (i+1)*offset + 1 + j
            tr = (i+1)*offset + 2 + j

            if direction == 0:
                elements[e] = (bl, tr, tl)
                e += 1
                elements[e] = (bl, br, tr)
                e += 1
            else:
                elements[e] = (bl, br, tl)
                e += 1
                elements[e] = (br, tr, tl)
                e += 1

    return nodes, elements

def write_fort14(f14, nodes, elements, name='ADCIRC Mesh'):

    with open(f14, 'w') as f:

        f.write(name + '\n')

        num_elements = len(elements)
        num_nodes = len(nodes)

        f.write('{} {}\n'.format(num_elements, num_nodes))

        for i in range(num_nodes):

            n = i+1
            x, y, z = nodes[n]
            f.write('{}\t{}\t{}\t{}\n'.format(n, x, y, z))

        for i in range(num_elements):

            e = i+1
            n1, n2, n3 = elements[e]
            f.write('{}\t3\t{}\t{}\t{}\n'.format(e, n1, n2, n3))

        f.write('0\n0\n0\n0\n')

def write_fort63(f63, nodes, dt, num_ts, name='ADCIRC Elevation Timeseries'):

    with open(f63, 'w') as f:

        f.write(name + '\n')
        f.write('{} {} {} {} {}\n'.format(num_ts, len(nodes), dt, 1, 1))

        for i, t, timestep in wave_elevations(nodes, dt, num_ts):

            f.write('{}\t{}\n'.format(t, i))

            for n in range(len(timestep)):

                node_number = n+1
                elevation = timestep[node_number]
                if node_number == 1: elevation = -99999

                f.write('{}\t{}\n'.format(node_number, elevation))

def write_fort64(f64, nodes, dt, num_ts, name='ADCIRC Velocity Timeseries'):

    with open(f64, 'w') as f:

        f.write(name + '\n')
        f.write('{} {} {} {} {}\n'.format(num_ts, len(nodes), dt, 1, 2))

        for i, t, timestep in wave_velocities(nodes, dt, num_ts):

            f.write('{}\t{}\n'.format(t, i))

            for n in range(len(timestep)):

                node_number = n+1
                xvel, yvel = timestep[node_number]
                f.write('{}\t{}\t{}\n'.format(node_number, xvel, yvel))


def wave_elevations(nodes, dt, num_ts):

    for i in range(num_ts):
        t = i*dt
        timeseries = dict()
        for n, (x, y, z) in nodes.items():
            timeseries[n] = math.sin(x+y+t)
        yield i, t, timeseries

def wave_velocities(nodes, dt, num_ts):

    for i in range(num_ts):
        t = i*dt
        timeseries = dict()
        for n, (x, y, z) in nodes.items():
            timeseries[n] = (math.sin(x+t), math.cos(y+t))
        yield i, t, timeseries


print('Generating black run')
black_nodes, black_elements = build_mesh(3, 3)
black_mesh = './Data/black/fort.14'
black_elevations = './Data/black/fort.63'
black_velocities = './Data/black/fort.64'
write_fort14(black_mesh, black_nodes, black_elements, 'Black Test Mesh')
write_fort63(black_elevations, black_nodes, 0.1, 50, 'Black Test Mesh')
write_fort64(black_velocities, black_nodes, 0.1, 50, 'Black Test Mesh')

print('Generating blue run')
blue_nodes, blue_elements = build_mesh(2, 2, 0.5, 0.5, 1)
blue_mesh = './Data/blue/fort.14'
blue_elevations = './Data/blue/fort.63'
blue_velocities = './Data/blue/fort.64'
write_fort14(blue_mesh, blue_nodes, blue_elements, 'Blue Test Mesh')
write_fort63(blue_elevations, blue_nodes, 0.1, 50, 'Blue Test Mesh')
write_fort64(blue_velocities, blue_nodes, 0.1, 50, 'Blue Test Mesh')

print('Generating red run')
red_nodes = {
    1: (1.5, 1.0, 0.0),
    2: (1.0, 1.5, 0.0),
    3: (2.0, 1.5, 0.0),
    4: (1.5, 2.0, 0.0)
}
red_elements = {
    1: (1, 4, 2),
    2: (1, 3, 4)
}
red_mesh = './Data/red/fort.14'
red_elevations = './Data/red/fort.63'
red_velocities = './Data/red/fort.64'
write_fort14(red_mesh, red_nodes, red_elements, 'Red Test Mesh')
write_fort63(red_elevations, red_nodes, 0.1, 50, 'Red Test Mesh')
write_fort64(red_velocities, red_nodes, 0.1, 50, 'Red Test Mesh')