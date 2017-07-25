# adcirc-comparisons

The adcirc-comparisons library allows you to write Python scripts that can be used to perform comparisons among ADCIRC
datasets regardless if meshes and times are identical or not. 

## Writing Scripts

In general, scripts will follow the following general process:

0. (Optional) Create a masking shape
1. Read data from multiple ADCIRC runs
2. Create a Comparator and add timeseries data to it
3. Create one or more Comparisons and add them to the comparator
4. Process the comparisons
5. Output results
6. Visualize results

The following sections will build a script, step-by-step, showing how to perform a single comparison between
two ADCIRC runs.

### (Optional) Create a masking Shape

The first optional step is to create a masking shape. If you only wish to perform a comparison in a specific
geographic region, you can create a shape inside of which the comparisons will be performed. Nodes and elements
that fall outside of the shape will be ignored completely and not included in the output. This can be
benefitial when performing comparisons with, for example, two full domains, but you only care about results
in a tiny geographic region. When using a mask with large meshes, the speed of processing is increased
significantly.

Here we'll create a circle as our mask.

```python
from DataStructures.Shapes import Circle

# A Circle takes a center point and a radius
circle = Circle(-78.0094680, 33.8726840, 0.0035)
```

### Read data from multiple ADCIRC runs
Next, we need to create at least two ADCIRC runs in order to perform a comparison. The ```Run``` class
provides an overarching container for all data associated with a single ADCIRC run.
An instance only needs to know the directory containing the ADCIRC run in order to automatically
load all data associated with that run. Currently the following two datasets are exposed by a ```Run```
instance:

* ```Run.elevation_timeseries``` - The elevation timeseries data contained by fort.63
* ```Run.velocity_timeseries``` - The velocity timeseries data contained by fort.64

Create two ```Run``` instances, applying the circle mask that we've created.

```python
from DataStructures.Shapes import Circle
from Adcirc.Run import Run

# A Circle takes a center point and a radius
circle = Circle(-78.0094680, 33.8726840, 0.0035)
run1 = Run('/home/tristan/adcirc/runs/run1/', circle)
run2 = Run('/home/tristan/adcirc/runs/run2/', circle)
```

### Create a Comparator and add timeseries data
The ```Comparator``` class provides the means to perform a comparison between two datasets. It's important to note
that when adding data to a ```Comparator```, all data must have the same number of dimensions. For example,
trying to perform a comparison between elevation and velocity data will not work because elevation data is
one dimensions while velocity data is two dimensional (x- and y- velocities).

For this example, we will compare the elevation timeseries (fort.63) data between the two ADCIRC runs.

```python
from DataStructures.Shapes import Circle
from Adcirc.Run import Run
from Adcirc.Comparisons import Comparator

# A Circle takes a center point and a radius
circle = Circle(-78.0094680, 33.8726840, 0.0035)
run1 = Run('/home/tristan/adcirc/runs/run1/', circle)
run2 = Run('/home/tristan/adcirc/runs/run2/', circle)

# Create a comparator to compare elevation timeseries data
elevation_comparator = Comparator()
elevation_comparator.add_timeseries(run1.elevation_timeseries)
elevation_comparator.add_timeseries(run2.elevation_timeseries)
```

### Create Comparisons and add them to the Comparator
Now that we have a ```Comparator```, we are able to perform comparisons among meshes. However, we must now
tell the ```Comparator``` which comparisons to make when processing the data. For this example, we want to
look at the average maximum difference at each node.

The average maximum difference will, at a single node in a single timestep, look at the value at that time
and location for every ADCIRC run in the comparator. It will determine the minimum value and the maximum value
and calculate the difference between the two (i.e. the maximum difference). It will do this for every timestep
and calculate the average value through time. 

This is performed for every single node that falls into the
overlapping portion of all meshes in the comparator. Nodes that fall geographically into the overlapping section
but are not common to all meshes are interpolated in the meshes that do not explicitly contain those nodes.

```python
from DataStructures.Shapes import Circle
from Adcirc.Run import Run
from Adcirc.Comparisons import Comparator, AverageMaximumDifference

# A Circle takes a center point and a radius
circle = Circle(-78.0094680, 33.8726840, 0.0035)
run1 = Run('/home/tristan/adcirc/runs/run1/', circle)
run2 = Run('/home/tristan/adcirc/runs/run2/', circle)

# Create a comparator to compare elevation timeseries data
elevation_comparator = Comparator()
elevation_comparator.add_timeseries(run1.elevation_timeseries)
elevation_comparator.add_timeseries(run2.elevation_timeseries)

# Create a comparison to perform
average_max_diff = AverageMaximumDifference()
elevation_comparator.add_comparison(average_max_diff)
```

### Process the comparisons
To kick of the processing of data once you have added all of your comparisons,
simply call ```Comparator.work()```

```python
from DataStructures.Shapes import Circle
from Adcirc.Run import Run
from Adcirc.Comparisons import Comparator, AverageMaximumDifference

# A Circle takes a center point and a radius
circle = Circle(-78.0094680, 33.8726840, 0.0035)
run1 = Run('/home/tristan/adcirc/runs/run1/', circle)
run2 = Run('/home/tristan/adcirc/runs/run2/', circle)

# Create a comparator to compare elevation timeseries data
elevation_comparator = Comparator()
elevation_comparator.add_timeseries(run1.elevation_timeseries)
elevation_comparator.add_timeseries(run2.elevation_timeseries)

# Create a comparison to perform
average_max_diff = AverageMaximumDifference()
elevation_comparator.add_comparison(average_max_diff)

# Process the data and perform comparisons
elevation_comparator.work()
```

### Output results

More coming soon, as there are multiple ways to do this. To write out the values for the average maximum difference
comparison, just use the ```Comparison.save()``` method.

```python
from DataStructures.Shapes import Circle
from Adcirc.Run import Run
from Adcirc.Comparisons import Comparator, AverageMaximumDifference

# A Circle takes a center point and a radius
circle = Circle(-78.0094680, 33.8726840, 0.0035)
run1 = Run('/home/tristan/adcirc/runs/run1/', circle)
run2 = Run('/home/tristan/adcirc/runs/run2/', circle)

# Create a comparator to compare elevation timeseries data
elevation_comparator = Comparator()
elevation_comparator.add_timeseries(run1.elevation_timeseries)
elevation_comparator.add_timeseries(run2.elevation_timeseries)

# Create a comparison to perform
average_max_diff = AverageMaximumDifference()
elevation_comparator.add_comparison(average_max_diff)

# Process the data and perform comparisons
elevation_comparator.work()

# Save the data to file
average_max_diff.save('/home/tristan/adcirc/runs/avg_max_diff.txt')
```

### Visualize results

Coming soon...
