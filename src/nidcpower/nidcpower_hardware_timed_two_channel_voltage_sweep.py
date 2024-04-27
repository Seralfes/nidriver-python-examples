"""NI-DCPower Hardware-Timed Two-Channel Voltage Sweep (IV Curve).

This example demonstrates how to set up a hardware-timed,
two-channel nested voltage sweep and display the results in a graph (IV Curve).

Use this example to produce the characteristic curves of a FET transistor.
It can be easily adapted to test a BJT by performing a current sweep instead of a voltage sweep.
This example performs a hardware-timed sweep (with triggers and events) using Sequence source mode.

When the code is run and the graph displays,
you can click on each plot in the right hand corner of the graph to enable/disable its visibility.
"""

# Module imports
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import nidcpower


# Gain voltage start and stop for first SMU:
voltage_start_0 = 3.5
voltage_stop_0 = 3.9

# Drain voltage start and stop for second SMU:
voltage_start_1 = 1
voltage_stop_1 = 5

# Number of plots to be displayed on the graph, also used for the voltages of the first SMU that control the gate voltage
plots = 5
# Limits the plots variable to a minimum of 1, in case a value less than 1 is specified
plots = np.clip(plots, 1, 2147483647)
# Number of measurements to be taken by the second SMU
points = 10
# Limits the points variable to a minimum of 1, in case a value less than 1 is specified
points = np.clip(points, 1, 2147483647)

sequence_voltages_0 = []
sequence_voltages_1 = []
source_delays = []

# Generates step voltages for the first (0) and seconds (1) SMU:
if plots - 1 == 0:
    sequence_voltages_0.append(voltage_start_0)

elif points - 1 == 0:
    sequence_voltages_1.append(voltage_start_1)

else:
    voltages_0 = (voltage_stop_0 - voltage_start_0) / (plots - 1)
    for i in range(plots):
        sequence_voltages_0.append((voltages_0 * i) + voltage_start_0)

    voltages_1 = (voltage_stop_1 - voltage_start_1) / (points - 1)
    for i in range(points):
        sequence_voltages_1.append((voltages_1 * i) + voltage_start_1)


# Sets up graph properties:
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# Creates graph subplot to be displayed:
fig, ax = plt.subplots(nrows=1, figsize=(7, 9.6))

# Initializes both SMU sessions:
with nidcpower.Session(resource_name="PXI1Slot1", options={}) as session1, nidcpower.Session(resource_name="PXI1Slot2", options={}) as session2:
    # Settings for the first SMU:
    session1.source_mode = nidcpower.SourceMode.SEQUENCE
    session1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session1.voltage_level_autorange = True
    session1.current_limit_autorange = True
    session1.source_delay = 0.003
    session1.current_limit = 0.01
    
    # Creates an array source delays of the same size as the step voltages to configure the set_sequence method for the first SMU:
    for i in range(len(sequence_voltages_0)):
        source_delays.append(0.003)

    session1.set_sequence(values=sequence_voltages_0, source_delays=source_delays)

    # Triggering setup of the first SMU:
    session1.source_trigger_type = nidcpower.TriggerType.DIGITAL_EDGE
    session1.digital_edge_source_trigger_input_terminal = f"/{session2.io_resource_descriptor}/Engine0/SequenceIterationCompleteEvent"

    session1.commit()

    # Settings for the second SMU:
    session2.source_mode = nidcpower.SourceMode.SEQUENCE
    session2.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session2.voltage_level_autorange = True
    session2.current_limit_autorange = True
    session2.source_delay = 0.005
    session2.current_limit = 0.01

    # Resets the previous source_delays array,
    # and creates a new array source delays of the same size as the step voltages,
    # to configure the set_sequence method for the second SMU:
    source_delays = []
    for i in range(len(sequence_voltages_1)):
        source_delays.append(0.005)

    session2.set_sequence(values=sequence_voltages_1, source_delays=source_delays)

    # Triggering setup of the second SMU:
    session2.start_trigger_type = nidcpower.TriggerType.DIGITAL_EDGE
    session2.digital_edge_start_trigger_input_terminal = f"/{session1.io_resource_descriptor}/Engine0/MeasureCompleteEvent"

    session2.sequence_loop_count = plots
    session2.commit()

    # Initiates both SMU sessions:
    session2.initiate()
    session1.initiate()

    session2.wait_for_event(event_id=nidcpower.Event.SEQUENCE_ENGINE_DONE, timeout=15)

    # Stores measurements of the first SMU:
    measurements_1 = session1.fetch_multiple(count=plots, timeout=10)

    # Creates an array to store measurements of the second SMU:
    measurements_2 = []
    for plot in range(len(measurements_1)):
        measurements_2.append(session2.fetch_multiple(count=points, timeout=10))

    # Voltage and current arrays of the second SMU measurements to later use each pair as a plot:
    measured_voltages_2 = []
    measured_currents_2 = []

    # Formatting for better output visualization:
    line_format = '{:<18} {:<16} {:<10}'
    print(line_format.format('Gate Voltage (V)', 'Current (A)', 'Drain Voltage (V)'))

    for plot in range(len(measurements_1)):
        for point in range(len(measurements_2[0])):
            measured_voltages_2.append(measurements_2[plot][point][0])
            measured_currents_2.append(measurements_2[plot][point][1])
            print(line_format.format("{:.3f}".format(measurements_1[plot][0]),
                                     "{:.3e}".format(measurements_2[plot][point][1]),
                                     "{:.3f}".format(measurements_2[plot][point][0])))

        # Plots a set of points where xaxis = Voltages and yaxis = Currents of the second SMU
        ax.plot(measured_voltages_2, measured_currents_2, marker='o', label=f"{measurements_1[plot][0]:3f} V")
        measured_voltages_2 = []
        measured_currents_2 = []

    # Disables generation/acquisition on both SMUs:
    session1.output_enabled = False
    session2.output_enabled = False

    # Settings for the plot to be displayed:
    graphs = {}

    lines = ax.get_lines()
    leg = ax.legend(fancybox=True, shadow=True)
    lined = {}  # Will map legend lines to original lines.
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(True)    # # Enable picking on the legend line.
        legline.set_pickradius(3)
        lined[legline] = origline
    
    def on_pick(event):
        """On the pick event, find the original line corresponding to the legend proxy line, and toggle its visibility."""
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        #Change the alpha on the line in the legend so we can see what lines
        #that have been toggled.
        legline.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()

    # Graph settings:
    ax.xaxis.set_major_formatter(ticker.EngFormatter(unit="V"))
    ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="A"))
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (A)')
    ax.grid()

    # Connects 'pick_event' to on_pick function to hide and display each plot by clicking on their corresponding legend color:
    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.suptitle("Current (Amps) vs Voltage (Volts)")

    plt.show()
