import nidcpower

with nidcpower.Session(resource_name="PXI1Slot1", options={}) as session:
    session.source_mode = nidcpower.SourceMode.SINGLE_POINT
    session.output_function = nidcpower.OutputFunction.PULSE_VOLTAGE
    session.pulse_voltage_level = 1.0
    session.pulse_voltage_level_range = 6.0
    session.pulse_bias_voltage_level = 0.0
    session.pulse_current_limit = 10e-3
    session.pulse_current_limit_range = 10e-3
    session.pulse_bias_current_limit = 10e-3
    session.pulse_off_time = 5e-3
    session.pulse_on_time = 1e-3
    session.pulse_bias_delay = 1e-6
    session.configure_aperture_time(aperture_time=0.1e-3, units=nidcpower.ApertureTimeUnits.SECONDS)
    session.source_delay = 50e-6

    session.commit()

    with session.initiate():
        session.wait_for_event(event_id=nidcpower.Event.PULSE_COMPLETE)
        measurements = session.fetch_multiple(count=1, timeout=5)
        print(f"Measurements: \n- Voltage: {measurements[0][0]}\n- Current: {measurements[0][1]}\n- In Compliance: {measurements[0][2]}")

        session.reset()