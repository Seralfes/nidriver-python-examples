"""NI-DCPower Pulse Current.

This example demonstrates how to use the DCPower Pulse API to generate a single Current pulse. 
This example initializes a session, configures the Source Mode and the Output Function,
configures the pulse parameters, initiates the pulse output, and takes a measurement.
"""
# Module imports
import nidcpower


with nidcpower.Session(resource_name="PXI1Slot1", options={}) as session:
    session.source_mode = nidcpower.SourceMode.SINGLE_POINT
    session.output_function = nidcpower.OutputFunction.PULSE_CURRENT

    session.pulse_current_level = 100e-3
    session.pulse_current_level_range = 100e-3
    session.pulse_bias_current_level = 0

    session.pulse_voltage_limit = 1
    session.pulse_voltage_limit_range = 1
    session.pulse_bias_voltage_limit = 1

    session.source_delay = 50e-6
    session.pulse_on_time = 0.001
    session.pulse_off_time = 0.005
    session.pulse_bias_delay = 1e-6

    session.aperture_time_units = nidcpower.ApertureTimeUnits.SECONDS
    session.aperture_time = 0.0001

    session.initiate()

    session.wait_for_event(event_id=nidcpower.Event.PULSE_COMPLETE)

    measurements = session.fetch_multiple(count=1)
    print(f"Measurements: \n- Voltage: {measurements[0][0]}"
          f"\n- Current: {measurements[0][1]}\n- In Compliance: {measurements[0][2]}")

    session.reset()
