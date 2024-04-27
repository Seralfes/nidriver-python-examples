"""NI-DCPower Hardware-Timed Voltage Sweep.

This example demonstrates how to sweep the voltage on a single channel and display the results in a graph.
This example performs a hardware-timed sweep using Sequence source mode.
"""
# Module imports
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import nidcpower


voltage_start = 1
voltage_stop = 5
points = 10
points = np.clip(points, 1, 2147483647)
voltages = []
source_delays = []

# Calculate the sequence: (stepsize * step# + start). 
if points - 1 == 0:
    voltages.append(voltage_start)

else:
    sequence_voltages = (voltage_stop - voltage_start) / (points - 1)
    for i in range(points):
        voltages.append((sequence_voltages * i) + voltage_start)

# Sets up graph properties:
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# Creates graph subplot to be displayed:
fig, ax = plt.subplots(nrows=1, figsize=(7, 9.6))

with nidcpower.Session(resource_name="PXI1Slot1", options={}) as session:
    session.source_mode = nidcpower.SourceMode.SEQUENCE
    session.output_function = nidcpower.OutputFunction.DC_VOLTAGE

    session.voltage_level_autorange = True
    session.current_limit_autorange = True

    session.source_delay = 0.005
    session.current_limit = 0.01
    
    for i in range(len(voltages)):
        source_delays.append(0.005)

    session.set_sequence(values=voltages, source_delays=source_delays)

    session.initiate()
    session.wait_for_event(event_id=nidcpower.Event.SEQUENCE_ENGINE_DONE, timeout=10)
    
    measurements = session.fetch_multiple(count=points)

    measured_voltage = []
    measured_current = []

    for measure in range(len(measurements)):
        measured_voltage.append(measurements[measure][0])
        measured_current.append(measurements[measure][1])

    # Graph settings:
    ax.xaxis.set_major_formatter(ticker.EngFormatter(unit="V"))
    ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="A"))
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Current (A)")
    ax.grid()
    ax.plot(measured_voltage, measured_current)
    
    plt.show()

    session.output_enabled = False

    session.abort()
