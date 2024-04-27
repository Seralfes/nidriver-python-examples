"""NI-SCOPE - Read and Graph Waveform.

This example demonstrates how to read waveforms from an NI-SCOPE channel, and plot it using the matplotlib library
"""
# Module imports
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import niscope


# Plot default configurations
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# Creation of plot figure and axis
fig, ax = plt.subplots()

num_samples = 250   # Number of samples to be read
samples = []        # List where samples will be stored for plotting

with niscope.Session(resource_name='PXIe5160', options={}) as session:
    # Scope configuration
    session.configure_vertical(range=5.0, coupling=niscope.VerticalCoupling.AC)
    session.configure_horizontal_timing(min_sample_rate=50000000, min_num_pts=num_samples, ref_position=50.0, num_records=1, enforce_realtime=True)

    # Read and store waveform.
    # The read() method returns a list of waveforms, with each channel being an element of the list
    # The elements within each channel are WaveformInfo class instances, with attributes that can be accessed
    waveforms = session.channels["1"].read(num_samples=num_samples)

    # The 'samples' attribute returns a memory address. To get the samples list, iterate over waveforms[0].samples and append them to a new list
    for sample in waveforms[0].samples:     # waveforms[0] corresponds to the first, and only in this example, waveform in the list
        samples.append(sample)

    # The x_increment attribute returns the delta-t (dt) of the waveform. Multiplying this by a range of num_samples ensures that both x and y axes have the same length
    x_time = [waveforms[0].x_increment * x for x in range(num_samples)]

    # Plot configuration
    ax.xaxis.set_major_formatter(ticker.EngFormatter(unit="s"))
    ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="V"))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.grid()
    ax.plot(x_time, samples)

    plt.title("Waveform Graph")
    plt.show()

    session.abort()
