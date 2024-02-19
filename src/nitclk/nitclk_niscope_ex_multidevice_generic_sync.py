"""Multi-Device Generic Sync (TClk).

This example demonstrates synchronizing mulitple oscilloscopes, with all devices configured using the same parameters.

Synchronizing the devices requires sharing a 10 MHz clock for a phase locked-loop reference,
and sharing a one-time synchronization pulse that resets the clocks dividers on the oscilloscope.

The master device will also route a digital trigger to the slave device when it receives its trigger.

This example preforms all the operations required to synchronize the devices through the NI-TClk API.
"""

import pprint

import niscope
import nitclk


pp = pprint.PrettyPrinter(indent=4, width=80)

with niscope.Session(resource_name="PXI1Slot1", options={}) as session1, niscope.Session(resource_name="PXI1Slot2", options={}) as session2:
    session_list = [session1, session2]
    for session in session_list:
        session.configure_chan_characteristics(input_impedance=1e6, max_input_frequency=-1.00)  # 1 M ohm and -1 to achieve full bandwidth
        session.configure_vertical(range=5.00, coupling=niscope.VerticalCoupling.DC, offset=0, probe_attenuation=1, enabled=True)
        session.configure_horizontal_timing(min_sample_rate=100e6, min_num_pts=1000, ref_position=50, num_records=1, enforce_realtime=True)

        if session == session_list[0]:
            session.configure_trigger_edge(trigger_source='0', level=0.00, trigger_coupling=niscope.TriggerCoupling.DC, slope=niscope.TriggerSlope.POSITIVE, holdoff=0, delay=0)

    nitclk.configure_for_homogeneous_triggers(session_list)
    nitclk.synchronize(session_list, min_tclk_period=0)
    nitclk.initiate(session_list)

    for session in session_list:
        print(session.channels[0].fetch_array_measurement(array_meas_function=niscope.ArrayMeasurement.MULTI_ACQ_AVERAGE, meas_num_samples=-1))
