import nidcpower

with nidcpower.Session(resource_name="PXI1Slot1", options={}) as session:
    session.source_mode = nidcpower.SourceMode.SINGLE_POINT

    session.channels[0].output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session.channels[0].voltage_level = 2.0
    session.channels[0].current_limit_range = 10e-3
    session.channels[0].current_limit = 10e-3

    session.channels[1].output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session.channels[1].voltage_level = 4.0
    session.channels[1].current_limit_range = 10e-3
    session.channels[1].current_limit = 10e-3

    session.commit()

    with session.initiate():
        session.wait_for_event(event_id=nidcpower.Event.SOURCE_COMPLETE, timeout=5)
        measurements = session.measure_multiple()
        print(f"Measurements 1: \n- Voltage: {measurements[0][0]}\n- Current: {measurements[0][1]}\n- In Compliance: {measurements[0][2]}")
        print(f"Measurements 2: \n- Voltage: {measurements[1][0]}\n- Current: {measurements[1][1]}\n- In Compliance: {measurements[1][2]}")