"""NI-DCPower Hardware-Timed Single Point.

This example demonstrates how to set up a hardware-timed Single Point operation.
The hardware is configured to source a voltage, wait for a specified delay and then take a measurement.
This example uses Single Point source mode.
"""
# Module imports
import nidcpower


with nidcpower.Session(resource_name="PXI1Slot1", reset=True, options={}) as session:
    session.source_mode = nidcpower.SourceMode.SINGLE_POINT
    session.output_function = nidcpower.OutputFunction.DC_VOLTAGE

    session.voltage_level = 2
    session.voltage_level_range = 10

    session.current_limit = 0.01
    session.current_limit_range = 0.01

    session.source_delay = 0.05

    session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE

    session.commit()

    with session.initiate():
        measurements1 = session.fetch_multiple(count=1, timeout=1.0)

        session.voltage_level = 4
        measurements2 = session.fetch_multiple(count=1, timeout=1.0)
        print(f"Measurements 1: \n- Voltage: {measurements1[0][0]}"
              f"\n- Current: {measurements1[0][1]}\n- In Compliance: {measurements1[0][2]}")
        print(f"Measurements 2: \n- Voltage: {measurements2[0][0]}"
              f"\n- Current: {measurements2[0][1]}\n- In Compliance: {measurements2[0][2]}")
