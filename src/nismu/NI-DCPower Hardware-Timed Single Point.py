import nidcpower

with nidcpower.Session(resource_name="PXI1Slot1", reset=True, options={}) as session:
    session.source_mode = nidcpower.SourceMode.SINGLE_POINT
    session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session.voltage_level = 2
    session.current_limit = 0.01
    session.voltage_level_range = 10
    session.current_limit_range = 0.01
    session.source_delay = 0.05
    session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE

    session.commit()

    with session.initiate():
        measurements1 = session.fetch_multiple(count=1, timeout=1.0)
        session.voltage_level = 4
        measurements2 = session.fetch_multiple(count=1, timeout=1.0)
        print(f"Measurements 1: \n- Voltage: {measurements1[0][0]}\n- Current: {measurements1[0][1]}\n- In Compliance: {measurements1[0][2]}")
        print(f"Measurements 2: \n- Voltage: {measurements2[0][0]}\n- Current: {measurements2[0][1]}\n- In Compliance: {measurements2[0][2]}")